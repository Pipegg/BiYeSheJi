import json
import logging
from typing import Optional

from django.http import HttpRequest, HttpResponse, QueryDict
from django.utils.datastructures import MultiValueDict
from django.utils.deprecation import MiddlewareMixin
from werkzeug.local import LocalStack
from django.middleware.csrf import get_token

from .ctx import RequestContext
from .globals import _cv_request
from core import R, query, DB

# 设置日志记录器
logger = logging.getLogger(__name__)

class CustomRequest(HttpRequest):
    session_data: Optional[query.Model]
    JSON: Optional[MultiValueDict]
    requestCtx: Optional[RequestContext]

    def __init__(self):
        super().__init__()
        self.session_data = None
        self.JSON = MultiValueDict()
        self.requestCtx = None

# 设置代理中间件对象，和jwt token 解密、cors 跨域处理
class MiddlewareProxy(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def process_request(self, request):
        # Convert the request to CustomRequest
        if not isinstance(request, CustomRequest):
            custom_request = CustomRequest()
            custom_request.__dict__.update(request.__dict__)
            request = custom_request

        # 获取当前token
        token = request.headers.get('token')
        # 获取当前token失败，尝试是不是 authorization 头
        if not token:
            token = request.headers.get('authorization')

        # 创建自定义session数据对象
        request.session_data = query.Model(None, {})

        # 判断token 是否存在
        if token:
            # 将token 进行解密
            data = R.jwtDecode(token)
            # token 解密成功，
            if data is not None:
                # 重新创建session数据对象
                session_data = query.Model(None,data)
                # 更新session数据对象内容
                session_data.update(DB.name(session_data['table']).find(session_data['id']))
                # 重新设置session数据对象
                request.session_data = session_data

        # 创建json 对象
        request.JSON = MultiValueDict()
        # 判断是否为json 的方式提交
        if request.content_type == 'application/json' and request.body:
            # 是则将数据进行解密
            try:
                post = json.loads(request.body.decode('utf-8'))
                # 判断是否为dict 字段格式，是的话写入到 request.JSON 对象当中
                if isinstance(post,dict):
                    for key,value in post.items():
                        request.JSON.appendlist(key,value)
            except json.JSONDecodeError:
                logger.warning(f"Failed to decode JSON body for {request.path}")

        # 创建上下文代理对象
        request.requestCtx = RequestContext(request)
        # 将上下文对象写入
        request.requestCtx.push()
        return None

    def process_response(self, request, response: HttpResponse):
        if isinstance(request, CustomRequest) and request.requestCtx:
            # 解除当前上下文内容
            request.requestCtx.pop()
            
        # 为GET请求设置CSRF token
        if request.method == 'GET':
            get_token(request)
            
        logger.debug(f"Processed response for {request.method} {request.path} with headers: {dict(response.headers)}")
        return response


# =====================
# 依赖导入
# =====================
import json
import decimal
import datetime
import time
import jwt
from itertools import chain
from django.forms import model_to_dict
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from core.settings import SECRET_KEY

# =====================
# JSON 响应工具
# =====================
def jsonReturn(code=0, msg='', data=None):
    """
    标准化 JSON 响应格式
    """
    result = {
        'code': code,
        'msg': msg,
        'data': data
    }
    content = json.dumps(result, cls=DecimalEncoder)
    return HttpResponse(content, content_type='application/json;charset=UTF-8')

def success(data):
    """
    返回成功响应
    """
    return jsonReturn(data=data)

def error(msg, code=1):
    """
    返回错误响应
    """
    return jsonReturn(code=code, msg=msg)

# =====================
# JSON 序列化工具
# =====================
class DecimalEncoder(DjangoJSONEncoder):
    """
    支持 Decimal、datetime、Django Model 的 JSON 编码器
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, models.Model):
            return django_to_dict(o)
        else:
            return super().default(o)

def django_to_dict(instance, fields=None, exclude=None):
    """
    将 Django Model 实例转为 dict
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    for key, f in opts.concrete_model.__dict__.items():
        if isinstance(f, property):
            data[key] = getattr(instance, key)
    return data

# =====================
# JWT 工具
# =====================
def jwtEncode(payload, exp=None):
    """
    生成 JWT token
    """
    jwtResult = {
        'iat': int(time.time()),
        'iss': 'Issuer'
    }
    if exp is not None:
        jwtResult['exp'] = int(time.time()) + exp
    jwtResult['data'] = payload
    try:
        return jwt.encode(jwtResult, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        print(e)
        return ''

def jwtDecode(token):
    """
    解密 JWT token，返回 payload
    """
    try:
        result = jwt.decode(token, SECRET_KEY, issuer='Issuer', algorithms=['HS256'])
    except Exception as e:
        print(e)
        return None
    if not result or not isinstance(result, dict):
        return None
    if 'exp' in result and result['exp'] < time.time():
        return None
    return result['data']

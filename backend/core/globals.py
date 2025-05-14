from contextvars import ContextVar

from django.contrib.sessions.backends.base import SessionBase
from werkzeug.local import LocalProxy

from django.http import HttpRequest

# 没有代理对象的时候的报错信息
_no_req_msg = """\
Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request. Consult the documentation on testing for
information about how to avoid this problem.\
"""

# 创建代理对象的上下文处理
_cv_request:ContextVar = ContextVar("django.request_ctx")

# 上下文的对象
request_ctx = LocalProxy(  # type: ignore[assignment]
    _cv_request, unbound_message=_no_req_msg
)
# 上下文中的 request 对象
request: HttpRequest = LocalProxy(
    _cv_request,"request",unbound_message=_no_req_msg
)

# 上下文中的 session 会话对象
session: SessionBase = LocalProxy(
    _cv_request,"session",unbound_message=_no_req_msg
)

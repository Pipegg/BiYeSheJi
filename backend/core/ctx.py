import contextvars
from types import TracebackType

from django.http import HttpRequest
from .globals import _cv_request

# 内容上下文
class RequestContext:
    # 初始化Request 类
    def __init__(self,request: HttpRequest):
        self.request = request
        self.session = request.session
        self._cv_tokens: list[tuple[contextvars.Token]] = []

    # 写入代理类 _cv_request
    def push(self):
        # 设置的同时返回之前的上下文件
        self._cv_tokens.append((_cv_request.set(self),))
        pass

    # 生命周期结束了，去除结果
    def pop(self):
        # 判断是否只有一个数据
        clear_request = len(self._cv_tokens) == 1
        # 获取当前的上下文
        ctx = _cv_request.get()
        # 获取保存在本地的
        token, = self._cv_tokens.pop()
        # 重置当前上下文
        _cv_request.reset(token)
        # 判断这个上下文是否不存在，不存在则出错
        if ctx is not self:
            raise AssertionError(
                f"Popped wrong request context. ({ctx!r} instead of {self!r})"
            )
        #print("pop self")
        pass

    # 以下是实现 python 内部的魔法函数
    def __enter__(self) :
        self.push()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        tb,
    ) -> None:
        self.pop()

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} {self.request.get_raw_uri()!r}"
            f" [{self.request.method}] of {self.request.method}>"
        )




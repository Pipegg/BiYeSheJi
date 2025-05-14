from functools import wraps
from django.urls import path, include, re_path
from django.http import JsonResponse

# 路由装饰器类的实现，只需要在方法上 添加 @router.route('路径') 就能配置，省去了在urls.py 中配置的繁琐操作
class Blueprint:
    def __init__(self,name,url_prefix = ''):
        if len(url_prefix):
            url_prefix = url_prefix.strip('/') + '/'
        self.url_prefix = url_prefix
        self.name = name
        self.urls = []
        pass

    # 装饰器类
    def route(self, rule:str, name = None, methods = None):
        if name is None:
            name = rule.strip('/').replace('/','_')

        if rule != '':
            rule = rule.strip('/') + '/'

        def decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                try:
                    # 方法检查
                    if methods and request.method not in methods:
                        return JsonResponse({
                            'code': 405,
                            'message': f'不支持 {request.method} 方法'
                        }, status=405)
                    return func(request, *args, **kwargs)
                except Exception as e:
                    return JsonResponse({
                        'code': 500,
                        'message': str(e)
                    }, status=500)

            self.add_rule(rule, wrapper, name)
            return wrapper

        return decorator

    # 添加规则
    def add_rule(self, rule, func, name):
        p = path(self.url_prefix+rule, func, name=name)
        self.urls.append(p)
        pass


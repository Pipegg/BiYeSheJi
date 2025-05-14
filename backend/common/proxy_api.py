import json
import requests
from django.http import JsonResponse, HttpResponse
from django.urls import path
import logging
from core import R

logger = logging.getLogger(__name__)

def proxy_api(request):
    """
    代理API，用于解决前端跨域请求问题
    接收请求参数中的target_url，然后转发请求到该URL
    """
    if request.method == 'OPTIONS':
        return R.success('OK')
    
    try:
        # 从请求中获取目标URL
        if request.method == 'POST':
            if request.body:
                try:
                    data = json.loads(request.body)
                    target_url = data.get('target_url')
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in request body")
                    return R.error("Invalid JSON")
            else:
                return R.error("Empty request body")
        else:
            target_url = request.GET.get('target_url')
        
        if not target_url:
            return R.error("Missing target_url parameter")
        
        logger.info(f"Proxying request to: {target_url}")
        
        # 转发请求
        headers = {
            'User-Agent': request.headers.get('User-Agent', ''),
            'Accept': request.headers.get('Accept', ''),
            'Accept-Language': request.headers.get('Accept-Language', ''),
            'Content-Type': request.headers.get('Content-Type', 'application/json'),
            'Origin': request.build_absolute_uri('/').rstrip('/'),
            'Referer': request.build_absolute_uri()
        }
        
        method = request.method
        if method == 'GET':
            response = requests.get(target_url, headers=headers, timeout=10)
        elif method == 'POST':
            forwarded_data = None
            if 'forwarded_data' in data:
                forwarded_data = data['forwarded_data']
            response = requests.post(target_url, json=forwarded_data, headers=headers, timeout=10)
        else:
            return R.error(f"Unsupported method: {method}")
        
        # 返回结果
        return R.success(response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text)
    
    except requests.RequestException as e:
        logger.error(f"Error proxying request: {str(e)}")
        return R.error(f"Error proxying request: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return R.error(f"Unexpected error: {str(e)}")

urlpatterns = [
    path('', proxy_api, name='proxy_api'),
] 
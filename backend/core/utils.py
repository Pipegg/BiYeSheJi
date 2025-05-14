from .query import DB, Model
from django.shortcuts import render
from .globals import request, session as sessionStore
from .R import DecimalEncoder, jwtDecode
from django.http import HttpRequest
import json
import random
from objtyping import to_primitive
from datetime import datetime
import time as osTime

# =====================
# 参数获取与解析
# =====================
def param(name: str, default=None) -> str:
    """
    获取单个参数，支持 GET、POST、JSON body，始终返回 str
    """
    val = None
    if name in request.GET:
        val = request.GET.getlist(name)
    elif name in request.POST:
        val = request.POST.getlist(name)
    else:
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            if name in json_body:
                val = json_body[name]
                if not isinstance(val, list):
                    val = [val]
        except Exception:
            pass
    if val is not None:
        if len(val) == 1:
            return str(val[0])
        return ",".join([str(v) for v in val])
    return str(default) if default is not None else ""

input = param

def paramlist(name: str, defs=None) -> list:
    """
    获取参数列表，支持 GET、POST、JSON body，始终返回 list
    """
    val = defs
    if name in request.GET:
        val = request.GET.getlist(name)
    elif name in request.POST:
        val = request.POST.getlist(name)
    else:
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            if name in json_body:
                val = json_body[name]
                if not isinstance(val, list):
                    val = [val]
        except Exception:
            pass
    return val if isinstance(val, list) else ([] if val is None else [val])

inputlist = paramlist

# =====================
# JSON 工具
# =====================
def jsonEncode(root):
    v = to_primitive(root)
    return json.dumps(v, cls=DecimalEncoder)

def jsonDecode(string):
    return json.loads(string)

# =====================
# Session 工具
# =====================
def session(name):
    return sessionStore.get(name)

# =====================
# 登录校验（支持 JWT）
# =====================
def checkLogin():
    # 优先检查 JWT token
    try:
        req = request if isinstance(request, HttpRequest) else None
        token = None
        if req:
            auth_header = req.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        else:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token:
            session_data = jwtDecode(token)
            if session_data and isinstance(session_data, dict) and session_data.get('username'):
                for k, v in session_data.items():
                    sessionStore[k] = v
                return True
    except Exception:
        pass
    username = sessionStore.get("username")
    return bool(username)

def checkLoginNot():
    return not checkLogin()

# =====================
# 时间与编号工具
# =====================
def date(format, t=None):
    if isinstance(t, datetime):
        return t.strftime(format)
    if isinstance(t, int):
        return osTime.strftime(format, osTime.localtime(t))
    return datetime.now().strftime(format)

def time():
    return int(osTime.time())

def getDateStr():
    return date("%Y-%m-%d %H:%M:%S")

def getID():
    a = random.randint(10000, 99999)
    return osTime.strftime("%y%m%d%H") + str(a)

# =====================
# 树结构与路径工具
# =====================
def getAllChild(table, pid, value):
    templists = DB.name(table).select()
    return _getAllChild(pid, value, templists)

def _getAllChild(pid, value, templates):
    result = [value]
    for child in templates:
        if child.get(pid) == value:
            ret = _getAllChild(pid, child.get("id"), templates)
            if ret:
                result += ret
    return result

def postion(table, pid, name, value):
    items = []
    parentid = value
    while parentid:
        mp = DB.name(table).find(parentid)
        if not mp or not len(mp):
            break
        items.append(mp[name])
        parentid = mp.get(pid)
    items.reverse()
    return items

getTreeOption = postion

# =====================
# 依赖导入
# =====================
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Admins
from core import utils, DB
import json
from core import Blueprint, R

# =====================
# 路由注册
# =====================
router = Blueprint("admins")

# =====================
# 条件构建工具
# =====================
def getWhere(request, qs):
    """
    根据前台填写的搜索条件，动态构建查询集
    """
    if utils.param("username"):
        qs = qs.filter(username__contains=utils.param("username"))
    if utils.param("xingming"):
        qs = qs.filter(xingming__contains=utils.param("xingming"))
    orderby = utils.param("orderby", "id")
    sort = utils.param("sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)
    return qs

# =====================
# 列表与查询
# =====================
@router.route('admin/selectAll/')
def selectAll(request):
    qs = getWhere(request, Admins.objects)
    result = list(qs.values())
    return R.success(result)

@router.route('admin/list/')
def adminlist(request):
    if not utils.checkLogin():
        return R.error("请登录后操作", 1001)
    qs = getWhere(request, Admins.objects)
    qs = qs.all()
    pagesize = utils.param("pagesize", 12)
    paginator = Paginator(qs, pagesize)
    page = utils.param('page', 1)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)
    result = {
        'lists': {
            'records': list(lists),
            'total': paginator.count
        }
    }
    return R.success(result)

@router.route('/findById/')
def findById(request):
    id = utils.param("id")
    mmm = Admins.objects.get(pk=id)
    if mmm is None:
        return R.error("没有找到相关数据")
    return R.success(mmm)

# =====================
# 删除
# =====================
@router.route('delete/')
def delete(request):
    ids = json.loads(request.body)
    for id in ids:
        map = Admins.objects.get(pk=id)
        map.delete()
    return R.success("删除成功")

# =====================
# 新增
# =====================
@router.route('insert/')
def insert(request):
    data = {
        'username': utils.param('username', ''),
        'pwd': utils.param('pwd', ''),
        'xingming': utils.param('xingming', ''),
        'xingbie': utils.param('xingbie', ''),
        'lianxifangshi': utils.param('lianxifangshi', ''),
        'touxiang': utils.param('touxiang', ''),
    }
    if not data['username']:
        return R.error("请填写帐号")
    if len(Admins.objects.filter(username=data['username']).all()):
        return R.error('帐号已重复')
    if not data['pwd']:
        return R.error("请填写密码")
    if not data['xingming']:
        return R.error("请填写姓名")
    if not data['xingbie']:
        return R.error("请填写性别")
    if not data['lianxifangshi']:
        return R.error("请填写联系方式")
    model = Admins(**data)
    model.save(force_insert=True)
    return R.success(model)

# =====================
# 更新
# =====================
@router.route('update/')
def update(request):
    charuid = utils.param('id')
    old = Admins.objects.get(pk=charuid)
    data = {
        'id': charuid,
        'username': utils.param('username', old.username),
        'pwd': utils.param('pwd', old.pwd),
        'xingming': utils.param('xingming', old.xingming),
        'xingbie': utils.param('xingbie', old.xingbie),
        'lianxifangshi': utils.param('lianxifangshi', old.lianxifangshi),
        'touxiang': utils.param('touxiang', old.touxiang),
    }
    if not data['username']:
        return R.error("请填写帐号")
    if len(Admins.objects.exclude(id=data['id']).filter(username=data['username']).all()):
        return R.error('帐号已重复')
    if not data['xingming']:
        return R.error("请填写姓名")
    if not data['xingbie']:
        return R.error("请填写性别")
    if not data['lianxifangshi']:
        return R.error("请填写联系方式")
    model = Admins(**data)
    model.save(force_update=True)
    return R.success(model)

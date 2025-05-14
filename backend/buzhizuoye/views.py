# =====================
# 依赖导入
# =====================
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from typing import Dict, Any, List
import json
from .models import Buzhizuoye
from core import utils, DB, Blueprint, R
from kechengxinxi.models import Kechengxinxi

# =====================
# 路由装饰器
# =====================
router = Blueprint("buzhizuoye")

# =====================
# 工具函数
# =====================

def getWhere(request, qs) -> Any:
    """
    根据前台填写的搜索条件，设置相关搜索
    Args:
        request: 请求对象
        qs: 查询集
    Returns:
        过滤后的查询集
    """
    if utils.param("kechengxinxiid"):
        qs = qs.filter(kechengxinxiid=utils.param("kechengxinxiid"))
    if utils.param("kechengbianhao"):
        qs = qs.filter(kechengbianhao__contains=utils.param("kechengbianhao"))
    if utils.param("kechengmingcheng"):
        qs = qs.filter(kechengmingcheng__contains=utils.param("kechengmingcheng"))
    if utils.param("kechengfenlei"):
        qs = qs.filter(kechengfenlei=utils.param("kechengfenlei"))
    if utils.param("zuoyebianhao"):
        qs = qs.filter(zuoyebianhao__contains=utils.param("zuoyebianhao"))
    if utils.param("zuoyemingcheng"):
        qs = qs.filter(zuoyemingcheng__contains=utils.param("zuoyemingcheng"))

    # 获取排序字段，默认为id
    orderby: str = utils.param("orderby", "id")
    # 获取是升序还是降序，默认为降序
    sort: str = utils.param("sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs

# =====================
# 视图函数
# =====================

@router.route('admin/selectAll/')
def selectAll(request) -> Any:
    """获取所有数据"""
    qs = getWhere(request, Buzhizuoye.objects)
    result = list(qs.values())
    return R.success(result)

@router.route('admin/list/')
def adminlist(request) -> Any:
    """管理员列表页面"""
    if not utils.checkLogin():
        return R.error("请登录后操作", 1001)
    
    qs = getWhere(request, Buzhizuoye.objects)
    qs = qs.all()
    
    # 分页处理
    pagesize: int = int(utils.param("pagesize", 12))
    paginator = Paginator(qs, pagesize)
    page: int = int(utils.param('page', 1))
    
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

@router.route('admin/fabujiaoshi/')
def fabujiaoshi(request) -> Any:
    """发布教师列表页面"""
    if not utils.checkLogin():
        return R.error("请登录后操作", 1001)
    
    qs = getWhere(request, Buzhizuoye.objects)
    qs = qs.filter(fabujiaoshi=utils.session('username'))
    qs = qs.all()
    
    # 分页处理
    pagesize: int = int(utils.param("pagesize", 12))
    paginator = Paginator(qs, pagesize)
    page: int = int(utils.param('page', 1))
    
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
def findById(request) -> Any:
    """根据id获取一行数据"""
    id = utils.param("id")
    try:
        mmm = Buzhizuoye.objects.get(pk=id)
        return R.success(mmm)
    except Buzhizuoye.DoesNotExist:
        return R.error("没有找到相关数据")

@router.route('detail/')
def detail(request) -> Any:
    """打开前台详情页面信息"""
    id = utils.param('id')
    try:
        map = Buzhizuoye.objects.get(pk=id)
        return R.success("ok")
    except Buzhizuoye.DoesNotExist:
        return R.error("没有找到相关数据")

@router.route('delete/')
def delete(request) -> Any:
    """根据数组id删除数据"""
    ids = json.loads(request.body)
    for id in ids:
        try:
            map = Buzhizuoye.objects.get(pk=id)
            map.delete()
        except Buzhizuoye.DoesNotExist:
            continue
    return R.success("删除成功")

@router.route('insert/')
def insert(request) -> Any:
    """插入布置作业数据"""
    data = {
        'kechengxinxiid': str(utils.param('kechengxinxiid', '0')),
        'kechengbianhao': str(utils.param('kechengbianhao', '')),
        'kechengmingcheng': str(utils.param('kechengmingcheng', '')),
        'kechengfenlei': str(utils.param('kechengfenlei', '0')),
        'fabujiaoshi': str(utils.param('fabujiaoshi', '')),
        'zuoyebianhao': str(utils.param('zuoyebianhao', '')),
        'jiezhiriqi': str(utils.param('jiezhiriqi', '')),
        'zuoyemingcheng': str(utils.param('zuoyemingcheng', '')),
        'zuoyefujian': str(utils.param('zuoyefujian', '')),
        'yitijiaorenshu': str(utils.param('yitijiaorenshu', '')),
        'zuoyemiaoshu': str(utils.param('zuoyemiaoshu', '')),
    }

    # 设置默认值
    if data['fabujiaoshi'] == '':
        data['fabujiaoshi'] = str(utils.session("username") or '')
    if data['yitijiaorenshu'] == '':
        data['yitijiaorenshu'] = '0'
    else:
        data['yitijiaorenshu'] = str(int(data['yitijiaorenshu']))

    # 参数验证
    if not data['zuoyebianhao']:
        return R.error("请填写作业编号")
    if not data['jiezhiriqi']:
        return R.error("请填写截至日期")
    if not data['zuoyemingcheng']:
        return R.error("请填写作业名称")
    if not data['zuoyefujian']:
        return R.error("请填写作业附件")
    if not data['zuoyemiaoshu']:
        return R.error("请填写作业描述")

    # 创建并保存
    model = Buzhizuoye(**data)
    model.save()
    return R.success("添加成功")

@router.route('update/')
def update(request) -> Any:
    """更新布置作业数据"""
    id = utils.param("id")
    try:
        model = Buzhizuoye.objects.get(pk=id)
    except Buzhizuoye.DoesNotExist:
        return R.error("没有找到相关数据")

    data = {
        'kechengxinxiid': str(utils.param('kechengxinxiid', '0')),
        'kechengbianhao': str(utils.param('kechengbianhao', '')),
        'kechengmingcheng': str(utils.param('kechengmingcheng', '')),
        'kechengfenlei': str(utils.param('kechengfenlei', '0')),
        'fabujiaoshi': str(utils.param('fabujiaoshi', '')),
        'zuoyebianhao': str(utils.param('zuoyebianhao', '')),
        'jiezhiriqi': str(utils.param('jiezhiriqi', '')),
        'zuoyemingcheng': str(utils.param('zuoyemingcheng', '')),
        'zuoyefujian': str(utils.param('zuoyefujian', '')),
        'yitijiaorenshu': str(utils.param('yitijiaorenshu', '')),
        'zuoyemiaoshu': str(utils.param('zuoyemiaoshu', '')),
    }

    # 参数验证
    if not data['zuoyebianhao']:
        return R.error("请填写作业编号")
    if not data['jiezhiriqi']:
        return R.error("请填写截至日期")
    if not data['zuoyemingcheng']:
        return R.error("请填写作业名称")
    if not data['zuoyefujian']:
        return R.error("请填写作业附件")
    if not data['zuoyemiaoshu']:
        return R.error("请填写作业描述")

    # 更新数据
    for key, value in data.items():
        setattr(model, key, value)
    model.save()
    return R.success("修改成功")




from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Wendaxiaoxi
from core import utils,DB
import json


# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("wendaxiaoxi")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    # 判断是否填写回复内容
    if utils.param("huifuneirong"):
        qs = qs.filter(huifuneirong__contains=utils.param("huifuneirong"))



    # 获取排序字段，默认为id
    orderby = utils.param( "orderby", "id")
    # 获取是升序还是降序，默认为降序
    sort = utils.param( "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs

# 获取所有数据
@router.route('admin/selectAll/')
def selectAll(request):
    # 获取搜素条件
    qs = getWhere(request,Wendaxiaoxi.objects)
    # 获取所有行
    result = list(qs.values())
	
    # 返回json 数据到前端
    return R.success(result)


# 管理员列表页面
@router.route('admin/list/')
def adminlist(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取搜素条件
    qs = getWhere(request,Wendaxiaoxi.objects)

    # 获取所有行
    qs = qs.all()
    # 分页数
    pagesize = utils.param( "pagesize", 12)
    # 分页获取数据
    paginator = Paginator(qs, pagesize)
    # 获取当前page页码，默认为1
    page = utils.param('page', 1)
    try:
        lists = paginator.page(page)  # 分页
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    # 返回前端所需的相关数据
    result = {
        'lists': {
            # 返回列表
            'records': list(lists),
            # 返回行数
            'total': paginator.count
        }
    }

    # 返回json 数据到前端
    return R.success(result)








# 根据id 获取一行数据
@router.route('/findById/')
def findById(request):
    # 获取提交的参数id
    id = utils.param("id")
    # 根据id 获取一行数据
    mmm = Wendaxiaoxi.objects.get(pk = id)
    # 没有找到这行数据则返回没有找到相关数据
    if mmm == None:
        return R.error("没有找到相关数据")

    # 根据获取的
    return R.success(mmm)





# 根据数组id 删除数据
@router.route('delete/')
def delete(request):
    # 获取提交body内容，进行json 解析
    ids = json.loads(request.body)
    # 循环删除数据
    for id in ids:
        # 获取一行数据
        map = Wendaxiaoxi.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")







# 插入问答消息数据
@router.route('insert/')
def insert(request):

    # 获取提交的数据
    data = {
        'xiaoxineirong': utils.param('xiaoxineirong',''),
        'huifuneirong': utils.param('huifuneirong',''),
        'guanlianhuifu': utils.param('guanlianhuifu',0),
        'yonghu': utils.param('yonghu',''),
        'addtime': utils.getDateStr(),

    }



    if data['yonghu'] == '':
        data['yonghu'] = utils.session( "username")








    # 创建model 对象，然后执行插入
    model = Wendaxiaoxi(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    # 返回插入的数据
    return R.success( model )

# 更新问答消息数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Wendaxiaoxi.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'xiaoxineirong': utils.param('xiaoxineirong',old.xiaoxineirong),
        'huifuneirong': utils.param('huifuneirong',old.huifuneirong),
        'guanlianhuifu': utils.param('guanlianhuifu',old.guanlianhuifu),
        'yonghu': utils.param('yonghu',old.yonghu),
        'addtime': old.addtime,

    }





    # 创建问答消息 对象
    model = Wendaxiaoxi(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




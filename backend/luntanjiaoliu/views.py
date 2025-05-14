from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Luntanjiaoliu
from core import utils,DB
import json


# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("luntanjiaoliu")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    # 判断是否填写编号
    if utils.param("bianhao"):
        qs = qs.filter(bianhao__contains=utils.param("bianhao"))
    # 判断是否填写标题
    if utils.param("biaoti"):
        qs = qs.filter(biaoti__contains=utils.param("biaoti"))
    # 判断是否选择分类
    if utils.param("fenlei"):
        qs = qs.filter(fenlei=utils.param("fenlei"))

    # 判断是否设置 issh
    if utils.param('issh'):
        qs = qs.filter(issh=utils.param('issh'))


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
    qs = getWhere(request,Luntanjiaoliu.objects)
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
    qs = getWhere(request,Luntanjiaoliu.objects)

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


# 发布人列表页面
@router.route('admin/faburen/')
def faburen(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取条件
    qs = getWhere(request,Luntanjiaoliu.objects)
    # 设置发布人值为当前登录用户
    qs = qs.filter(faburen=utils.session('username'))

    # 获取所有信息
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


# 前台列表页面
@router.route('/index/')
def index(request):

    # 获取前端搜素条件
    qs = getWhere(request,Luntanjiaoliu.objects)
    # 必须审核后才展示该数据
    qs = qs.filter(issh="是")

    # 获取所有数据
    qs = qs.all()
    # 分页数
    pagesize = utils.param("pagesize", 12)
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
    mmm = Luntanjiaoliu.objects.get(pk = id)
    # 没有找到这行数据则返回没有找到相关数据
    if mmm == None:
        return R.error("没有找到相关数据")

    # 根据获取的
    return R.success(mmm)




# 打开前台详情页面信息
@router.route('detail/')
def detail(request):
    # 获取提交的参数id
    id = utils.param('id')
    # 根据id 获取一行数据
    map = Luntanjiaoliu.objects.get(pk=id)


    return R.success("ok")

# 根据数组id 删除数据
@router.route('delete/')
def delete(request):
    # 获取提交body内容，进行json 解析
    ids = json.loads(request.body)
    # 循环删除数据
    for id in ids:
        # 获取一行数据
        map = Luntanjiaoliu.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")

# 审核数据
@router.route('admin/checkIssh')
def checkIssh(request):
    # 获取提交的id
    id = utils.param('id')
    # 根据id 获取一行数据
    map = Luntanjiaoliu.objects.get(pk = id)
    # 设置issh 提交的内容
    map.issh = utils.param('value')
    # 更新数据
    map.save(force_update = True)
    # 返回成功的内容
    return R.success(map.issh)






# 插入论坛交流数据
@router.route('insert/')
def insert(request):

    # 获取提交的数据
    data = {
        'bianhao': utils.param('bianhao',''),
        'biaoti': utils.param('biaoti',''),
        'fenlei': utils.param('fenlei',0),
        'tupian': utils.param('tupian',''),
        'huifushu': utils.param('huifushu',''),
        'faburen': utils.param('faburen',''),
        'hudongneirong': utils.param('hudongneirong',''),
        'quanxian': utils.param('quanxian',''),
        'xingming': utils.param('xingming',''),
        'touxiang': utils.param('touxiang',''),
        'addtime': utils.getDateStr(),

    }



    if data['huifushu'] == '':
        data['huifushu'] = 0
    else:
        data['huifushu'] = int(data['huifushu'])
    if data['faburen'] == '':
        data['faburen'] = utils.session( "username")

    # 判断是否有填写编号。
    if not data['bianhao']:
        return R.error("请填写编号")
    # 判断是否有填写标题。
    if not data['biaoti']:
        return R.error("请填写标题")
    # 判断是否有填写分类。
    if not data['fenlei']:
        return R.error("请填写分类")







    # 创建model 对象，然后执行插入
    model = Luntanjiaoliu(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    # 返回插入的数据
    return R.success( model )

# 更新论坛交流数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Luntanjiaoliu.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'bianhao': utils.param('bianhao',old.bianhao),
        'biaoti': utils.param('biaoti',old.biaoti),
        'fenlei': utils.param('fenlei',old.fenlei),
        'tupian': utils.param('tupian',old.tupian),
        'huifushu': utils.param('huifushu',old.huifushu),
        'faburen': utils.param('faburen',old.faburen),
        'hudongneirong': utils.param('hudongneirong',old.hudongneirong),
        'quanxian': utils.param('quanxian',old.quanxian),
        'xingming': utils.param('xingming',old.xingming),
        'touxiang': utils.param('touxiang',old.touxiang),
        'addtime': old.addtime,

    }

    if data['huifushu'] == '':
        data['huifushu'] = 0
    else:
        data['huifushu'] = int(data['huifushu'])

    # 判断是否有填写编号。
    if not data['bianhao']:
        return R.error("请填写编号")
    # 判断是否有填写标题。
    if not data['biaoti']:
        return R.error("请填写标题")
    # 判断是否有填写分类。
    if not data['fenlei']:
        return R.error("请填写分类")



    # 创建论坛交流 对象
    model = Luntanjiaoliu(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Kechengxuexi
from core import utils,DB
import json

from kechengxinxi.models import Kechengxinxi
# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("kechengxuexi")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    if utils.param("kechengxinxiid"):
        qs = qs.filter(kechengxinxiid=utils.param("kechengxinxiid"))
    # 判断是否填写课程编号
    if utils.param("kechengbianhao"):
        qs = qs.filter(kechengbianhao__contains=utils.param("kechengbianhao"))
    # 判断是否填写课程名称
    if utils.param("kechengmingcheng"):
        qs = qs.filter(kechengmingcheng__contains=utils.param("kechengmingcheng"))
    # 判断是否选择课程分类
    if utils.param("kechengfenlei"):
        qs = qs.filter(kechengfenlei=utils.param("kechengfenlei"))
    # 判断是否填写学习编号
    if utils.param("xuexibianhao"):
        qs = qs.filter(xuexibianhao__contains=utils.param("xuexibianhao"))
    # 判断是否填写学生用户
    if utils.param("xueshengyonghu"):
        qs = qs.filter(xueshengyonghu__contains=utils.param("xueshengyonghu"))



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
    qs = getWhere(request,Kechengxuexi.objects)
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
    qs = getWhere(request,Kechengxuexi.objects)

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


# 发布教师列表页面
@router.route('admin/fabujiaoshi/')
def fabujiaoshi(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取条件
    qs = getWhere(request,Kechengxuexi.objects)
    # 设置发布教师值为当前登录用户
    qs = qs.filter(fabujiaoshi=utils.session('username'))

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
# 学生用户列表页面
@router.route('admin/xueshengyonghu/')
def xueshengyonghu(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取条件
    qs = getWhere(request,Kechengxuexi.objects)
    # 设置学生用户值为当前登录用户
    qs = qs.filter(xueshengyonghu=utils.session('username'))

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






# 根据id 获取一行数据
@router.route('/findById/')
def findById(request):
    # 获取提交的参数id
    id = utils.param("id")
    # 根据id 获取一行数据
    mmm = Kechengxuexi.objects.get(pk = id)
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
        map = Kechengxuexi.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")







# 插入课程学习数据
@router.route('insert/')
def insert(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作");

    # 获取提交的数据
    data = {
        'kechengxinxiid': utils.param('kechengxinxiid',0),
        'kechengbianhao': utils.param('kechengbianhao',''),
        'kechengmingcheng': utils.param('kechengmingcheng',''),
        'kechengfenlei': utils.param('kechengfenlei',0),
        'fabujiaoshi': utils.param('fabujiaoshi',''),
        'xuexibianhao': utils.param('xuexibianhao',''),
        'xuexijindu': utils.param('xuexijindu',''),
        'xueshengyonghu': utils.param('xueshengyonghu',''),
        'xuexizhuangtai': utils.param('xuexizhuangtai',''),
        'addtime': utils.getDateStr(),
    }

    if data['fabujiaoshi'] == '':
        data['fabujiaoshi'] = utils.session( "username")
    if data['xuexijindu'] == '':
        data['xuexijindu'] = 0
    else:
        data['xuexijindu'] = int(data['xuexijindu'])
    if data['xueshengyonghu'] == '':
        data['xueshengyonghu'] = utils.session( "username")

    # 判断是否有填写学习编号。
    if not data['xuexibianhao']:
        return R.error("请填写学习编号")

    # 创建model 对象，然后执行插入
    model = Kechengxuexi(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    # 返回插入的数据
    return R.success( model )

# 更新课程学习数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Kechengxuexi.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'kechengxinxiid': utils.param('kechengxinxiid',old.kechengxinxiid),
        'kechengbianhao': utils.param('kechengbianhao',old.kechengbianhao),
        'kechengmingcheng': utils.param('kechengmingcheng',old.kechengmingcheng),
        'kechengfenlei': utils.param('kechengfenlei',old.kechengfenlei),
        'fabujiaoshi': utils.param('fabujiaoshi',old.fabujiaoshi),
        'xuexibianhao': utils.param('xuexibianhao',old.xuexibianhao),
        'xuexijindu': utils.param('xuexijindu',old.xuexijindu),
        'xueshengyonghu': utils.param('xueshengyonghu',old.xueshengyonghu),
        'xuexizhuangtai': utils.param('xuexizhuangtai',old.xuexizhuangtai),
        'addtime': old.addtime,

    }

    if data['xuexijindu'] == '':
        data['xuexijindu'] = 0
    else:
        data['xuexijindu'] = int(data['xuexijindu'])

    # 判断是否有填写学习编号。
    if not data['xuexibianhao']:
        return R.error("请填写学习编号")



    # 创建课程学习 对象
    model = Kechengxuexi(**data)
    # 执行更新数据
    model.save(force_update = True)


    # 返回更新后的值
    return R.success( model )




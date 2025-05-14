from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# from yuce.recommend import NeuralCollaborativeFiltering, csv_path, model_path, mapping_path
from yuce.updatedata import updateKecheng
from .models import Xuexijindu
from core import utils,DB
import json

from kechengxuexi.models import Kechengxuexi
# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("xuexijindu")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):
    if utils.param("kechengxuexiid"):
        qs = qs.filter(kechengxuexiid=utils.param("kechengxuexiid"))
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
    qs = getWhere(request,Xuexijindu.objects)
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
    qs = getWhere(request,Xuexijindu.objects)

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
    qs = getWhere(request,Xuexijindu.objects)
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
    qs = getWhere(request,Xuexijindu.objects)
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
    mmm = Xuexijindu.objects.get(pk = id)
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
        map = Xuexijindu.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")


# 插入学习进度数据
@router.route('insert/')
def insert(request):
    # 获取提交的数据
    data = {
        'kechengxuexiid': utils.param('kechengxuexiid',0),
        'kechengbianhao': utils.param('kechengbianhao',''),
        'kechengmingcheng': utils.param('kechengmingcheng',''),
        'kechengfenlei': utils.param('kechengfenlei',0),
        'xuexibianhao': utils.param('xuexibianhao',''),
        'fabujiaoshi': utils.param('fabujiaoshi',''),
        'xueshengyonghu': utils.param('xueshengyonghu',''),
        'xuexijindu': utils.param('xuexijindu',''),
        'addtime': utils.getDateStr(),

    }

    if not data['fabujiaoshi']:
        data['fabujiaoshi'] = str(utils.session("username") or "")
    if not data['xueshengyonghu']:
        data['xueshengyonghu'] = str(utils.session("username") or "")
    if not data['xuexijindu']:
        data['xuexijindu'] = "0"
    else:
        data['xuexijindu'] = str(int(data['xuexijindu']))

    # 判断是否有填写学习进度。
    if not data['xuexijindu']:
        return R.error("请填写学习进度")

    # 创建model 对象，然后执行插入
    model = Xuexijindu(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    try:
        DB.execute("UPDATE kechengxuexi SET xuexizhuangtai = '学习中' WHERE id='%s' AND '%s'>0"%(utils.param("kechengxuexiid"),utils.param("xuexijindu"),))
        DB.execute("UPDATE kechengxuexi SET xuexijindu = '%s' WHERE id='%s'"%(utils.param("xuexijindu"),utils.param("kechengxuexiid"),))
        DB.execute("UPDATE kechengxuexi SET xuexizhuangtai = '已完成' WHERE id='%s' AND '%s'=100"%(utils.param("kechengxuexiid"),utils.param("xuexijindu"),))

        updateKecheng()
    except Exception as e:
        print("%s"% (e))

    # 返回插入的数据
    return R.success( model )


# 更新学习进度数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Xuexijindu.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'kechengxuexiid': utils.param('kechengxuexiid',old.kechengxuexiid),
        'kechengbianhao': utils.param('kechengbianhao',old.kechengbianhao),
        'kechengmingcheng': utils.param('kechengmingcheng',old.kechengmingcheng),
        'kechengfenlei': utils.param('kechengfenlei',old.kechengfenlei),
        'xuexibianhao': utils.param('xuexibianhao',old.xuexibianhao),
        'fabujiaoshi': utils.param('fabujiaoshi',old.fabujiaoshi),
        'xueshengyonghu': utils.param('xueshengyonghu',old.xueshengyonghu),
        'xuexijindu': utils.param('xuexijindu',old.xuexijindu),
        'addtime': old.addtime,

    }

    if data['xuexijindu'] == '':
        data['xuexijindu'] = 0
    else:
        data['xuexijindu'] = int(data['xuexijindu'])

    # 判断是否有填写学习进度。
    if not data['xuexijindu']:
        return R.error("请填写学习进度")

    # 创建学习进度 对象
    model = Xuexijindu(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Zuoyepiyue
from core import utils,DB
import json

from tijiaozuoye.models import Tijiaozuoye
# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("zuoyepiyue")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    if utils.param("tijiaozuoyeid"):
        qs = qs.filter(tijiaozuoyeid=utils.param("tijiaozuoyeid"))
    # 判断是否填写课程编号
    if utils.param("kechengbianhao"):
        qs = qs.filter(kechengbianhao__contains=utils.param("kechengbianhao"))
    # 判断是否填写课程名称
    if utils.param("kechengmingcheng"):
        qs = qs.filter(kechengmingcheng__contains=utils.param("kechengmingcheng"))
    # 判断是否选择课程分类
    if utils.param("kechengfenlei"):
        qs = qs.filter(kechengfenlei=utils.param("kechengfenlei"))
    # 判断是否填写作业名称
    if utils.param("zuoyemingcheng"):
        qs = qs.filter(zuoyemingcheng__contains=utils.param("zuoyemingcheng"))
    # 判断是否填写作业附件
    if utils.param("zuoyefujian"):
        qs = qs.filter(zuoyefujian__contains=utils.param("zuoyefujian"))
    # 判断是否填写学生姓名
    if utils.param("xueshengxingming"):
        qs = qs.filter(xueshengxingming__contains=utils.param("xueshengxingming"))
    # 判断是否填写分数的起始值
    if utils.param("fenshu_start"):
        qs = qs.filter(fenshu__gte=utils.param("fenshu_start"))

    # 判断是否填写分数的结束值
    if utils.param("fenshu_end"):
        qs = qs.filter(fenshu__lte=utils.param("fenshu_end"))

    # 判断是否填写评语
    if utils.param("pingyu"):
        qs = qs.filter(pingyu__contains=utils.param("pingyu"))

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
    qs = getWhere(request,Zuoyepiyue.objects)
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
    qs = getWhere(request,Zuoyepiyue.objects)

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
    qs = getWhere(request,Zuoyepiyue.objects)
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
# 提交学生列表页面
@router.route('admin/tijiaoxuesheng/')
def tijiaoxuesheng(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取条件
    qs = getWhere(request,Zuoyepiyue.objects)
    # 设置提交学生值为当前登录用户
    qs = qs.filter(tijiaoxuesheng=utils.session('username'))

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
    mmm = Zuoyepiyue.objects.get(pk = id)
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
        map = Zuoyepiyue.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")







# 插入作业批阅数据
@router.route('insert/')
def insert(request):

    # 获取提交的数据
    data = {
        'tijiaozuoyeid': utils.param('tijiaozuoyeid',0),
        'kechengbianhao': utils.param('kechengbianhao',''),
        'kechengmingcheng': utils.param('kechengmingcheng',''),
        'kechengfenlei': utils.param('kechengfenlei',0),
        'fabujiaoshi': utils.param('fabujiaoshi',''),
        'zuoyemingcheng': utils.param('zuoyemingcheng',''),
        'zuoyefujian': utils.param('zuoyefujian',''),
        'xueshengxingming': utils.param('xueshengxingming',''),
        'tijiaoxuesheng': utils.param('tijiaoxuesheng',''),
        'fenshu': utils.param('fenshu',''),
        'pingyu': utils.param('pingyu',''),
        'addtime': utils.getDateStr(),

    }



    if data['fabujiaoshi'] == '':
        data['fabujiaoshi'] = utils.session( "username")
    if data['tijiaoxuesheng'] == '':
        data['tijiaoxuesheng'] = utils.session( "username")
    if data['fenshu'] == '':
        data['fenshu'] = 0
    else:
        data['fenshu'] = int(data['fenshu'])

    # 判断是否有填写分数。
    if not data['fenshu']:
        return R.error("请填写分数")
    # 判断是否有填写评语。
    if not data['pingyu']:
        return R.error("请填写评语")







    # 创建model 对象，然后执行插入
    model = Zuoyepiyue(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    try:
        DB.execute("UPDATE tijiaozuoye SET zuoyezhuangtai = '已批阅' WHERE id='%s'"%(utils.param("tijiaozuoyeid"),))
    except Exception as e:
        print("%s"% (e))

    # 返回插入的数据
    return R.success( model )

# 更新作业批阅数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Zuoyepiyue.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'tijiaozuoyeid': utils.param('tijiaozuoyeid',old.tijiaozuoyeid),
        'kechengbianhao': utils.param('kechengbianhao',old.kechengbianhao),
        'kechengmingcheng': utils.param('kechengmingcheng',old.kechengmingcheng),
        'kechengfenlei': utils.param('kechengfenlei',old.kechengfenlei),
        'fabujiaoshi': utils.param('fabujiaoshi',old.fabujiaoshi),
        'zuoyemingcheng': utils.param('zuoyemingcheng',old.zuoyemingcheng),
        'zuoyefujian': utils.param('zuoyefujian',old.zuoyefujian),
        'xueshengxingming': utils.param('xueshengxingming',old.xueshengxingming),
        'tijiaoxuesheng': utils.param('tijiaoxuesheng',old.tijiaoxuesheng),
        'fenshu': utils.param('fenshu',old.fenshu),
        'pingyu': utils.param('pingyu',old.pingyu),
        'addtime': old.addtime,

    }

    if data['fenshu'] == '':
        data['fenshu'] = 0
    else:
        data['fenshu'] = int(data['fenshu'])

    # 判断是否有填写分数。
    if not data['fenshu']:
        return R.error("请填写分数")
    # 判断是否有填写评语。
    if not data['pingyu']:
        return R.error("请填写评语")



    # 创建作业批阅 对象
    model = Zuoyepiyue(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




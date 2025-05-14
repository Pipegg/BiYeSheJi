from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Xuesheng
from core import utils,DB
import json

# Create your views here.
from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("xuesheng")

# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):
   # 判断是否填写学号
    if utils.param("xuehao"):
        qs = qs.filter(xuehao__contains=utils.param("xuehao"))
    # 判断是否填写姓名
    if utils.param("xingming"):
        qs = qs.filter(xingming__contains=utils.param("xingming"))
    # 判断是否选择性别
    if utils.param("xingbie"):
        qs = qs.filter(xingbie=utils.param("xingbie"))
    # 判断是否填写手机
    if utils.param("shouji"):
        qs = qs.filter(shouji__contains=utils.param("shouji"))
    # 判断是否填写邮箱
    if utils.param("youxiang"):
        qs = qs.filter(youxiang__contains=utils.param("youxiang"))
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
    qs = getWhere(request,Xuesheng.objects)
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
    qs = getWhere(request,Xuesheng.objects)
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
    mmm = Xuesheng.objects.get(pk = id)
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
        map = Xuesheng.objects.get(pk = id)
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
    map = Xuesheng.objects.get(pk = id)
    # 设置issh 提交的内容
    map.issh = utils.param('value')
    # 更新数据
    map.save(force_update = True)
    # 返回成功的内容
    return R.success(map.issh)

# 插入学生数据
@router.route('insert/')
def insert(request):
    # 获取提交的数据
    data = {
        'xuehao': utils.param('xuehao',''),
        'mima': utils.param('mima',''),
        'xingming': utils.param('xingming',''),
        'xingbie': utils.param('xingbie',''),
        'shouji': utils.param('shouji',''),
        'youxiang': utils.param('youxiang',''),
        'touxiang': utils.param('touxiang',''),
    }

    # 判断是否有填写学号。
    if not data['xuehao']:
        return R.error("请填写学号")
    if len(Xuesheng.objects.filter(xuehao=data['xuehao']).all()):
        return R.error('学号已重复')
    # 判断是否有填写密码。
    if not data['mima']:
        return R.error("请填写密码")
    # 判断是否有填写姓名。
    if not data['xingming']:
        return R.error("请填写姓名")
    # 判断是否有填写性别。
    if not data['xingbie']:
        return R.error("请填写性别")
    # 判断是否有填写手机。
    if not data['shouji']:
        return R.error("请填写手机")
    # 判断是否有填写邮箱。
    if not data['youxiang']:
        return R.error("请填写邮箱")

    # 创建model 对象，然后执行插入
    model = Xuesheng(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    # 返回插入的数据
    return R.success( model )

# 更新学生数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Xuesheng.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'xuehao': utils.param('xuehao',old.xuehao),
        'mima': utils.param('mima',old.mima),
        'xingming': utils.param('xingming',old.xingming),
        'xingbie': utils.param('xingbie',old.xingbie),
        'shouji': utils.param('shouji',old.shouji),
        'youxiang': utils.param('youxiang',old.youxiang),
        'touxiang': utils.param('touxiang',old.touxiang),

    }

    # 判断是否有填写学号。
    if not data['xuehao']:
        return R.error("请填写学号")
    if len(Xuesheng.objects.exclude(id = data['id']).filter(xuehao=data['xuehao']).all()):
        return R.error('学号已重复')
    # 判断是否有填写姓名。
    if not data['xingming']:
        return R.error("请填写姓名")
    # 判断是否有填写性别。
    if not data['xingbie']:
        return R.error("请填写性别")
    # 判断是否有填写手机。
    if not data['shouji']:
        return R.error("请填写手机")
    # 判断是否有填写邮箱。
    if not data['youxiang']:
        return R.error("请填写邮箱")

    # 创建学生 对象
    model = Xuesheng(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )

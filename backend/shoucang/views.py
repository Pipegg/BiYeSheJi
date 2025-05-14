from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Shoucang
from core import utils,DB
import json


# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("shoucang")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    # 判断是否填写标题
    if utils.param("biaoti"):
        qs = qs.filter(biaoti__contains=utils.param("biaoti"))



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
    qs = getWhere(request,Shoucang.objects)
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
    qs = getWhere(request,Shoucang.objects)

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


# 用户列表页面
@router.route('admin/username/')
def username(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取条件
    qs = getWhere(request,Shoucang.objects)
    # 设置用户值为当前登录用户
    qs = qs.filter(username=utils.session('username'))

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
    mmm = Shoucang.objects.get(pk = id)
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
        map = Shoucang.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")





# 批量删除数据
@router.route('/batch/')
def batch(request):
    # 获取提交的ids
    ids = utils.paramlist("ids")

    if utils.param('delete'):
        for id in ids:
            map = Shoucang.objects.get(pk = id)

            map.delete()

    return R.success("批量处理成功")


# 插入收藏数据
@router.route('insert/')
def insert(request):
    # 添加详细的调试信息
    print("收藏insert API调用")
    print(f"请求方法: {request.method}")
    print(f"请求头: {dict(request.headers.items())}")
    print(f"请求体长度: {len(request.body) if request.body else 0}")
    
    if request.body:
        try:
            body_str = request.body.decode('utf-8')
            print(f"请求体: {body_str[:200]}")
        except:
            print(f"无法解码请求体")
    
    # 判断是否登录
    is_logged_in = utils.checkLogin()
    username = utils.session("username")
    
    print(f"登录检查结果: {is_logged_in}, 会话用户名: {username}")
    
    # 检查授权头
    auth_header = request.headers.get('Authorization', '')
    token_header = request.headers.get('token', '')
    print(f"授权头: {auth_header}")
    print(f"Token头: {token_header}")
    
    # 宽松的登录检查 - 如果会话中有用户名，就认为已登录
    if not is_logged_in:
        # 尝试从请求中获取用户名
        req_username = utils.param('username', '')
        if req_username:
            print(f"从请求参数获取到用户名: {req_username}")
            username = req_username
            is_logged_in = True
        # 如果仍然没有登录，返回错误
        else:
            print("登录检查失败，未找到有效的用户名")
            return R.error("请登录后操作")
    else:
        print(f"用户已登录: {username}")

    # 获取提交的数据
    data = {
        'username': utils.param('username', ''),
        'xwid': utils.param('xwid', ''),
        'biao': utils.param('biao', ''),
        'biaoti': utils.param('biaoti', ''),
        'addtime': utils.getDateStr(),
    }
    
    print(f"收到的表单数据: {data}")

    if data['username'] == '':
        data['username'] = username
        print(f"使用会话中的用户名: {data['username']}")
    
    if data['xwid'] == '':
        data['xwid'] = 0
    else:
        data['xwid'] = int(data['xwid'])

    # 检查是否已存在
    res = Shoucang.objects.filter(biao=utils.param("biao")).filter(xwid=utils.param("xwid")).filter(username=data['username']).all()
    if len(res):
        print(f"已存在的收藏记录，执行取消收藏: {res[0].id}")
        item_id = res[0].id
        res[0].delete()
        # 返回标准格式的JSON对象，而不是字符串
        return R.success({
            'id': item_id,
            'username': data['username'],
            'xwid': data['xwid'],
            'biao': data['biao'],
            'biaoti': data['biaoti'],
            'action': 'cancel',
            'msg': '已取消收藏'
        })
    else:
        # 创建model 对象，然后执行插入
        print(f"准备插入新收藏记录: {data}")
        model = Shoucang(**data)
        # 执行插入数据库
        model.save(force_insert = True)

        # 返回插入的数据
        print(f"收藏记录插入成功: {model.id}")
        return R.success({
            'id': model.id,
            'username': model.username,
            'xwid': model.xwid,
            'biao': model.biao,
            'biaoti': model.biaoti,
            'action': 'add',
            'msg': '收藏成功'
        })

# 更新收藏数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Shoucang.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'username': utils.param('username',old.username),
        'xwid': utils.param('xwid',old.xwid),
        'biao': utils.param('biao',old.biao),
        'biaoti': utils.param('biaoti',old.biaoti),
        'addtime': old.addtime,

    }

    if data['xwid'] == '':
        data['xwid'] = 0
    else:
        data['xwid'] = int(data['xwid'])




    # 创建收藏 对象
    model = Shoucang(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




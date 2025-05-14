from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Kechengxinxi
from core import utils,DB
import json


# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("kechengxinxi")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    # 判断是否填写课程编号
    if utils.param("kechengbianhao"):
        qs = qs.filter(kechengbianhao__contains=utils.param("kechengbianhao"))
    # 判断是否填写课程名称
    if utils.param("kechengmingcheng"):
        qs = qs.filter(kechengmingcheng__contains=utils.param("kechengmingcheng"))
    # 判断是否选择课程分类
    if utils.param("kechengfenlei"):
        qs = qs.filter(kechengfenlei=utils.param("kechengfenlei"))

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
    qs = getWhere(request,Kechengxinxi.objects)
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
    qs = getWhere(request,Kechengxinxi.objects)

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
    qs = getWhere(request,Kechengxinxi.objects)
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


# 前台列表页面
@router.route('/index/')
def index(request):

    # 获取前端搜素条件
    qs = getWhere(request,Kechengxinxi.objects)
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
    try:
        # 打印请求信息以便调试
        print("====== FINDBYID DEBUG INFO ======")
        print("REQUEST METHOD:", request.method)
        print("REQUEST PATH:", request.path)
        print("REQUEST GET:", dict(request.GET))
        print("REQUEST POST:", dict(request.POST))
        print("REQUEST HEADERS:", {k: str(v) for k, v in request.headers.items()})
        
        # 获取提交的参数id - 从多个可能的位置尝试获取
        id_from_get = request.GET.get('id')
        id_from_post = request.POST.get('id')
        id_from_param = utils.param("id")
        
        print("ID FROM GET:", id_from_get)
        print("ID FROM POST:", id_from_post)
        print("ID FROM PARAM:", id_from_param)
        
        # 选择一个非空的ID值
        id = id_from_get or id_from_post or id_from_param
        
        print("FINAL ID VALUE:", id)
        
        if not id:
            print("ERROR: ID参数未提供")
            return R.error("参数错误：未提供ID", 400)
            
        # 尝试转换ID为整数
        try:
            id = int(id)
            print("CONVERTED ID:", id)
        except (ValueError, TypeError):
            print("ERROR: ID不是有效整数:", id)
            return R.error("参数错误：ID '{}' 不是有效的整数".format(str(id)), 400)
            
        # 根据id 获取一行数据
        try:
            mmm = Kechengxinxi.objects.get(pk=id)
            print("FOUND MODEL:", getattr(mmm, 'id', '?'), getattr(mmm, 'kechengmingcheng', '?'))
            # 返回成功结果
            return R.success(mmm)
        except Kechengxinxi.DoesNotExist:
            print("ERROR: 未找到课程, ID:", id)
            return R.error("未找到ID为 {} 的课程信息".format(str(id)), 404)
            
    except Exception as e:
        # 记录详细错误
        import traceback
        error_details = traceback.format_exc()
        print("EXCEPTION:", str(e))
        print("TRACEBACK:", error_details)
        
        # 返回友好的错误信息
        return R.error("获取课程信息时发生错误: {}".format(str(e)), 500)




# 打开前台详情页面信息
@router.route('detail/')
def detail(request):
    # 获取提交的参数id
    id = utils.param('id')
    # 根据id 获取一行数据
    map = Kechengxinxi.objects.get(pk=id)


    return R.success("ok")

# 根据数组id 删除数据
@router.route('delete/')
def delete(request):
    # 获取提交body内容，进行json 解析
    ids = json.loads(request.body)
    # 循环删除数据
    for id in ids:
        # 获取一行数据
        map = Kechengxinxi.objects.get(pk = id)

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
    map = Kechengxinxi.objects.get(pk = id)
    # 设置issh 提交的内容
    map.issh = utils.param('value')
    # 更新数据
    map.save(force_update = True)
    # 返回成功的内容
    return R.success(map.issh)

# 获取收藏数据
@router.route('admin/getshoucang')
def getshoucang(request):
    # 添加调试信息
    print("获取收藏状态API调用")
    print("原始请求数据:")
    print("GET参数:", dict(request.GET.items()))
    print("POST参数:", dict(request.POST.items()))
    
    try:
        # 直接读取GET参数和header以排查问题
        raw_id = request.GET.get('id')
        print(f"直接从GET读取的ID: {raw_id}")
        
        # 获取请求参数 - 尝试显式处理None值
        id_param = utils.param('id')
        if not id_param or id_param == 'None':
            # 尝试直接从URL参数获取
            id_param = raw_id
            print(f"从URL直接获取ID: {id_param}")
        
        print(f"最终使用的ID参数: {id_param}")
        
        username = utils.param('username', '')
        
        # 如果没有提供用户名，则从会话中获取
        if not username:
            session_username = utils.session('username')
            if session_username:
                username = str(session_username)
        
        # 打印详细的请求信息
        print(f"请求参数: id={id_param}, 前端提供的用户名: {username}")
        print(f"会话中的用户名: {utils.session('username')}")
        print(f"请求头: {dict(request.headers.items())}")
        
        # 确保ID和用户名是有效的
        if not id_param or id_param == 'None' or id_param == '':
            print("错误: 未提供课程ID")
            return R.error("缺少课程ID参数")
            
        if not username:
            print("警告: 未提供用户名，将返回未收藏状态")
            return R.success({
                'shoucangCount': 0,
                'is_shoucang': False
            })
        
        # 将ID转换为整数以确保类型匹配
        try:
            num_id = int(id_param)
            print(f"已将ID转换为整数: {num_id}")
        except (ValueError, TypeError) as e:
            print(f"警告: ID类型转换失败: {id_param}, 错误: {str(e)}")
            # 使用原始值
            num_id = id_param
        
        # 根据id获取收藏总数 - 使用整数ID
        count = DB.name("shoucang").where("biao", "kechengxinxi").where("xwid", num_id).count()
        
        # 判断是否收藏 - 确保username非空且使用整数ID
        is_val = DB.name("shoucang").where("biao", "kechengxinxi").where("xwid", num_id).where("username", username).count()
        
        # 添加更多的调试信息
        print(f"查询参数: biao=kechengxinxi, xwid={num_id}, username={username}")
        print(f"查询结果: 总收藏数={count}, 当前用户是否收藏={is_val > 0}")
        
        # 确保返回正确的数据类型
        result = {
            'shoucangCount': int(count),
            'is_shoucang': bool(is_val > 0)
        }
        
        print(f"返回数据: {result}")
        
        return R.success(result)
    except Exception as e:
        # 记录错误详情
        import traceback
        error_details = traceback.format_exc()
        print(f"获取收藏状态出错: {str(e)}")
        print(f"错误详情: {error_details}")
        
        # 返回错误响应，但不暴露内部错误详情
        return R.error("获取收藏状态失败，请稍后再试")




# 插入课程信息数据
@router.route('insert/')
def insert(request):

    # 获取提交的数据
    data = {
        'kechengbianhao': utils.param('kechengbianhao',''),
        'kechengmingcheng': utils.param('kechengmingcheng',''),
        'kechengfenlei': utils.param('kechengfenlei',0),
        'kechengfengmian': utils.param('kechengfengmian',''),
        'kechengyaodian': utils.param('kechengyaodian',''),
        'fabujiaoshi': utils.param('fabujiaoshi',''),
        'kechengxiangqing': utils.param('kechengxiangqing',''),
        'addtime': utils.getDateStr(),

    }



    if data['fabujiaoshi'] == '':
        data['fabujiaoshi'] = utils.session( "username")

    # 判断是否有填写课程编号。
    if not data['kechengbianhao']:
        return R.error("请填写课程编号")
    # 判断是否有填写课程名称。
    if not data['kechengmingcheng']:
        return R.error("请填写课程名称")
    # 判断是否有填写课程分类。
    if not data['kechengfenlei']:
        return R.error("请填写课程分类")
    # 判断是否有填写课程封面。
    if not data['kechengfengmian']:
        return R.error("请填写课程封面")
    # 判断是否有填写课程要点。
    if not data['kechengyaodian']:
        return R.error("请填写课程要点")







    # 创建model 对象，然后执行插入
    model = Kechengxinxi(**data)
    # 执行插入数据库
    model.save(force_insert = True)

    # 返回插入的数据
    return R.success( model )

# 更新课程信息数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Kechengxinxi.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'kechengbianhao': utils.param('kechengbianhao',old.kechengbianhao),
        'kechengmingcheng': utils.param('kechengmingcheng',old.kechengmingcheng),
        'kechengfenlei': utils.param('kechengfenlei',old.kechengfenlei),
        'kechengfengmian': utils.param('kechengfengmian',old.kechengfengmian),
        'kechengyaodian': utils.param('kechengyaodian',old.kechengyaodian),
        'fabujiaoshi': utils.param('fabujiaoshi',old.fabujiaoshi),
        'kechengxiangqing': utils.param('kechengxiangqing',old.kechengxiangqing),
        'addtime': old.addtime,

    }


    # 判断是否有填写课程编号。
    if not data['kechengbianhao']:
        return R.error("请填写课程编号")
    # 判断是否有填写课程名称。
    if not data['kechengmingcheng']:
        return R.error("请填写课程名称")
    # 判断是否有填写课程分类。
    if not data['kechengfenlei']:
        return R.error("请填写课程分类")
    # 判断是否有填写课程封面。
    if not data['kechengfengmian']:
        return R.error("请填写课程封面")
    # 判断是否有填写课程要点。
    if not data['kechengyaodian']:
        return R.error("请填写课程要点")



    # 创建课程信息 对象
    model = Kechengxinxi(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




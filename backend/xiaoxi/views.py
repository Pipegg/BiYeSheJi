from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Xiaoxi
from core import utils,DB
import json

from siliao.models import Siliao
# Create your views here.

from core import Blueprint,R

# 创建路由装饰器
router=Blueprint("xiaoxi")


# 根据前台填写的搜素条件，设置相关搜素
def getWhere(request,qs):



    if utils.param("siliaoid"):
        qs = qs.filter(siliaoid=utils.param("siliaoid"))



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
    qs = getWhere(request,Xiaoxi.objects)
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
    qs = getWhere(request,Xiaoxi.objects)

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


# 发送人列表页面
@router.route('admin/fasongren/')
def fasongren(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
    # 获取条件
    qs = getWhere(request,Xiaoxi.objects)
    # 设置发送人值为当前登录用户
    qs = qs.filter(fasongren=utils.session('username'))

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
    mmm = Xiaoxi.objects.get(pk = id)
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
        map = Xiaoxi.objects.get(pk = id)

        # 执行删除
        map.delete()

    # 提示删除成功
    return R.success("删除成功")







# 插入消息数据
@router.route('insert/')
def insert(request):
    try:
        print("==== 消息插入请求开始 ====")
        print(f"请求方法: {request.method}")
        print(f"请求内容类型: {request.content_type}")
        
        # 打印请求参数
        if request.method == 'POST':
            print("POST参数:", dict(request.POST))
        if request.method == 'GET':
            print("GET参数:", dict(request.GET))
            
        # 尝试解析请求体
        try:
            if request.body:
                print(f"请求体: {request.body.decode('utf-8')[:200]}")
                if 'application/json' in request.content_type:
                    import json
                    body_data = json.loads(request.body)
                    print(f"JSON数据: {body_data}")
        except Exception as e:
            print(f"解析请求体错误: {e}")
        
        # 使用utils.param获取参数
        siliaoid = utils.param('siliaoid', 0)
        bianhao = utils.param('bianhao', '')
        neirong = utils.param('neirong', '')
        fasongren = utils.param('fasongren', '')
        fasongshijian = utils.param('fasongshijian', '')
        shifouzhakan = utils.param('shifouzhakan', '')
        
        print(f"获取的参数: siliaoid={siliaoid}, bianhao={bianhao}, neirong={neirong[:50] if neirong else ''}...")
        print(f"fasongren={fasongren}, fasongshijian={fasongshijian}, shifouzhakan={shifouzhakan}")
        
        # 获取提交的数据
        data = {
            'siliaoid': siliaoid,
            'bianhao': bianhao or '',
            'neirong': neirong or '',
            'fasongren': fasongren or '',
            'fasongshijian': fasongshijian or '',
            'shifouzhakan': shifouzhakan or '',
        }

        # 如果没有发送人，使用当前登录用户
        if not data['fasongren']:
            data['fasongren'] = utils.session("username") or ''
            print(f"使用会话用户名作为发送人: {data['fasongren']}")

        # 判断是否有填写发送时间
        if not data['fasongshijian']:
            print("错误: 缺少发送时间")
            return R.error("请填写发送时间")
            
        # 验证siliaoid是否有效
        if not data['siliaoid']:
            print("错误: 缺少siliaoid")
            return R.error("缺少会话ID")

        # 创建model对象，然后执行插入
        print("创建消息对象准备插入")
        model = Xiaoxi(**data)
        model.save(force_insert=True)
        print(f"消息插入成功，ID: {model.pk}")

        # 更新siliao表的addtime字段
        try:
            siliao_id = str(data['siliaoid'])
            DB.execute(f"UPDATE siliao SET addtime=now() WHERE id='{siliao_id}'")
            print(f"更新siliao表的addtime字段成功, siliaoid={siliao_id}")
        except Exception as e:
            print(f"更新siliao表addtime时出错: {e}")

        # 返回插入的数据
        print("==== 消息插入请求完成 ====")
        return R.success(model)
        
    except Exception as e:
        import traceback
        print(f"消息插入异常: {e}")
        print(f"异常详情: {traceback.format_exc()}")
        return R.error(f"消息发送失败: {str(e)}")

# 更新消息数据
@router.route('update/')
def update(request):
    # 获取id值
    charuid = utils.param('id')
    # 获取原有数据
    old = Xiaoxi.objects.get(pk = charuid)
    # 更新的数据
    data = {
        'id': charuid,
        'siliaoid': utils.param('siliaoid',old.siliaoid),
        'bianhao': utils.param('bianhao',old.bianhao),
        'neirong': utils.param('neirong',old.neirong),
        'fasongren': utils.param('fasongren',old.fasongren),
        'fasongshijian': utils.param('fasongshijian',old.fasongshijian),
        'shifouzhakan': utils.param('shifouzhakan',old.shifouzhakan),

    }


    # 判断是否有填写发送时间。
    if not data['fasongshijian']:
        return R.error("请填写发送时间")


    # 创建消息 对象
    model = Xiaoxi(**data)
    # 执行更新数据
    model.save(force_update = True)

    # 返回更新后的值
    return R.success( model )




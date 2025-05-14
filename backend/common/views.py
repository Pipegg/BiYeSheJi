from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from core import request,utils,DB

# Create your views here.
from core import Blueprint, R
import json

# 创建访问路由
router = Blueprint("commons")

# from yuce.recommend import NeuralCollaborativeFiltering,model_path,mapping_path,csv_path
from yuce.updatedata import updateKecheng
@router.route('/filter')
def filter(request:HttpRequest):
    if "学生" == utils.session('cx'):
        # 假设直接调用 yuce.views.recommend_courses 逻辑，或通过 HTTP 请求
        # 这里以 HTTP 请求为例（如有更优方式可替换）
        import requests as pyrequests
        try:
            # 假设本地服务端口为8006，token等信息可从 session 获取
            token = utils.session('token') if hasattr(utils, 'session') else None
            headers = {'Authorization': f'Bearer {token}'} if token else {}
            resp = pyrequests.get('http://127.0.0.1:8006/yuce/recommend_courses', headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('code') == 0 and data.get('data'):
                    # 推荐课程ID列表
                    course_ids = [c['course_id'] for c in data['data'] if 'course_id' in c]
                    if course_ids:
                        where = " 1=1 and id IN(" + (','.join([str(c) for c in course_ids])) + ") "
                        lists = DB.name("kechengxinxi").where(where).order("rand()").limit(8).select()
                        return R.success(lists)
        except Exception as e:
            print(e)
    # 非学生或无推荐，返回随机课程
    lists = DB.name("kechengxinxi").order("rand()").limit(8).select()
    return R.success(lists)


@router.route('/xunlian')
def xuanlian(request):
    updateKecheng()
    return R.success("数据更新完成")


# 系统登录
@router.route("/login/")
def login(request):
    # 获取用户名
    username = utils.param('username')
    # 获取密码
    password = utils.param('pwd')
    # 获取登录角色
    cx       = utils.param('cx')


    if "a" in request.GET:
        # 获取填写的验证码
        pagerandom = utils.param('pagerandom')
        # 使用jwt token 对用户提交的验证码数据进行解密,得出系统生成的值,在对比填写的值是否正确
        captcha = R.jwtDecode(utils.param('captchToken'))
        # 未填写验证码
        if not pagerandom:
            return R.error( "请填写验证码")
        # 验证码不正确
        if pagerandom != captcha:
            return R.error( "验证码错误")
    # 未填写账号
    if not username:
        return R.error("请填写账号")
    # 未填写密码
    if not password:
        return R.error("请填写密码")
    # 未选择登录角色
    if not cx:
        return R.error("请选择相应角色")
    qs = None
    issh = False
    table = ''

    if cx == '管理员':
        from admins.models import Admins
        table = 'admins'
        
        # 设置账号、和密码的条件
        qs = Admins.objects.filter(username=username , pwd=password)
    if cx == '学生':
        from xuesheng.models import Xuesheng
        table = 'xuesheng'
        
        # 设置账号、和密码的条件
        qs = Xuesheng.objects.filter(xuehao=username , mima=password)
        issh=True
    if cx == '教师':
        from jiaoshi.models import Jiaoshi
        table = 'jiaoshi'
        
        # 设置账号、和密码的条件
        qs = Jiaoshi.objects.filter(gonghao=username , mima=password)

    # 没有找到qs，则无法登录
    if qs is None:
        return R.error('没有找到相关角色')

    # 获取数据
    list = qs.values()

    # 没有数据，则表示账号和密码错误
    if not list:
        return R.error("账号或密码错误")


    user = list[0]
    if issh and user['issh'] != '是':
        return R.error('账号审核中')

    # 设置session 数据
    session = {
        'table': table,
        'cx': cx,
        'roles': cx,
        'id': user['id'],
        'username': username,
    }
    if 'cx' in user:
        session['cx'] = user['cx']
    # 根据session 数据进行jwt token 对数据进行加密
    token = R.jwtEncode(session,  86400*7)
    # 将用户数据写入session 中
    session['object'] = user

    # 返回session数据和token
    return R.success({
        'session': session,
        'token': token
    })

def add_cors_headers(response):
    # 支持所有跨域请求
    response["Access-Control-Allow-Origin"] = "*"
    # 允许的请求方法
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    # 允许的请求头
    response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With, token, Accept, Origin"
    # 允许凭证信息
    response["Access-Control-Allow-Credentials"] = "true"
    # 预检请求的缓存时间
    response["Access-Control-Max-Age"] = "3600"
    return response

def get_token(request):
    return request.GET.get('token') or request.POST.get('token')

def check_token(func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return add_cors_headers(HttpResponse())
            
        token = get_token(request)
        if not token:
            response = R.error('未登录')
            return add_cors_headers(response)
            
        result = R.jwtDecode(token)
        if not result:
            response = R.error('登录已过期')
            return add_cors_headers(response)
            
        request.user = result
        response = func(request, *args, **kwargs)
        return add_cors_headers(response)
    return wrapper

@router.route('/query')
def query(request:HttpRequest):
    print('请求方法', request.method)
    print('请求 CONTENT_TYPE:', request.META.get('CONTENT_TYPE'))
    print('请求 Content-Type:', request.headers.get('Content-Type'))
    print('请求 Content-Length:', request.headers.get('Content-Length'))
    print('请求 Headers:', {k: v for k, v in request.META.items() if k.startswith('HTTP_')})
    print('请求体原始数据长度:', len(request.body))
    print('请求体原始数据:', request.body)
    print('queryname', request.POST.get('name'))  
    
    if request.method == 'OPTIONS':
        response = HttpResponse()
        return add_cors_headers(response)
    try:
        if request.method == 'POST':
            content_type = request.headers.get('Content-Type', '')
            print('Content-Type:', content_type)
            
            # 初始化数据
            data = None
            
            # 优先级1: 尝试从 POST 数据中获取 json_data 字段
            json_data = request.POST.get('json_data')
            if json_data:
                print('找到 json_data 字段:', json_data)
                try:
                    data = json.loads(json_data)
                    print('成功解析 json_data:', data)
                    print('json_data 类型:', type(data))
                except json.JSONDecodeError as e:
                    print('json_data 解析错误:', str(e))
            
            # 优先级2: 尝试直接使用 POST 数据 (FormData格式)
            if not data and request.POST:
                print('使用 FormData POST 数据')
                data = request.POST
                print('FormData:', data)
            
            # 优先级3: 尝试直接从请求体读取原始数据 (JSON格式)
            if not data:
                try:
                    raw_data = request.body
                    print('原始请求体:', raw_data)
                    
                    if raw_data:
                        try:
                            data = json.loads(raw_data)
                            print('成功解析 JSON 数据:', data)
                            print('data 类型:', type(data))
                            print('data 是否有 name 属性:', 'name' in data)
                            if 'name' in data:
                                print('name 值:', data['name'])
                        except json.JSONDecodeError as e:
                            print('JSON 解析错误:', str(e))
                except Exception as e:
                    print('读取请求体出错:', str(e))
            
            # 优先级4: 最后尝试 GET 参数
            if not data:
                print('所有POST获取方式失败，尝试GET参数')
                data = request.GET
        else:
            data = request.GET
            print('收到/query参数（GET）:', data)
            
        # 如果所有方法都失败，尝试从 URL 获取参数
        if not data:
            print('所有方法获取数据都失败，尝试从 URL 参数获取')
            data = request.GET
        
        print('最终使用的数据:', data)
        
        if not isinstance(data, dict):
            print('数据不是字典类型，尝试转换')
            try:
                if hasattr(data, 'dict'):
                    data = data.dict()
                    print('转换后的数据:', data)
            except:
                print('转换失败')
        
        # 处理特殊参数：尝试解析字符串化的 JSON
        try:
            # 处理 where 参数
            where_value = data.get('where', '')
            if isinstance(where_value, str) and where_value.startswith('['):
                try:
                    data['where'] = json.loads(where_value)
                    print('解析 where JSON 成功:', data['where'])
                except:
                    print('解析 where JSON 失败')
            
            # 处理 order 参数
            order_value = data.get('order', '')
            if isinstance(order_value, str) and order_value.startswith('['):
                try:
                    data['order'] = json.loads(order_value)
                    print('解析 order JSON 成功:', data['order'])
                except:
                    print('解析 order JSON 失败')
            
            # 处理 limit 参数
            limit_value = data.get('limit', '')
            if isinstance(limit_value, str) and limit_value.startswith('{'): 
                try:
                    data['limit'] = json.loads(limit_value)
                    print('解析 limit JSON 成功:', data['limit'])
                except:
                    print('解析 limit JSON 失败')
        except Exception as e:
            print('处理特殊参数出错:', str(e))
        
        # 获取表名，确保是字符串
        table_name = data.get('name', '')
        if not isinstance(table_name, str):
            table_name = str(table_name)
        print('获取到的表名:', table_name)
        print('表名类型:', type(table_name))
        
        if not table_name:
            print('表名为空，返回错误')
            return add_cors_headers(R.error('缺少表名参数'))
            
        # 获取函数名，确保是字符串
        func_name = data.get('func', 'select')
        if not isinstance(func_name, str):
            func_name = str(func_name)
        if not hasattr(DB.name(table_name), func_name):
            return add_cors_headers(R.error(f'不支持的操作: {func_name}'))
        
        db = DB.name(table_name)
        where = data.get('where', '')
        if where:
            # Fix the error with direct insertion of Python dictionaries into SQL
            if isinstance(where, list):
                # Process each condition in the where list
                for condition in where:
                    if isinstance(condition, dict):
                        field_name = condition.get('name', '')
                        operator = condition.get('exp', '=')
                        value = condition.get('value', '')
                        
                        if field_name:  # Only add if field_name is not empty
                            db = db.where(field_name, operator, value)
            else:
                # If it's not a list, pass it directly
                db = db.where(where)
        
        order = data.get('order')
        if order:
            print('order 参数:', order, type(order))
            if isinstance(order, list):
                order = ','.join(order)
                print('拼接后的 order:', order)
            db = db.order(order)
        
        try:
            # 检查 limit 是否为字典格式
            limit_param = data.get('limit', {})
            print('limit 参数原始值:', limit_param, type(limit_param))
            
            # 如果是空字符串或 'null'，设置默认值
            if limit_param == '' or limit_param == 'null':
                limit_param = {}
                print('limit 参数为空，使用默认值')
            
            # 尝试解析 JSON 字符串（如果尚未解析）
            if isinstance(limit_param, str) and (limit_param.startswith('{') or limit_param.startswith('[')):
                try:
                    limit_param = json.loads(limit_param)
                    print('手动解析 limit JSON 成功:', limit_param)
                except Exception as e:
                    print(f'手动解析 limit JSON 失败: {str(e)}')
                    limit_param = {}
            
            print('处理后的 limit 参数:', limit_param, type(limit_param))
            
            # 处理分页参数
            if isinstance(limit_param, dict) and 'size' in limit_param:
                # 如果是字典格式，直接使用 size 和 offset
                try:
                    size = int(limit_param.get('size', 10))
                    offset = int(limit_param.get('offset', 0))
                    print(f'从字典中获取 size={size}, offset={offset}')
                    
                    if offset > 0:
                        db = db.limit(f"{offset},{size}")
                    else:
                        db = db.limit(size)
                    
                    page = offset // size + 1 if size > 0 else 1
                    limit = size
                except (ValueError, TypeError) as e:
                    print(f'处理字典格式 limit 参数出错: {str(e)}')
                    page = 1
                    limit = 10
                    db = db.limit(limit)
            else:
                # 使用传统的 page 和 limit 参数
                try:
                    page_value = data.get('page', 1)
                    limit_value = data.get('limit', 10)
                    
                    # 确保是整数
                    page = int(str(page_value)) if page_value is not None else 1
                    limit = int(str(limit_value)) if limit_value is not None else 10
                    
                    print(f'使用传统分页参数 page={page}, limit={limit}')
                    
                    if page > 1:
                        offset = (page - 1) * limit
                        db = db.limit(f"{offset},{limit}")
                    else:
                        db = db.limit(limit)
                except (ValueError, TypeError) as e:
                    print(f'处理传统分页参数出错: {str(e)}')
                    page = 1
                    limit = 10
                    db = db.limit(limit)
        except Exception as e:
            print(f'整体分页处理出错: {str(e)}')
            return add_cors_headers(R.error(f'分页参数无效: {str(e)}'))
        
        method = getattr(db, func_name)
        result = method()
        total = 0
        try:
            total_db = DB.name(table_name)
            if where:
                # Apply the same where clause processing here for consistency
                if isinstance(where, list):
                    for condition in where:
                        if isinstance(condition, dict):
                            field_name = condition.get('name', '')
                            operator = condition.get('exp', '=')
                            value = condition.get('value', '')
                            
                            if field_name:  # Only add if field_name is not empty
                                total_db = total_db.where(field_name, operator, value)
                else:
                    total_db = total_db.where(where)
            total = total_db.count()
        except Exception as count_error:
            print(f"Error getting count: {str(count_error)}")
            total = len(result or [])
        return add_cors_headers(R.success({
            'data': result or [],
            'total': total,
            'page': page,
            'limit': limit
        }))
    except Exception as e:
        import traceback
        print('Query error:', str(e))
        print('Error traceback:', traceback.format_exc())
        return add_cors_headers(R.error(f'数据库查询失败: {str(e)}'))

@router.route('/tokenLogin/')
def token_login(request):
    # 处理OPTIONS预检请求
    if request.method == 'OPTIONS':
        response = HttpResponse()
        return add_cors_headers(response)
        
    response = None
    try:
        # 优先从请求头获取token
        token = request.headers.get('token')
        if not token:
            # 如果请求头没有，则尝试从GET参数获取
            token = request.GET.get('token')
            
        if not token:
            print("No token provided")
            response = R.error('请提供token')
        else:
            print(f"Attempting to decode token: {token[:10]}...")
            result = R.jwtDecode(token)
            if result:
                print(f"Token decoded successfully for user: {result.get('username')}")
                try:
                    user = DB.name(result['table']).find(result['id'])
                    if user:
                        print(f"User found: {user.get('username')}")
                        # 生成新token
                        new_token = R.jwtEncode(result, 86400*7)
                        result['object'] = user
                        response = R.success({
                            'session': result,
                            'token': new_token
                        })
                    else:
                        print("User not found in database")
                        response = R.error('用户不存在')
                except Exception as e:
                    print(f"Database error: {str(e)}")
                    response = R.error('数据库查询失败')
            else:
                print("Token decode failed")
                response = R.error('token无效')
    except Exception as e:
        print(f'Token login error: {str(e)}')
        response = R.error("登录失败")
        
    return add_cors_headers(response or R.error("未知错误"))

# 生成验证码
@router.route("captch/")
def captcha(request):
    try:
        from .captch import create_validate_code
        img, strs = create_validate_code(size=(120, 30))
        from io import BytesIO
        f = BytesIO()
        img.save(f, "png")
        data = f.getvalue()
        print("验证码值：%s" % (strs,))
        
        import base64
        basestr = base64.b64encode(data).decode('utf-8')
        baseData = "data:image/png;base64,{}".format(basestr)
        token = R.jwtEncode(strs, 500)
        
        response_data = {
            'token': token,
            'url': baseData
        }
        
        return R.success(response_data)
    except Exception as e:
        import traceback
        print("验证码生成失败:", str(e))
        print(traceback.format_exc())
        return R.error("验证码生成失败: " + str(e))

# 前端点击退出登录后执行，后端可以执行一些相关操作
@router.route("logout/")
def logout(request):
    return R.success('ok')

# 修改密码
@router.route("/mod/")
def mod(request):
    # 判断是否登录
    if not utils.checkLogin():
        return R.error("请登录后操作",1001)
		
    # 获取原密码
    oldPwd = utils.param("oldPassword" , "")
    # 获取新密码
    newPwd = utils.param("newPassword" , "")
    # 获取确认密码
    newPwd2 = utils.param("confirmPassword" , "")

    # 判断原密码、新密码、确认密码是否填写，只要有一个没填，则提示填写
    if not all([oldPwd,newPwd2,newPwd]):
        return R.error("请填写原密码或新密码或确认密码")

    # 比较新密码和确认密码是否一致
    if newPwd != newPwd2:
        return R.error( "两次输入密码错误")

    # 获取操作值
    cx  = utils.session("roles")
    # 获取账号
    username = utils.session("username")
    qs = None
    mimafield = ''

    if cx == '管理员':
        from admins.models import Admins
                
        qs = Admins.objects.filter(username=username , pwd=oldPwd)
        mimafield = 'pwd'
    if cx == '学生':
        from xuesheng.models import Xuesheng
                
        qs = Xuesheng.objects.filter(xuehao=username , mima=oldPwd)
        mimafield = 'mima'
    if cx == '教师':
        from jiaoshi.models import Jiaoshi
                
        qs = Jiaoshi.objects.filter(gonghao=username , mima=oldPwd)
        mimafield = 'mima'

    # 没有这个角色
    if qs is None:
        return R.error( "没有该用户")

    # 获取数据
    values = qs.all()
    # 没有数据的话则代表密码错误
    if not len(values):
        return R.error( "原密码错误")

    # 根据参数设置新密码
    user = values[0]
    # 设置密码属性的值
    setattr(user , mimafield , newPwd)
    # 保存
    user.save()
    return R.success("密码修改成功")




# 检测账号是否重复
@router.route('/checkon')
def checkon(request):
    # 检测表
    table = utils.input('table')
    # 检测列
    col = utils.input('col')
    # 检测类型
    checktype = utils.input('checktype')
    # 获取列的值
    val = utils.input(col)
    # 获取数据
    qs = DB.name(table).where(col,val)
    if checktype == 'update':
        id = utils.input('id')
        qs.where('id' , 'neq',id)
    # 数据行数
    count = qs.count()
    # 行数大于0 的话则已存在
    if count:
        return HttpResponse('false')
    else:
        # 数据不存在
        return HttpResponse('true')

# 获取文件的md5 值
import os,hashlib
def get_file_md5(file):
    f_md5 = hashlib.md5(file.read())
    return f_md5.hexdigest()

# 保存上传的文件
def save_upload_file(PostFile, FilePath):
    try:
        # 打开文件
        f = open(FilePath, 'wb')
        # 获取文件数据
        for chunk in PostFile.chunks():
            # 将数据写入目标文件
            f.write(chunk)
    except Exception as E:
        # 写入出错
        f.close()
        # 返回报错信息
        return u"写入文件错误: {}".format(str(E))
    f.close()
    # 返回成功
    return u"SUCCESS"

# 上传文件
@router.route('/upload/')
def upload(request:HttpRequest):
    # 获取上传的附件
    file = request.FILES.get('fujian')
    # 设置状态
    state = "SUCCESS"
    # 文件不存在则报上传错误
    if file is None:
        return R.error("上传错误")

    # 设置文件保存路径 为 根目录\static\
    BASE_DIR = os.path.abspath('static')
    # 在设置文件保存路径为： 根目录\static\upload\
    BASE_DIR = BASE_DIR + "/upload/"
    # 判断文件夹是否存在，不存在则创建目录
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    # 获取文件长度
    size = file.size
    # 将文件名称分成 名称和后缀
    name, ext = os.path.splitext(file.name)
    # 获取文件流
    stream = file.file
    # 根据文件流 获取md5值
    md5 = get_file_md5(stream)
    # 设置回文件的初始位置
    stream.seek(0)
    if state == 'SUCCESS':
        # 保存文件到"文件保存路径"中
        state = save_upload_file(file,BASE_DIR+md5+ext)
    # 保存时出错了，则返回错误
    if state != 'SUCCESS':
        return R.error(state)

    # 返回文件保存的路径
    return R.success('/static/upload/'+md5+ext)

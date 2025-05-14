from django.views.decorators.http import require_POST
from core.query import DB
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import ChatHistory
from LLMs.model_service import ModelService

from core import Blueprint, R, utils as Info

router = Blueprint("commons")

model_service = ModelService()


@router.route('check/')
def check(request):
    req = json.loads(request.body)
    sid = req.get("sid")
    rid = req.get("rid")

    if not sid or not rid:
        return R.error("参数缺失")

    if sid == rid:
        return R.error("不允许和自己聊天")

    u = get_user(rid)
    if not u:
        return R.error("收信人错误")

    siliao = (DB.name("Siliao")
              .where(f"(faxinren = '{sid}' AND shouxinren='{rid}') OR (faxinren = '{rid}' AND shouxinren='{sid}')")
              .find()
              )
    if not siliao:
        siliao = {
            "faxinren": sid,
            "shouxinren": rid,
            "bianhao": Info.getID(),
            "addtime": Info.getDateStr()
        }
        siliao['id'] = DB.name("Siliao").insert(siliao)

    return R.success(siliao)


def get_user(u):
    """
    通过用户名查找用户信息
    :param u: 用户名/学号/工号
    :return: 用户信息字典或None
    """
    if not u:
        print(f"Warning: Empty username passed to get_user")
        return None
        
    try:
        # 先检查学生表
        user = DB.name("xuesheng").where("xuehao", u).find()
        if user:
            print(f"Found student user: {u}")
            return user
            
        # 再检查教师表
        user = DB.name("jiaoshi").where("gonghao", u).find()
        if user:
            print(f"Found teacher user: {u}")
            return user
            
        print(f"User not found: {u}")
        return None
    except Exception as e:
        print(f"Error in get_user({u}): {e}")
        return None


@csrf_exempt
@require_POST
@router.route('sessionList/')
def session_list(request):
    """处理获取聊天会话列表的请求"""
    try:
        print("Session list API called")
        print(f"Request method: {request.method}")
        print(f"Headers: {dict(request.headers.items())}")
        
        # 尝试多种方式获取请求参数
        req = {}
        
        # 先尝试解析请求体为JSON
        if request.body:
            print(f"Request body exists, length: {len(request.body)}")
            try:
                body_str = request.body.decode('utf-8')
                print(f"Request body: {body_str[:200]}")
                req = json.loads(body_str)
                print(f"Parsed JSON: {req}")
            except Exception as e:
                print(f"Error parsing JSON body: {e}")
                
                # 如果JSON解析失败，尝试作为表单处理
                if hasattr(request, 'POST') and request.POST:
                    req = request.POST.dict()
                    print(f"Using POST form data: {req}")
        
        # 如果仍然没有数据，尝试从查询参数获取
        if not req and hasattr(request, 'GET') and request.GET:
            req = request.GET.dict()
            print(f"Using GET parameters: {req}")
        
        # 如果仍然没有数据，尝试显式解析请求体
        if not req and request.body:
            try:
                # 尝试使用urlparse解析
                from urllib.parse import parse_qs
                body_str = request.body.decode('utf-8')
                parsed = parse_qs(body_str)
                req = {k: v[0] for k, v in parsed.items()}
                print(f"Using URL-decoded parameters: {req}")
            except Exception as parse_error:
                print(f"Error parsing request body as URL-encoded: {parse_error}")
        
        # 最后检查是否有数据
        if not req:
            # 错误，但返回空结果而不是错误
            print("No valid request data found")
            return R.success([])
        
        # 获取参数
        sid = req.get("sid")
        if not sid:
            print("Missing required parameter: sid")
            return R.error("用户ID不能为空")
        
        type = req.get("type", "one")
        lastdate = req.get("lastdate", "")
        
        print(f"Processing request with: sid={sid}, type={type}, lastdate={lastdate}")
        
        # 查询数据库
        try:
            list = []
            if type == "one":
                list = DB.name("Siliao").where(f"(faxinren = '{sid}' OR shouxinren='{sid}')").order("addtime desc").select()
                print(f"Found {len(list)} conversations for user {sid}")
            elif type == "new":
                # 确保lastdate有值
                if not lastdate:
                    lastdate = "1970-01-01 00:00:00"
                list = DB.name("Siliao") \
                    .where(f"(faxinren = '{sid}' OR shouxinren='{sid}')") \
                    .where("addtime", ">", lastdate) \
                    .order("addtime asc") \
                    .select()
                print(f"Found {len(list)} new conversations for user {sid} since {lastdate}")
            
            # 如果没有结果，返回空列表
            if not list:
                return R.success([])
            
            # 处理每个会话
            result = []
            for item in list:
                try:
                    # 获取对话的另一方用户
                    other_user_id = item.get("shouxinren" if sid == item.get("faxinren") else "faxinren")
                    current_user_id = item.get("faxinren" if sid == item.get("faxinren") else "shouxinren")
                    
                    # 获取用户信息
                    user_info = get_user(other_user_id)
                    current_user_info = get_user(current_user_id)
                    
                    if user_info and current_user_info:
                        # 添加用户信息
                        item["user"] = user_info
                        item["sender"] = current_user_info
                        
                        # 获取未读消息数
                        try:
                            read_count = DB.name("Xiaoxi").where("siliaoid", item.get("id")) \
                                .where("fasongren", "!=", sid) \
                                .where("shifouzhakan", "否").count()
                            item["readCount"] = read_count
                        except:
                            item["readCount"] = 0
                        
                        # 获取最后一条消息
                        try:
                            last_msg = DB.name("Xiaoxi").where("siliaoid", item.get("id")).order("id desc").limit(1).find()
                            item["last"] = last_msg
                        except:
                            item["last"] = None
                        
                        # 添加到结果
                        result.append(item)
                except Exception as conv_error:
                    print(f"Error processing conversation {item.get('id')}: {conv_error}")
            
            print(f"Returning {len(result)} processed conversations")
            return R.success(result)
            
        except Exception as db_error:
            print(f"Database error: {db_error}")
            import traceback
            print(traceback.format_exc())
            return R.error(f"数据库查询错误: {str(db_error)}")
            
    except Exception as e:
        import traceback
        print(f"Unhandled exception in session_list: {e}")
        print(traceback.format_exc())
        return R.error(f"处理请求失败: {str(e)}")


@csrf_exempt
@require_POST
@router.route('updateRead')
def update_read(request):
    try:
        # 添加详细日志
        print("updateRead API called")
        print(f"Request method: {request.method}")
        print(f"Content-Type: {request.headers.get('Content-Type', 'unknown')}")
        print(f"Request body raw length: {len(request.body) if request.body else 0}")
        
        req = {}
        body_str = ""
        
        # 先尝试解析请求体为JSON
        if request.body:
            try:
                body_str = request.body.decode('utf-8')
                print(f"Request body: {body_str[:200]}")
                req = json.loads(body_str)
                print(f"Parsed JSON: {req}")
            except Exception as e:
                print(f"Error parsing JSON body: {e}")
                # 尝试其他解析方式
        
        # 如果JSON解析失败，尝试作为表单处理
        if not req and hasattr(request, 'POST') and request.POST:
            req = request.POST.dict()
            print(f"Using POST form data: {req}")
        
        # 如果仍然没有数据，尝试从查询参数获取
        if not req and hasattr(request, 'GET') and request.GET:
            req = request.GET.dict()
            print(f"Using GET parameters: {req}")
            
        # 如果仍然没有数据，尝试通过URL编码解析
        if not req and body_str:
            try:
                from urllib.parse import parse_qs
                parsed = parse_qs(body_str)
                req = {k: v[0] for k, v in parsed.items()}
                print(f"Using URL-decoded parameters: {req}")
            except Exception as parse_error:
                print(f"Error parsing request body as URL-encoded: {parse_error}")
        
        # 获取参数，从多个可能的源尝试
        chatid = None
        sid = None
        
        # 从解析的数据中获取参数
        if req:
            chatid = req.get("chatid")
            sid = req.get("sid")
        
        # 如果原始请求体中包含这些关键字，尝试直接提取
        if not chatid and 'chatid' in body_str:
            import re
            match = re.search(r'"chatid"\s*:\s*"?([^",]+)"?', body_str)
            if match:
                chatid = match.group(1)
                print(f"Extracted chatid from raw body: {chatid}")
                
        if not sid and 'sid' in body_str:
            import re
            match = re.search(r'"sid"\s*:\s*"?([^",]+)"?', body_str)
            if match:
                sid = match.group(1)
                print(f"Extracted sid from raw body: {sid}")
        
        # 验证参数
        if not chatid or not sid:
            print(f"Missing or invalid parameters: chatid={chatid}, sid={sid}")
            return R.error("参数不完整")
        
        # 执行更新操作
        try:
            print(f"Updating read status for chat: {chatid}, user: {sid}")
            affected = DB.name('Xiaoxi').where("siliaoid", chatid).where("fasongren", "!=", sid).setField("shifouzhakan", "是")
            print(f"Updated {affected} messages to read for chat {chatid}")
            return R.success("ok")
        except Exception as db_error:
            print(f"Database error: {db_error}")
            return R.error(f"数据库操作失败: {str(db_error)}")
    except Exception as e:
        import traceback
        print(f"Unhandled exception in update_read: {e}")
        print(traceback.format_exc())
        return R.error(f"处理请求失败: {str(e)}")


@require_POST
@router.route('chatMessage')
def chat_message(request):
    req = json.loads(request.body)
    chatid = req.get("chatid")
    page_number = req.get("pageNumber", 1)
    page_size = req.get("pageSize", 20)
    offset_max = req.get("offsetMax", "")
    offset_min = req.get("offsetMin", "")
    type = req.get("type")
    list = []

    if type == "one":
        list = DB.name('Xiaoxi').where("siliaoid", chatid).order("id desc").limit(page_size).select()
    elif type == "top":
        list = DB.name('Xiaoxi').where("siliaoid", chatid) \
            .order("id desc").limit(page_size) \
            .where("id", "<", offset_min).select()
    elif type == "new":
        list = DB.name('Xiaoxi').where("siliaoid", chatid) \
            .order("id desc").limit(page_size) \
            .where("id", ">", offset_max).select()

    for v in list:
        user = get_user(v['fasongren'])
        v['fasongrenObj'] = user
        v['fasongrenUser'] = user
        v['user'] = user

    return R.success(list)


@csrf_exempt
@require_http_methods(['POST'])
def ask_question(request):
    try:
        print("Received request body:", request.body)
        data = json.loads(request.body)
        print("Parsed data:", data)
        
        question = data.get('question')
        user_id = data.get('user_id')
        
        print(f"Question: {question}, User ID: {user_id}")
        
        if not question:
            print("Error: Question is empty")
            return JsonResponse({
                'error': '问题内容不能为空'
            }, status=400)
            
        if not user_id:
            print("Error: User ID is empty")
            return JsonResponse({
                'error': '用户ID不能为空'
            }, status=400)
            
        # 获取回答
        try:
            answer = model_service.answer_question(question, user_id)
            print(f"Generated answer: {answer}")
            
            if not answer:
                print("Error: AI generated empty answer")
                return JsonResponse({
                    'error': 'AI生成回答失败'
                }, status=500)
            
            # 保存到数据库
            try:
                ChatHistory.objects.create(
                    user_id=user_id,
                    question=question,
                    answer=answer
                )
                print("Successfully saved to database")
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                # 即使保存失败也返回答案
                pass
            
            return JsonResponse({
                'answer': answer
            })
            
        except Exception as ai_error:
            print(f"AI service error: {str(ai_error)}")
            return JsonResponse({
                'error': 'AI服务错误：' + str(ai_error)
            }, status=500)
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return JsonResponse({
            'error': '请求数据格式错误'
        }, status=400)
    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(['GET'])
def get_history(request):
    try:
        print("Received request for history")
        print("Request GET params:", request.GET)
        print("Request headers:", request.headers)
        
        # 获取并验证用户ID
        user_id = request.GET.get('user_id')
        print(f"User ID from request: {user_id}")
        
        if not user_id:
            print("Error: User ID is empty")
            return JsonResponse({
                'error': '用户ID不能为空'
            }, status=400)
            
        # 验证用户ID格式
        if not isinstance(user_id, (str, int)):
            print(f"Error: Invalid user ID type: {type(user_id)}")
            return JsonResponse({
                'error': '用户ID格式错误'
            }, status=400)
            
        # 获取最近10条对话记录
        try:
            # 确保 user_id 是字符串类型
            user_id = str(user_id)
            print(f"Querying history for user_id: {user_id}")
            
            history = ChatHistory.objects.filter(
                user_id=user_id
            ).order_by('-created_at')[:10]
            
            print(f"Found {len(history)} history records")
            
            # 如果没有找到历史记录，返回空列表而不是错误
            if not history:
                print("No history records found")
                return JsonResponse([], safe=False)
            
            messages = []
            for record in reversed(history):
                messages.extend([
                    {
                        'role': 'user',
                        'content': record.question,
                        'timestamp': record.created_at.isoformat()
                    },
                    {
                        'role': 'assistant',
                        'content': record.answer,
                        'timestamp': record.created_at.isoformat()
                    }
                ])
                
            print(f"Returning {len(messages)} messages")
            return JsonResponse(messages, safe=False)
            
        except Exception as db_error:
            print(f"Database error: {str(db_error)}")
            print(f"Error type: {type(db_error)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({
                'error': '数据库查询错误'
            }, status=500)
        
    except Exception as e:
        print(f"Error in get_history: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def clear_history(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({
                'error': '用户ID不能为空'
            }, status=400)
            
        # 删除数据库中的记录
        ChatHistory.objects.filter(user_id=user_id).delete()
        
        # 清空内存中的对话上下文
        model_service.clear_conversation_history(user_id)
        
        return JsonResponse({
            'message': '对话历史已清空'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def get_follow_up_questions(request):
    try:
        data = json.loads(request.body)
        question = data.get('question')
        answer = data.get('answer')
        
        if not question or not answer:
            return JsonResponse({
                'error': '问题和回答不能为空'
            }, status=400)
            
        # 获取后续问题建议
        questions = model_service.generate_follow_up_questions(question, answer)
        
        return JsonResponse({
            'questions': questions
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

# 添加一个简单的测试API确认请求处理是否正常
@csrf_exempt
@require_POST
@router.route('test_api/')
def test_api(request):
    """简单的测试API，用于确认请求处理是否正常"""
    try:
        print("Test API called")
        print(f"Request method: {request.method}")
        print(f"Headers: {dict(request.headers.items())}")
        print(f"Body length: {len(request.body) if request.body else 0}")
        
        # 尝试处理请求体
        result = {"received": False, "data": None, "error": None}
        
        if request.body:
            try:
                body_str = request.body.decode('utf-8')
                print(f"Body as text: {body_str[:200]}")
                
                if 'application/json' in request.headers.get('Content-Type', ''):
                    data = json.loads(body_str)
                    result["received"] = True
                    result["data"] = data
                    print(f"Parsed JSON: {data}")
                else:
                    result["data"] = body_str
                    result["received"] = True
            except Exception as e:
                result["error"] = str(e)
                print(f"Error processing body: {e}")
        
        # 返回结果
        return JsonResponse({
            "code": 0,
            "msg": "测试接口",
            "data": result
        })
    except Exception as e:
        import traceback
        print(f"Test API error: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            "code": 1,
            "msg": f"测试接口错误: {str(e)}",
            "data": None
        })

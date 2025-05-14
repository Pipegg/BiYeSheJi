# =====================
# 依赖导入
# =====================
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from typing import Dict, Any
from .models import (
    AIConversation,
    AIHomeworkEvaluation,
    AILearningPath,
    AILearningAnalysis
)
from .serializers import (
    AIConversationSerializer,
    AIHomeworkEvaluationSerializer,
    AILearningPathSerializer,
    AILearningAnalysisSerializer
)
from LLMs.model_service import ModelService
from tijiaozuoye.models import Tijiaozuoye
from kechengxuexi.models import Kechengxuexi
from xuexijilu.models import Xuexijilu
import json
from django.http import HttpRequest
from core import R
from django.contrib.auth.models import AnonymousUser

# =====================
# 视图集定义
# =====================
class AIConversationViewSet(viewsets.ModelViewSet):
    """AI对话视图集"""
    serializer_class = AIConversationSerializer
    permission_classes = [IsAuthenticated]
    model_service = ModelService()

    def get_queryset(self):
        """获取当前用户的AI对话记录"""
        return AIConversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """创建AI对话并自动生成回复"""
        question: str = serializer.validated_data['question']
        context: str = serializer.validated_data.get('context', '')
        answer: str = self.model_service.answer_question(question, context)
        serializer.save(user=self.request.user, answer=answer)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """获取对话历史记录（最近50条）"""
        conversations = self.get_queryset().order_by('-created_at')[:50]
        messages = []
        for conv in conversations:
            messages.extend([
                {
                    'role': 'user',
                    'content': conv.question,
                    'timestamp': conv.created_at
                },
                {
                    'role': 'assistant',
                    'content': conv.answer,
                    'timestamp': conv.created_at
                }
            ])
        return Response({
            'code': 0,
            'msg': '获取成功',
            'data': messages
        })

class AIHomeworkEvaluationViewSet(viewsets.ModelViewSet):
    """AI作业批改视图集"""
    serializer_class = AIHomeworkEvaluationSerializer
    permission_classes = [IsAuthenticated]
    model_service = ModelService()

    def get_queryset(self):
        """获取当前用户的作业批改记录"""
        return AIHomeworkEvaluation.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        """创建作业批改记录并自动评测"""
        homework = serializer.validated_data['homework']
        answer: str = serializer.validated_data['answer']
        evaluation: Dict[str, Any] = self.model_service.evaluate_homework(homework.zuoyemingcheng, answer)
        serializer.save(
            student=self.request.user,
            score=evaluation['score'],
            strengths=evaluation['strengths'],
            weaknesses=evaluation['weaknesses'],
            suggestions=evaluation['suggestions']
        )

class AILearningPathViewSet(viewsets.ModelViewSet):
    """AI学习路径视图集"""
    serializer_class = AILearningPathSerializer
    permission_classes = [IsAuthenticated]
    model_service = ModelService()

    def get_user_from_token(self, request):
        """从请求中获取用户信息，优先处理token参数"""
        from core.R import jwtDecode
        
        # 先尝试从请求头获取token
        token = request.headers.get('token')
        if not token:
            auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]  # 去掉Bearer前缀
            
        # 如果请求头没有token，尝试从请求参数获取
        if not token and hasattr(request, 'GET') and 'token' in request.GET:
            token = request.GET.get('token')
            
        # 如果还没有token，尝试从请求体获取
        if not token and hasattr(request, 'data') and request.data:
            if isinstance(request.data, dict) and 'token' in request.data:
                token = request.data.get('token')
            
        # 如果还没有token，尝试从cookies获取
        if not token and hasattr(request, 'COOKIES') and 'auth_token' in request.COOKIES:
            token = request.COOKIES.get('auth_token')
        
        print(f"从请求中提取的token: {token[:30]}..." if token else "未找到token")
            
        if token:
            # 解析token获取用户信息
            decoded = jwtDecode(token)
            print(f"Token解析结果: {decoded}")
            if decoded and 'table' in decoded and 'id' in decoded:
                from core.query import DB
                # 从数据库获取用户信息
                user_data = DB.name(decoded['table']).find(decoded['id'])
                if user_data:
                    # 设置request.user为数据库中查询到的用户
                    request.user = user_data
                    print(f"用户认证成功: {user_data.get('username')}")
                    
                    # 将用户信息存储到session，确保持久化
                    if hasattr(request, 'session'):
                        request.session['user_id'] = decoded['id']
                        request.session['table'] = decoded['table']
                        request.session['username'] = user_data.get('username')
                        request.session.save()
                        print("用户信息已保存到session")
                    
                    # 创建响应用于设置cookie (Django中response对象会在视图返回时使用)
                    # 这里我们只是准备cookie数据，实际设置会在dispatch中完成
                    request._auth_cookies = {
                        'auth_token': token,
                        'user_id': decoded['id'],
                        'username': user_data.get('username', ''),
                        'table': decoded['table']
                    }
                    
                    return True
                else:
                    print(f"未找到ID为 {decoded['id']} 的用户")
            else:
                print("Token解析失败或缺少必要信息")
        return False

    def dispatch(self, request, *args, **kwargs):
        """重写dispatch方法，添加token验证"""
        print(f"\n--- Learning Path API 请求开始 ---")
        print(f"请求方法: {request.method}")
        print(f"请求路径: {request.path}")
        print(f"请求头: {dict(request.headers)}")
        print(f"Cookie: {request.COOKIES}")
        print(f"会话ID: {request.session.session_key if hasattr(request, 'session') else 'None'}")
        
        # 首先检查请求用户是否已经过Django认证
        if hasattr(request, 'user') and hasattr(request.user, 'is_authenticated'):
            if request.user.is_authenticated:
                print(f"Django认证已通过: {request.user}")
                response = super().dispatch(request, *args, **kwargs)
                return self._add_auth_cookies(response, request)
            else:
                print("Django认证未通过")
        
        # 尝试从token获取用户
        if self.get_user_from_token(request):
            print("Token认证成功")
            response = super().dispatch(request, *args, **kwargs)
            return self._add_auth_cookies(response, request)
        
        # 尝试从会话中获取用户ID
        if hasattr(request, 'session') and 'user_id' in request.session:
            try:
                from core.query import DB
                user_id = request.session['user_id']
                table = request.session.get('table', 'xuesheng')
                print(f"尝试从会话中获取用户: ID={user_id}, 表={table}")
                user_data = DB.name(table).find(user_id)
                if user_data:
                    request.user = user_data
                    print(f"会话认证成功: {user_data.get('username')}")
                    response = super().dispatch(request, *args, **kwargs)
                    return self._add_auth_cookies(response, request)
                else:
                    print(f"未找到ID为 {user_id} 的用户")
            except Exception as e:
                print(f"会话用户获取错误: {e}")
                import traceback
                traceback.print_exc()
        
        # 尝试从请求数据中获取用户信息（针对POST请求）
        if request.method == 'POST' and hasattr(request, 'data') and request.data:
            try:
                from core.query import DB
                data = request.data
                print(f"检查POST数据中的用户信息: {data}")
                
                if 'username' in data and data['username'] and 'table' in data:
                    username = data['username']
                    table = data['table']
                    print(f"从POST数据查找用户: 表={table}, 用户名={username}")
                    
                    users = DB.name(table).where('username', username).select()
                    if users and len(users) > 0:
                        user_data = users[0]
                        request.user = user_data
                        print(f"从POST数据找到用户: {user_data.get('username')}")
                        return super().dispatch(request, *args, **kwargs)
                
                if 'user_id' in data and data['user_id'] and 'table' in data:
                    user_id = data['user_id']
                    table = data['table']
                    print(f"从POST数据查找用户ID: 表={table}, ID={user_id}")
                    
                    user_data = DB.name(table).find(user_id)
                    if user_data:
                        request.user = user_data
                        print(f"从POST数据找到用户: {user_data.get('username')}")
                        return super().dispatch(request, *args, **kwargs)
            except Exception as e:
                print(f"处理POST数据时出错: {e}")
        
        # 所有认证方式都失败，返回403错误
        print("认证失败，返回403错误")
        return Response({"code": 403, "msg": "请先登录后再访问学习路径"}, status=403)

    def _add_auth_cookies(self, response, request):
        """添加认证cookie到响应"""
        if hasattr(request, '_auth_cookies'):
            try:
                # 设置cookie，有效期为7天
                max_age = 7 * 24 * 60 * 60  # 7天
                for key, value in request._auth_cookies.items():
                    response.set_cookie(
                        key, 
                        value, 
                        max_age=max_age, 
                        httponly=True, 
                        samesite='Lax',
                        secure=request.is_secure()  # 在HTTPS时设置secure
                    )
                    print(f"设置认证cookie: {key}")
            except Exception as e:
                print(f"设置cookie时出错: {e}")
        return response

    def get_queryset(self):
        """获取当前用户的学习路径"""
        print(f"获取学习路径 - 当前用户: {self.request.user}")
        print(f"用户类型: {type(self.request.user)}")
        
        # 先尝试使用用户的ID或username直接查询
        try:
            # 使用getattr安全地获取ID，避免类型错误
            user_id = getattr(self.request.user, 'id', None)
            if user_id:
                print(f"使用用户ID查询: {user_id}")
                paths = AILearningPath.objects.filter(student=self.request.user)
                print(f"找到学习路径数量: {len(paths)}")
                return paths
        except Exception as e:
            print(f"直接查询失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 尝试使用字典类型的用户处理
        try:
            if isinstance(self.request.user, dict):
                print("用户对象是字典类型")
                
                # 尝试使用ID查询
                if 'id' in self.request.user and self.request.user['id']:
                    user_id = self.request.user['id']
                    print(f"尝试使用字典ID查询: {user_id}")
                    
                    # 获取表名
                    table = self.request.user.get('table', 'xuesheng')
                    print(f"表名: {table}")
                    
                    # 构建查询
                    query = Q(student__id=user_id)
                    
                    # 如果有用户名也添加到查询条件
                    if 'username' in self.request.user and self.request.user['username']:
                        username = self.request.user['username']
                        print(f"同时使用用户名查询: {username}")
                        query = query | Q(student__username=username)
                    
                    paths = AILearningPath.objects.filter(query)
                    print(f"找到学习路径数量: {len(paths)}")
                    return paths
                
                # 如果没有ID但有用户名
                elif 'username' in self.request.user and self.request.user['username']:
                    username = self.request.user['username']
                    print(f"仅使用用户名查询: {username}")
                    paths = AILearningPath.objects.filter(student__username=username)
                    print(f"找到学习路径数量: {len(paths)}")
                    return paths
        except Exception as e:
            print(f"字典查询方法失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 尝试从查询参数或GET参数中获取用户信息
        try:
            # 检查请求是否有GET参数
            if hasattr(self.request, 'GET'):
                params = self.request.GET
                
                if 'username' in params and params['username']:
                    username = params['username']
                    print(f"从GET参数获取用户名: {username}")
                    paths = AILearningPath.objects.filter(student__username=username)
                    print(f"找到学习路径数量: {len(paths)}")
                    return paths
                
                if 'user_id' in params and params['user_id']:
                    user_id = params['user_id']
                    print(f"从GET参数获取用户ID: {user_id}")
                    paths = AILearningPath.objects.filter(student__id=user_id)
                    print(f"找到学习路径数量: {len(paths)}")
                    return paths
                    
            # 尝试从session获取
            if hasattr(self.request, 'session'):
                user_id = self.request.session.get('user_id')
                if user_id:
                    print(f"从session获取用户ID: {user_id}")
                    table = self.request.session.get('table', 'xuesheng')
                    paths = AILearningPath.objects.filter(student__id=user_id)
                    print(f"找到学习路径数量: {len(paths)}")
                    return paths
        except Exception as e:
            print(f"参数查询方法失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 所有方法都失败，返回空查询集
        print("所有查询方法都失败，返回空查询集")
        return AILearningPath.objects.none()

    def perform_create(self, serializer):
        """创建学习路径并自动生成内容"""
        subject: str = serializer.validated_data['subject']
        level: str = serializer.validated_data['level']
        learning_path: Dict[str, Any] = self.model_service.generate_learning_path(subject, level)
        # 初始化progress为与order等长的0列表
        progress = [0] * len(learning_path.get('order', []))
        serializer.save(
            student=self.request.user,
            goals=learning_path['goals'],
            content=learning_path['content'],
            order=learning_path['order'],
            suggestions=learning_path['suggestions'],
            progress=progress
        )

    @action(detail=True, methods=['post'])
    def mark_stage(self, request, pk=None):
        """
        阶段进度打卡/撤销打卡
        参数: stage_index(int), status(0/1)
        """
        path = self.get_object()
        stage_index = int(request.data.get('stage_index', -1))
        status = int(request.data.get('status', 1))
        if 0 <= stage_index < len(path.progress):
            path.progress[stage_index] = status
            path.save()
            return Response({'code': 0, 'msg': '进度已更新', 'progress': path.progress})
        return Response({'code': 1, 'msg': '参数错误'}, status=400)

    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """
        路径再生成/微调
        可选参数: subject, level
        """
        path = self.get_object()
        subject = request.data.get('subject', path.subject)
        level = request.data.get('level', path.level)
        learning_path: Dict[str, Any] = self.model_service.generate_learning_path(subject, level)
        path.subject = subject
        path.level = level
        path.goals = learning_path['goals']
        path.content = learning_path['content']
        path.order = learning_path['order']
        path.suggestions = learning_path['suggestions']
        path.progress = [0] * len(learning_path.get('order', []))
        path.save()
        return Response({'code': 0, 'msg': '学习路径已重新生成', 'data': AILearningPathSerializer(path).data})

    @action(detail=False, methods=['post'])
    def fetch(self, request):
        """
        使用POST方法获取当前用户的学习路径
        支持在请求体中传递认证信息
        """
        print(f"\n--- Learning Path Fetch 请求 ---")
        print(f"请求数据: {request.data}")
        print(f"请求头: {dict(request.headers)}")
        print(f"Cookie: {request.COOKIES}")
        print(f"会话ID: {request.session.session_key if hasattr(request, 'session') else 'None'}")
        
        # 检查会话中是否保存了用户状态
        if hasattr(request, 'session'):
            print(f"会话内容: {dict(request.session)}")
        
        # 先直接尝试使用当前用户获取学习路径
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            print(f"当前用户: {request.user}")
            # 获取学习路径
            queryset = self.get_queryset()
            print(f"查询集大小: {queryset.count()}")
            
            if queryset.exists():
                # 返回第一个学习路径
                serializer = self.get_serializer(queryset.first())
                print(f"返回学习路径: {serializer.data.get('id')}")
                return Response({
                    "code": 0,
                    "msg": "获取成功",
                    "data": serializer.data
                })
            else:
                print("用户没有学习路径")
                return Response({
                    "code": 404,
                    "msg": "未找到学习路径，请创建一个新的",
                }, status=404)
        
        # 尝试使用请求中的token认证（如果用户尚未认证）
        auth_success = False
        
        # 1. 尝试从HTTP头中获取token (使用各种可能的头名称)
        token = None
        auth_headers = ['token', 'Authorization', 'authorization', 'X-Token', 'x-token']
        
        for header in auth_headers:
            if header in request.headers:
                header_value = request.headers.get(header)
                print(f"从头部 {header} 获取 token/auth 信息: {header_value[:30]}..." if header_value else "无")
                
                # 处理Bearer token
                if header_value and header_value.startswith('Bearer '):
                    token = header_value[7:]
                    print(f"发现Bearer token: {token[:30]}...")
                    break
                elif header_value:
                    token = header_value
                    print(f"发现普通token: {token[:30]}...")
                    break
        
        # 2. 尝试从请求体中获取token
        if not token and 'token' in request.data:
            token = request.data.get('token')
            print(f"从请求体中获取token: {token[:30]}..." if token else "无token")
        
        # 3. 尝试从请求参数中获取token
        if not token and hasattr(request, 'GET') and 'token' in request.GET:
            token = request.GET.get('token')
            print(f"从URL参数中获取token: {token[:30]}..." if token else "无token")
        
        # 4. 尝试从cookies中获取token
        if not token and 'token' in request.COOKIES:
            token = request.COOKIES.get('token')
            print(f"从Cookies中获取token: {token[:30]}..." if token else "无token")
        
        # 5. 使用token进行认证
        if token:
            from core.R import jwtDecode
            decoded = jwtDecode(token)
            if decoded and 'table' in decoded and 'id' in decoded:
                from core.query import DB
                print(f"Token解析结果: {decoded}")
                user_data = DB.name(decoded['table']).find(decoded['id'])
                if user_data:
                    request.user = user_data
                    print(f"Token认证成功: {user_data.get('username')}")
                    auth_success = True
                    
                    # 将用户信息存储到session
                    if hasattr(request, 'session'):
                        request.session['user_id'] = decoded['id']
                        request.session['table'] = decoded['table']
                        request.session['username'] = user_data.get('username')
                        request.session.save()
                        print("用户信息已保存到会话")
        
        # 6. 如果token认证失败，尝试从请求数据中获取用户信息
        if not auth_success:
            try:
                from core.query import DB
                # 检查所有可能的用户名字段
                username_fields = ['username', 'user', 'name', 'xuehao', 'gonghao']
                username = None
                
                for field in username_fields:
                    if field in request.data and request.data[field]:
                        username = request.data[field]
                        print(f"从字段 {field} 找到用户名: {username}")
                        break
                    
                # 检查可能的用户ID字段
                id_fields = ['user_id', 'id', 'userId', 'userid']
                user_id = None
                
                for field in id_fields:
                    if field in request.data and request.data[field]:
                        user_id = request.data[field]
                        print(f"从字段 {field} 找到用户ID: {user_id}")
                        break
                
                # 确定用户表
                table = request.data.get('table', 'xuesheng')
                
                # 先尝试用户名查询
                if username:
                    print(f"从请求数据查找用户: 表={table}, 用户名={username}")
                    users = DB.name(table).where('username', username).select()
                    
                    # 尝试其他可能的用户名字段
                    if not users or len(users) == 0:
                        for field in ['xuehao', 'gonghao']:
                            users = DB.name(table).where(field, username).select()
                            if users and len(users) > 0:
                                print(f"通过字段 {field} 找到用户")
                                break
                    
                    if users and len(users) > 0:
                        user_data = users[0]
                        print(f"通过用户名找到用户: {user_data}")
                        request.user = user_data
                        auth_success = True
                    else:
                        print(f"未找到用户名为 {username} 的用户")
                
                # 如果用户名查询失败，尝试ID查询
                if not auth_success and user_id:
                    print(f"从请求数据查找用户ID: 表={table}, ID={user_id}")
                    user_data = DB.name(table).find(user_id)
                    if user_data:
                        print(f"通过ID找到用户: {user_data}")
                        request.user = user_data
                        auth_success = True
                    else:
                        print(f"未找到ID为 {user_id} 的用户")
            except Exception as e:
                print(f"从请求数据获取用户信息时出错: {e}")
                import traceback
                traceback.print_exc()
        
        # 7. 如果通过任何方式成功认证，尝试获取学习路径
        if auth_success:
            # 获取学习路径
            queryset = self.get_queryset()
            print(f"查询集大小: {queryset.count()}")
            
            if queryset.exists():
                # 返回第一个学习路径
                serializer = self.get_serializer(queryset.first())
                print(f"返回学习路径: {serializer.data.get('id')}")
                return Response({
                    "code": 0,
                    "msg": "获取成功",
                    "data": serializer.data
                })
            else:
                print("用户没有学习路径")
                return Response({
                    "code": 404,
                    "msg": "未找到学习路径，请创建一个新的",
                }, status=404)
        
        # 所有认证方法都失败，返回详细的错误信息
        print("认证失败，返回403错误")
        return Response({
            "code": 403, 
            "msg": "请先登录后再访问学习路径",
            "auth_error": True,
            "debug_info": {
                "has_token": bool(token),
                "has_session": hasattr(request, 'session') and bool(request.session.session_key),
                "has_cookies": bool(request.COOKIES),
                "user_info_in_request": bool(request.data.get('username') or request.data.get('user_id')),
            }
        }, status=403)

class AILearningAnalysisViewSet(viewsets.ModelViewSet):
    """AI学习进度分析视图集"""
    serializer_class = AILearningAnalysisSerializer
    permission_classes = [IsAuthenticated]
    model_service = ModelService()

    def get_queryset(self):
        """获取当前用户的学习进度分析"""
        return AILearningAnalysis.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        """创建学习进度分析并自动分析数据"""
        student_data: Dict[str, Any] = self._get_student_data()
        analysis: Dict[str, Any] = self.model_service.analyze_learning_progress(student_data)
        serializer.save(
            student=self.request.user,
            overall_progress=analysis['overall_progress'],
            strengths=analysis['strengths'],
            weaknesses=analysis['weaknesses'],
            suggestions=analysis['suggestions']
        )

    def _get_student_data(self) -> Dict[str, Any]:
        """
        获取学生的学习数据
        Returns:
            包含学生学习数据的字典
        """
        user = self.request.user
        # 获取作业成绩
        homework_scores = Tijiaozuoye.objects.filter(
            tijiaoxuesheng=user.get_username()
        ).values('zuoyemingcheng').annotate(
            avg_score=Avg('zuoyezhuangtai')
        ).order_by('-avg_score')[:5]
        # 获取课程进度
        course_progress = Kechengxuexi.objects.filter(
            xueshengyonghu=user.get_username()
        ).values('kechengmingcheng', 'xuexijindu').order_by('-xuexijindu')[:5]
        # 获取学习时间
        learning_time = Xuexijilu.objects.filter(
            xueshengyonghu=user.get_username()
        ).values('addtime').annotate(
            total_time=Count('id')
        ).order_by('-addtime')[:7]
        return {
            'homework_scores': list(homework_scores),
            'course_progress': list(course_progress),
            'learning_time': list(learning_time),
            'student_info': {
                'name': user.get_username(),
                'total_courses': Kechengxuexi.objects.filter(xueshengyonghu=user.get_username()).count(),
                'total_homework': Tijiaozuoye.objects.filter(tijiaoxuesheng=user.get_username()).count(),
                'total_learning_time': Xuexijilu.objects.filter(xueshengyonghu=user.get_username()).count()
            }
        } 
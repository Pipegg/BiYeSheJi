from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from core import utils, DB, R
from core import Blueprint
from .llm_recommend import LLMRecommender
import pandas as pd
from kechengxinxi.models import Kechengxinxi
from xuexijilu.models import Xuexijilu
from typing import Optional
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由装饰器
router = Blueprint("yuce")

# 全局推荐器实例
recommender: Optional[LLMRecommender] = None

def get_course_data() -> pd.DataFrame:
    """
    获取课程数据并转换为DataFrame
    """
    try:
        courses = Kechengxinxi.objects.all().values()
        return pd.DataFrame(list(courses))
    except Exception as e:
        logger.error(f"获取课程数据失败: {e}")
        return pd.DataFrame()

def get_student_data() -> pd.DataFrame:
    """
    获取学习记录数据并转换为DataFrame
    """
    try:
        study_records = Xuexijilu.objects.all().values()
        return pd.DataFrame(list(study_records))
    except Exception as e:
        logger.error(f"获取学习记录失败: {e}")
        return pd.DataFrame()

def init_recommender() -> None:
    """
    初始化推荐系统
    """
    global recommender
    try:
        if recommender is None:
            recommender = LLMRecommender()
            
            # 获取数据
            course_data = get_course_data()
            student_data = get_student_data()
            
            if course_data.empty or student_data.empty:
                logger.error("无法初始化推荐系统：数据为空")
                return
            
            # 训练推荐系统
            recommender.fit(course_data, student_data)
            logger.info("推荐系统初始化成功")
    except Exception as e:
        logger.error(f"初始化推荐系统失败: {e}")
        recommender = None

@router.route('/recommend_courses')
def recommend_courses(request):
    """
    为当前用户推荐课程
    """
    try:
        # 确保用户已登录
        if not utils.checkLogin():
            return R.error("请先登录")
            
        # 获取当前用户ID
        user_id = utils.session('id')
        if not user_id:
            return R.error("无法获取用户ID")
            
        # 初始化推荐系统
        init_recommender()
        if recommender is None:
            return R.error("推荐系统初始化失败")
            
        # 获取推荐数量参数
        try:
            top_n = int(request.GET.get('top_n', 5))
            top_n = max(1, min(top_n, 20))  # 限制推荐数量范围
        except ValueError:
            top_n = 5
            
        # 获取推荐课程
        recommendations = recommender.recommend_courses(str(user_id), top_n=top_n)
        
        if not recommendations:
            return R.success([])  # 返回空列表而不是错误
            
        return R.success(recommendations)
    except Exception as e:
        logger.error(f"推荐课程时出错: {e}")
        return R.error(f"推荐失败：{str(e)}")

@router.route('/get_popular_courses')
def get_popular_courses(request):
    """
    获取热门课程
    """
    try:
        # 初始化推荐系统
        init_recommender()
        if recommender is None:
            return R.error("推荐系统初始化失败")
            
        # 获取推荐数量参数
        try:
            top_n = int(request.GET.get('top_n', 5))
            top_n = max(1, min(top_n, 20))  # 限制推荐数量范围
        except ValueError:
            top_n = 5
            
        # 获取热门课程
        popular_courses = recommender.get_popular_courses(top_n=top_n)
        
        if not popular_courses:
            return R.success([])  # 返回空列表而不是错误
            
        return R.success(popular_courses)
    except Exception as e:
        logger.error(f"获取热门课程时出错: {e}")
        return R.error(f"获取热门课程失败：{str(e)}")

@router.route('/get_course_explanation')
def get_course_explanation(request):
    """
    获取课程推荐解释
    """
    try:
        # 确保用户已登录
        if not utils.checkLogin():
            return R.error("请先登录")
            
        # 获取参数
        user_id = utils.session('id')
        course_id = request.GET.get('course_id')
        
        if not user_id or not course_id:
            return R.error("缺少必要参数")
            
        # 初始化推荐系统
        init_recommender()
        if recommender is None:
            return R.error("推荐系统初始化失败")
            
        # 获取推荐解释
        explanation = recommender.get_recommendation_explanation(str(user_id), str(course_id))
        
        return R.success({"explanation": explanation})
    except Exception as e:
        logger.error(f"获取推荐解释时出错: {e}")
        return R.error(f"获取推荐解释失败：{str(e)}")

@router.route('/update_recommender')
def update_recommender(request):
    """
    更新推荐系统
    """
    try:
        # 重新初始化推荐系统
        global recommender
        recommender = None
        init_recommender()
        
        if recommender is None:
            return R.error("推荐系统更新失败")
            
        return R.success("推荐系统更新成功")
    except Exception as e:
        logger.error(f"更新推荐系统时出错: {e}")
        return R.error(f"更新失败：{str(e)}")

@router.route('/get_student_profile')
def get_student_profile(request):
    """
    获取学生学习画像
    """
    try:
        # 确保用户已登录
        if not utils.checkLogin():
            return R.error("请先登录")
            
        # 获取当前用户ID
        user_id = utils.session('id')
        if not user_id:
            return R.error("无法获取用户ID")
            
        # 初始化推荐系统
        init_recommender()
        if recommender is None:
            return R.error("推荐系统初始化失败")
            
        # 获取学习画像
        profile = recommender.analyze_student_profile(str(user_id))
        
        return R.success(profile)
    except Exception as e:
        logger.error(f"获取学习画像时出错: {e}")
        return R.error(f"获取学习画像失败：{str(e)}") 
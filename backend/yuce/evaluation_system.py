# =====================
# 依赖导入
# =====================
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
from sklearn.metrics import ndcg_score

logger = logging.getLogger(__name__)

# =====================
# 推荐系统评估与反馈主类
# =====================
class EvaluationSystem:
    def __init__(self):
        """
        初始化评估系统，包含多种评估指标和反馈收集机制
        """
        self.metrics = {
            'precision': self._calculate_precision,
            'recall': self._calculate_recall,
            'ndcg': self._calculate_ndcg,
            'diversity': self._calculate_diversity,
            'novelty': self._calculate_novelty,
            'coverage': self._calculate_coverage
        }
        self.feedback_data = []
        self.ab_test_groups = {}

    # =====================
    # 推荐评估相关
    # =====================
    def evaluate_recommendations(self, recommendations: List[Dict[str, Any]], 
                              ground_truth: List[str],
                              all_items: List[str]) -> Dict[str, float]:
        """
        评估推荐结果，返回各项指标分数
        """
        try:
            if not recommendations or not ground_truth:
                return {metric: 0.0 for metric in self.metrics.keys()}
            rec_items = [rec['course_id'] for rec in recommendations]
            results = {}
            for metric_name, metric_func in self.metrics.items():
                results[metric_name] = metric_func(rec_items, ground_truth, all_items)
            return results
        except Exception as e:
            logger.error(f"评估推荐结果失败: {e}")
            return {metric: 0.0 for metric in self.metrics.keys()}

    def _calculate_precision(self, recommended: List[str], 
                          relevant: List[str], 
                          all_items: List[str]) -> float:
        """
        计算准确率
        """
        try:
            if not recommended:
                return 0.0
            hits = len(set(recommended) & set(relevant))
            return float(hits / len(recommended))
        except Exception as e:
            logger.error(f"计算准确率失败: {e}")
            return 0.0

    def _calculate_recall(self, recommended: List[str], 
                       relevant: List[str], 
                       all_items: List[str]) -> float:
        """
        计算召回率
        """
        try:
            if not relevant:
                return 0.0
            hits = len(set(recommended) & set(relevant))
            return float(hits / len(relevant))
        except Exception as e:
            logger.error(f"计算召回率失败: {e}")
            return 0.0

    def _calculate_ndcg(self, recommended: List[str], 
                      relevant: List[str], 
                      all_items: List[str]) -> float:
        """
        计算NDCG
        """
        try:
            if not recommended or not relevant:
                return 0.0
            relevance = np.zeros(len(recommended))
            for i, item in enumerate(recommended):
                if item in relevant:
                    relevance[i] = 1
            ideal_relevance = np.zeros(len(recommended))
            ideal_relevance[:min(len(relevant), len(recommended))] = 1
            relevance = relevance.reshape(1, -1)
            ideal_relevance = ideal_relevance.reshape(1, -1)
            return float(ndcg_score(ideal_relevance, relevance))
        except Exception as e:
            logger.error(f"计算NDCG失败: {e}")
            return 0.0

    def _calculate_diversity(self, recommended: List[str], 
                          relevant: List[str], 
                          all_items: List[str]) -> float:
        """
        计算多样性
        """
        try:
            if len(recommended) < 2:
                return 0.0
            diversity_sum = 0
            count = 0
            for i in range(len(recommended)):
                for j in range(i + 1, len(recommended)):
                    diversity_sum += 1 - self._item_similarity(recommended[i], recommended[j])
                    count += 1
            return float(diversity_sum / count if count > 0 else 0)
        except Exception as e:
            logger.error(f"计算多样性失败: {e}")
            return 0.0

    def _calculate_novelty(self, recommended: List[str], 
                        relevant: List[str], 
                        all_items: List[str]) -> float:
        """
        计算新颖性
        """
        try:
            if not recommended or not all_items:
                return 0.0
            item_popularity = self._calculate_item_popularity(all_items)
            novelty_sum = sum(-np.log2(item_popularity.get(item, 1.0)) 
                            for item in recommended)
            return float(novelty_sum / len(recommended))
        except Exception as e:
            logger.error(f"计算新颖性失败: {e}")
            return 0.0

    def _calculate_coverage(self, recommended: List[str], 
                         relevant: List[str], 
                         all_items: List[str]) -> float:
        """
        计算覆盖率
        """
        try:
            if not recommended or not all_items:
                return 0.0
            return float(len(set(recommended)) / len(all_items))
        except Exception as e:
            logger.error(f"计算覆盖率失败: {e}")
            return 0.0

    def _item_similarity(self, item1: str, item2: str) -> float:
        """
        计算项目间相似度（可自定义实现）
        """
        return 0.5

    def _calculate_item_popularity(self, items: List[str]) -> Dict[str, float]:
        """
        计算项目流行度（可自定义实现）
        """
        return {item: 1.0/len(items) for item in items}

    # =====================
    # 用户反馈收集与分析
    # =====================
    def collect_feedback(self, user_id: str, course_id: str, 
                       feedback_type: str, rating: float) -> None:
        """
        收集用户反馈
        """
        try:
            feedback = {
                'user_id': user_id,
                'course_id': course_id,
                'feedback_type': feedback_type,
                'rating': rating,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.feedback_data.append(feedback)
        except Exception as e:
            logger.error(f"收集用户反馈失败: {e}")

    def analyze_feedback(self, time_window: int = 7) -> Dict[str, Any]:
        """
        分析用户反馈
        """
        try:
            if not self.feedback_data:
                return {}
            current_time = datetime.now()
            start_time = current_time - timedelta(days=time_window)
            recent_feedback = [
                f for f in self.feedback_data 
                if datetime.strptime(f['timestamp'], '%Y-%m-%d %H:%M:%S') >= start_time
            ]
            if not recent_feedback:
                return {}
            feedback_df = pd.DataFrame(recent_feedback)
            analysis = {
                'average_rating': float(feedback_df['rating'].mean()),
                'rating_distribution': feedback_df['rating'].value_counts().to_dict(),
                'feedback_types': feedback_df['feedback_type'].value_counts().to_dict(),
                'daily_feedback_count': feedback_df.groupby(
                    pd.to_datetime(feedback_df['timestamp']).dt.date
                ).size().to_dict()
            }
            return analysis
        except Exception as e:
            logger.error(f"分析用户反馈失败: {e}")
            return {}

    # =====================
    # A/B 测试相关
    # =====================
    def setup_ab_test(self, test_name: str, variants: List[str], 
                    distribution: List[float]) -> bool:
        """
        设置A/B测试
        """
        try:
            if not variants or not distribution or len(variants) != len(distribution):
                return False
            self.ab_test_groups[test_name] = {
                'variants': variants,
                'distribution': distribution,
                'assignments': {},
                'results': {variant: [] for variant in variants}
            }
            return True
        except Exception as e:
            logger.error(f"设置A/B测试失败: {e}")
            return False

    def assign_variant(self, test_name: str, user_id: str) -> Optional[str]:
        """
        分配用户到A/B测试组
        """
        try:
            group = self.ab_test_groups.get(test_name)
            if not group:
                return None
            if user_id in group['assignments']:
                return group['assignments'][user_id]
            # 按分布概率分配
            import random
            r = random.random()
            cumulative = 0.0
            for variant, prob in zip(group['variants'], group['distribution']):
                cumulative += prob
                if r < cumulative:
                    group['assignments'][user_id] = variant
                    return variant
            # 默认分配到最后一个
            group['assignments'][user_id] = group['variants'][-1]
            return group['variants'][-1]
        except Exception as e:
            logger.error(f"分配A/B测试组失败: {e}")
            return None

    def record_ab_test_result(self, test_name: str, variant: str, 
                           metrics: Dict[str, float]) -> bool:
        """
        记录A/B测试结果
        """
        try:
            group = self.ab_test_groups.get(test_name)
            if not group or variant not in group['results']:
                return False
            group['results'][variant].append(metrics)
            return True
        except Exception as e:
            logger.error(f"记录A/B测试结果失败: {e}")
            return False

    def analyze_ab_test(self, test_name: str) -> Dict[str, Any]:
        """
        分析A/B测试结果
        """
        try:
            group = self.ab_test_groups.get(test_name)
            if not group:
                return {}
            results = group['results']
            analysis = {variant: self._analyze_metrics(metrics_list)
                        for variant, metrics_list in results.items()}
            # 可扩展：统计显著性检验
            if len(results) == 2:
                variants = list(results.keys())
                analysis['significance'] = self._calculate_significance(
                    results[variants[0]], results[variants[1]])
            return analysis
        except Exception as e:
            logger.error(f"分析A/B测试结果失败: {e}")
            return {}

    def _analyze_metrics(self, metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
        """
        计算一组指标的均值
        """
        if not metrics_list:
            return {}
        df = pd.DataFrame(metrics_list)
        return df.mean().to_dict()

    def _calculate_significance(self, group1_results: List[Dict[str, float]], 
                             group2_results: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        显著性检验（可扩展）
        """
        # 这里只做均值对比，实际可用 t 检验等
        if not group1_results or not group2_results:
            return {}
        df1 = pd.DataFrame(group1_results)
        df2 = pd.DataFrame(group2_results)
        mean1 = df1.mean().to_dict() if not df1.empty else {}
        mean2 = df2.mean().to_dict() if not df2.empty else {}
        return {'group1_mean': mean1, 'group2_mean': mean2}
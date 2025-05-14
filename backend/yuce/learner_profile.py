# =====================
# 依赖导入
# =====================
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)

# =====================
# 学习者画像系统
# =====================
class LearnerProfile:
    def __init__(self):
        """
        初始化学习者画像系统
        """
        self.cognitive_features = {}  # 认知特征
        self.affective_features = {}  # 情感特征
        self.behavioral_features = {} # 行为特征
        self.temporal_features = {}   # 时序特征
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=5)

    # =====================
    # 特征提取
    # =====================
    def extract_cognitive_features(self, learning_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        提取认知特征
        """
        try:
            if not learning_records:
                return {}
            scores = [record.get('quiz_score', 0) for record in learning_records]
            progress = [record.get('progress', 0) for record in learning_records]
            return {
                'average_score': np.mean(scores),
                'score_std': np.std(scores),
                'progress_rate': np.mean(progress),
                'mastery_level': self._calculate_mastery_level(scores, progress),
                'learning_speed': self._calculate_learning_speed(learning_records)
            }
        except Exception as e:
            logger.error(f"提取认知特征失败: {e}")
            return {}

    def extract_affective_features(self, interaction_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        提取情感特征
        """
        try:
            if not interaction_records:
                return {}
            return {
                'engagement_level': self._calculate_engagement(interaction_records),
                'persistence_score': self._calculate_persistence(interaction_records),
                'interest_areas': self._identify_interests(interaction_records),
                'learning_style': self._identify_learning_style(interaction_records)
            }
        except Exception as e:
            logger.error(f"提取情感特征失败: {e}")
            return {}

    def extract_behavioral_features(self, learning_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        提取行为特征
        """
        try:
            if not learning_records:
                return {}
            return {
                'study_pattern': self._analyze_study_pattern(learning_records),
                'interaction_frequency': self._calculate_interaction_frequency(learning_records),
                'completion_rate': self._calculate_completion_rate(learning_records),
                'review_habit': self._analyze_review_habit(learning_records)
            }
        except Exception as e:
            logger.error(f"提取行为特征失败: {e}")
            return {}

    def extract_temporal_features(self, learning_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        提取时序特征
        """
        try:
            if not learning_records:
                return {}
            sorted_records = sorted(learning_records, 
                                 key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'))
            return {
                'learning_trend': self._analyze_learning_trend(sorted_records),
                'study_time_distribution': self._analyze_study_time(sorted_records),
                'progress_velocity': self._calculate_progress_velocity(sorted_records),
                'knowledge_retention': self._analyze_knowledge_retention(sorted_records)
            }
        except Exception as e:
            logger.error(f"提取时序特征失败: {e}")
            return {}

    # =====================
    # 认知/行为/情感/时序特征计算
    # =====================
    def _calculate_mastery_level(self, scores: List[float], progress: List[float]) -> float:
        """
        计算知识掌握水平
        """
        if not scores or not progress:
            return 0.0
        weighted_scores = np.array(scores) * np.array(progress)
        return float(np.mean(weighted_scores))

    def _calculate_learning_speed(self, records: List[Dict[str, Any]]) -> float:
        """
        计算学习速度
        """
        if not records:
            return 0.0
        progress_changes = []
        for i in range(1, len(records)):
            time_diff = datetime.strptime(records[i]['timestamp'], '%Y-%m-%d %H:%M:%S') - \
                       datetime.strptime(records[i-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
            progress_diff = records[i].get('progress', 0) - records[i-1].get('progress', 0)
            if time_diff.total_seconds() > 0:
                progress_changes.append(progress_diff / time_diff.total_seconds())
        return float(np.mean(progress_changes)) if progress_changes else 0.0

    def _calculate_engagement(self, records: List[Dict[str, Any]]) -> float:
        """
        计算参与度
        """
        if not records:
            return 0.0
        interaction_scores = []
        for record in records:
            score = 0
            score += record.get('comments', 0) * 2
            score += record.get('questions', 0) * 3
            score += record.get('submissions', 0) * 4
            interaction_scores.append(score)
        return float(np.mean(interaction_scores))

    def _calculate_persistence(self, records: List[Dict[str, Any]]) -> float:
        """
        计算坚持度
        """
        if not records:
            return 0.0
        retry_counts = [record.get('retry_count', 0) for record in records]
        return float(np.mean(retry_counts))

    def _identify_interests(self, records: List[Dict[str, Any]]) -> List[str]:
        """
        识别兴趣领域
        """
        if not records:
            return []
        category_scores = {}
        for record in records:
            category = record.get('category', '')
            if category:
                score = record.get('engagement_score', 0)
                category_scores[category] = category_scores.get(category, 0) + score
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, _ in sorted_categories[:3]]

    def _identify_learning_style(self, records: List[Dict[str, Any]]) -> str:
        """
        识别学习风格
        """
        if not records:
            return "unknown"
        behaviors = {
            'visual': 0,
            'auditory': 0,
            'reading': 0,
            'kinesthetic': 0
        }
        for record in records:
            behaviors['visual'] += record.get('video_time', 0)
            behaviors['auditory'] += record.get('audio_time', 0)
            behaviors['reading'] += record.get('reading_time', 0)
            behaviors['kinesthetic'] += record.get('practice_time', 0)
        return max(behaviors.items(), key=lambda x: x[1])[0]

    def _analyze_study_pattern(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析学习模式
        """
        if not records:
            return {}
        study_times = [datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S').hour 
                      for record in records]
        return {
            'peak_hours': self._find_peak_hours(study_times),
            'session_length': self._calculate_average_session_length(records),
            'frequency': self._calculate_study_frequency(records)
        }

    # =====================
    # 画像更新与行为分析
    # =====================
    def update_profile(self, student_id: str, new_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        更新学习者画像
        """
        try:
            self.cognitive_features = self.extract_cognitive_features(new_records)
            self.affective_features = self.extract_affective_features(new_records)
            self.behavioral_features = self.extract_behavioral_features(new_records)
            self.temporal_features = self.extract_temporal_features(new_records)
            profile = {
                'student_id': student_id,
                'cognitive_features': self.cognitive_features,
                'affective_features': self.affective_features,
                'behavioral_features': self.behavioral_features,
                'temporal_features': self.temporal_features,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return profile
        except Exception as e:
            logger.error(f"更新学习者画像失败: {e}")
            return {}

    def _calculate_interaction_frequency(self, records: List[Dict[str, Any]]) -> float:
        """
        计算互动频率
        """
        if not records:
            return 0.0
        total_interactions = sum(record.get('interactions', 0) for record in records)
        time_span = (datetime.strptime(records[-1]['timestamp'], '%Y-%m-%d %H:%M:%S') - 
                    datetime.strptime(records[0]['timestamp'], '%Y-%m-%d %H:%M:%S')).days + 1
        return total_interactions / time_span if time_span > 0 else 0.0

    def _calculate_completion_rate(self, records: List[Dict[str, Any]]) -> float:
        """
        计算完成率
        """
        if not records:
            return 0.0
        completed = sum(1 for record in records if record.get('progress', 0) >= 100)
        return completed / len(records)

    def _analyze_review_habit(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析复习习惯
        """
        if not records:
            return {}
        review_patterns = {
            'frequency': 0.0,
            'interval': 0.0,
            'duration': 0.0
        }
        course_reviews = {}
        for record in records:
            course_id = record.get('course_id', '')
            if course_id:
                if course_id not in course_reviews:
                    course_reviews[course_id] = []
                course_reviews[course_id].append(record)
        for course_records in course_reviews.values():
            if len(course_records) > 1:
                review_patterns['frequency'] += float(len(course_records))
                timestamps = [datetime.strptime(r['timestamp'], '%Y-%m-%d %H:%M:%S') 
                            for r in course_records]
                intervals = [(timestamps[i+1] - timestamps[i]).days 
                           for i in range(len(timestamps)-1)]
                review_patterns['interval'] += float(np.mean(intervals))
                durations = [float(r.get('duration', 0)) for r in course_records]
                review_patterns['duration'] += float(np.mean(durations))
        num_courses = len(course_reviews)
        if num_courses > 0:
            review_patterns['frequency'] /= num_courses
            review_patterns['interval'] /= num_courses
            review_patterns['duration'] /= num_courses
        return review_patterns

    def _analyze_learning_trend(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析学习趋势
        """
        if not records:
            return {}
        progress_rates = []
        for i in range(1, len(records)):
            time_diff = (datetime.strptime(records[i]['timestamp'], '%Y-%m-%d %H:%M:%S') -
                        datetime.strptime(records[i-1]['timestamp'], '%Y-%m-%d %H:%M:%S')).total_seconds()
            progress_diff = records[i].get('progress', 0) - records[i-1].get('progress', 0)
            if time_diff > 0:
                progress_rates.append(progress_diff / time_diff)
        return {
            'trend_direction': 'increasing' if np.mean(progress_rates) > 0 else 'decreasing',
            'trend_strength': abs(np.mean(progress_rates)),
            'volatility': np.std(progress_rates) if len(progress_rates) > 1 else 0
        }

    def _analyze_study_time(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析学习时间分布
        """
        if not records:
            return {}
        hourly_distribution = [0] * 24
        for record in records:
            hour = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S').hour
            duration = record.get('duration', 0)
            hourly_distribution[hour] += duration
        peak_hours = []
        threshold = np.mean(hourly_distribution) + np.std(hourly_distribution)
        for hour, duration in enumerate(hourly_distribution):
            if duration > threshold:
                peak_hours.append(hour)
        return {
            'hourly_distribution': hourly_distribution,
            'peak_hours': peak_hours,
            'total_study_time': sum(hourly_distribution),
            'average_daily_time': sum(hourly_distribution) / len(set(r['timestamp'][:10] for r in records))
        }

    def _calculate_progress_velocity(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算学习进度速度
        """
        if not records:
            return {}
        velocities = []
        accelerations = []
        for i in range(1, len(records)):
            time_diff = (datetime.strptime(records[i]['timestamp'], '%Y-%m-%d %H:%M:%S') -
                        datetime.strptime(records[i-1]['timestamp'], '%Y-%m-%d %H:%M:%S')).total_seconds()
            progress_diff = records[i].get('progress', 0) - records[i-1].get('progress', 0)
            
            if time_diff > 0:
                velocity = progress_diff / time_diff
                velocities.append(velocity)
                
                if i > 1:
                    prev_velocity = velocities[-2]
                    acceleration = (velocity - prev_velocity) / time_diff
                    accelerations.append(acceleration)
        
        return {
            'average_velocity': np.mean(velocities) if velocities else 0,
            'velocity_std': np.std(velocities) if len(velocities) > 1 else 0,
            'average_acceleration': np.mean(accelerations) if accelerations else 0
        }

    def _analyze_knowledge_retention(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析知识保持情况
        """
        if not records:
            return {}
        retention_data = {
            'review_effectiveness': 0,
            'forgetting_curve': [],
            'retention_rate': 0
        }
        course_records = {}
        for record in records:
            course_id = record.get('course_id', '')
            if course_id:
                if course_id not in course_records:
                    course_records[course_id] = []
                course_records[course_id].append(record)
        for course_id, course_data in course_records.items():
            if len(course_data) < 2:
                continue
            scores = [r.get('quiz_score', 0) for r in course_data]
            intervals = [(datetime.strptime(course_data[i+1]['timestamp'], '%Y-%m-%d %H:%M:%S') -
                         datetime.strptime(course_data[i]['timestamp'], '%Y-%m-%d %H:%M:%S')).days
                        for i in range(len(course_data)-1)]
            retention_rates = []
            for i in range(1, len(scores)):
                if scores[i-1] > 0:
                    retention_rates.append(scores[i] / scores[i-1])
            retention_data['retention_rate'] += np.mean(retention_rates) if retention_rates else 0
            retention_data['forgetting_curve'].append({
                'course_id': course_id,
                'intervals': intervals,
                'scores': scores
            })
        if course_records:
            retention_data['retention_rate'] /= len(course_records)
        return retention_data

    def _find_peak_hours(self, study_times: List[int]) -> List[int]:
        """
        找出学习高峰时段
        """
        if not study_times:
            return []
        hour_counts = [0] * 24
        for hour in study_times:
            hour_counts[hour] += 1
        mean_count = np.mean(hour_counts)
        std_count = np.std(hour_counts)
        peak_hours = [hour for hour, count in enumerate(hour_counts) 
                     if count > mean_count + 0.5 * std_count]
        return peak_hours

    def _calculate_average_session_length(self, records: List[Dict[str, Any]]) -> float:
        """
        计算平均学习时长
        """
        if not records:
            return 0.0
        session_lengths = []
        current_session = []
        for i in range(len(records)):
            if not current_session:
                current_session.append(records[i])
            else:
                time_diff = (datetime.strptime(records[i]['timestamp'], '%Y-%m-%d %H:%M:%S') -
                           datetime.strptime(current_session[-1]['timestamp'], '%Y-%m-%d %H:%M:%S')).total_seconds()
                
                if time_diff > 1800:
                    session_length = sum(r.get('duration', 0) for r in current_session)
                    session_lengths.append(session_length)
                    current_session = [records[i]]
                else:
                    current_session.append(records[i])
        
        if current_session:
            session_length = sum(r.get('duration', 0) for r in current_session)
            session_lengths.append(session_length)
        
        return float(np.mean(session_lengths)) if session_lengths else 0.0

    def _calculate_study_frequency(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算学习频率
        """
        if not records:
            return {}
        daily_counts = {}
        for record in records:
            date = record['timestamp'][:10]
            daily_counts[date] = daily_counts.get(date, 0) + 1
        counts = list(daily_counts.values())
        return {
            'average_daily_sessions': float(np.mean(counts)),
            'max_daily_sessions': float(np.max(counts)),
            'study_days_ratio': len(daily_counts) / ((datetime.strptime(records[-1]['timestamp'][:10], '%Y-%m-%d') -
                                                    datetime.strptime(records[0]['timestamp'][:10], '%Y-%m-%d')).days + 1)
        } 
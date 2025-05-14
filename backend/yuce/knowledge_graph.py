from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

class KnowledgeGraph:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        """
        初始化知识图谱
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            logger.error(f"Neo4j连接失败: {e}")
            self.driver = None

    def close(self):
        """
        关闭数据库连接
        """
        if self.driver:
            self.driver.close()

    def create_course_node(self, course_data: Dict[str, Any]) -> bool:
        """
        创建课程节点
        """
        if not self.driver:
            return False

        query = """
        MERGE (c:Course {id: $id})
        SET c.name = $name,
            c.category = $category,
            c.description = $description,
            c.difficulty = $difficulty
        """
        try:
            with self.driver.session() as session:
                session.run(query, 
                    id=course_data['课程ID'],
                    name=course_data['课程名称'],
                    category=course_data['课程分类'],
                    description=course_data['课程描述'],
                    difficulty=course_data.get('难度', 'medium')
                )
            return True
        except Exception as e:
            logger.error(f"创建课程节点失败: {e}")
            return False

    def create_knowledge_point(self, course_id: str, knowledge_data: Dict[str, Any]) -> bool:
        """
        创建知识点节点
        """
        if not self.driver:
            return False

        query = """
        MATCH (c:Course {id: $course_id})
        MERGE (k:KnowledgePoint {id: $k_id})
        SET k.name = $name,
            k.description = $description
        MERGE (c)-[r:CONTAINS]->(k)
        """
        try:
            with self.driver.session() as session:
                session.run(query,
                    course_id=course_id,
                    k_id=knowledge_data['id'],
                    name=knowledge_data['name'],
                    description=knowledge_data['description']
                )
            return True
        except Exception as e:
            logger.error(f"创建知识点失败: {e}")
            return False

    def create_skill_node(self, knowledge_id: str, skill_data: Dict[str, Any]) -> bool:
        """
        创建技能点节点
        """
        if not self.driver:
            return False

        query = """
        MATCH (k:KnowledgePoint {id: $k_id})
        MERGE (s:Skill {id: $s_id})
        SET s.name = $name,
            s.level = $level,
            s.description = $description
        MERGE (k)-[r:REQUIRES]->(s)
        """
        try:
            with self.driver.session() as session:
                session.run(query,
                    k_id=knowledge_id,
                    s_id=skill_data['id'],
                    name=skill_data['name'],
                    level=skill_data['level'],
                    description=skill_data['description']
                )
            return True
        except Exception as e:
            logger.error(f"创建技能点失败: {e}")
            return False

    def add_prerequisite_relation(self, course_id: str, prereq_id: str, weight: float) -> bool:
        """
        添加课程前置关系
        """
        if not self.driver:
            return False

        query = """
        MATCH (c1:Course {id: $course_id})
        MATCH (c2:Course {id: $prereq_id})
        MERGE (c2)-[r:PREREQUISITE]->(c1)
        SET r.weight = $weight
        """
        try:
            with self.driver.session() as session:
                session.run(query,
                    course_id=course_id,
                    prereq_id=prereq_id,
                    weight=weight
                )
            return True
        except Exception as e:
            logger.error(f"添加前置关系失败: {e}")
            return False

    def get_course_prerequisites(self, course_id: str) -> List[Dict[str, Any]]:
        """
        获取课程的前置课程
        """
        if not self.driver:
            return []

        query = """
        MATCH (c2:Course)-[r:PREREQUISITE]->(c1:Course {id: $course_id})
        RETURN c2.id as id, c2.name as name, r.weight as weight
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, course_id=course_id)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"获取前置课程失败: {e}")
            return []

    def get_knowledge_path(self, start_course_id: str, end_course_id: str) -> List[Dict[str, Any]]:
        """
        获取两个课程之间的知识路径
        """
        if not self.driver:
            return []

        query = """
        MATCH path = shortestPath((c1:Course {id: $start_id})-[*]->(c2:Course {id: $end_id}))
        UNWIND nodes(path) as node
        RETURN node.id as id, node.name as name, labels(node)[0] as type
        """
        try:
            with self.driver.session() as session:
                result = session.run(query,
                    start_id=start_course_id,
                    end_id=end_course_id
                )
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"获取知识路径失败: {e}")
            return []

    def get_course_knowledge_points(self, course_id: str) -> List[Dict[str, Any]]:
        """
        获取课程的所有知识点
        """
        if not self.driver:
            return []

        query = """
        MATCH (c:Course {id: $course_id})-[:CONTAINS]->(k:KnowledgePoint)
        RETURN k.id as id, k.name as name, k.description as description
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, course_id=course_id)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"获取知识点失败: {e}")
            return []

    def get_required_skills(self, knowledge_id: str) -> List[Dict[str, Any]]:
        """
        获取知识点需要的技能
        """
        if not self.driver:
            return []

        query = """
        MATCH (k:KnowledgePoint {id: $k_id})-[:REQUIRES]->(s:Skill)
        RETURN s.id as id, s.name as name, s.level as level, s.description as description
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, k_id=knowledge_id)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"获取技能需求失败: {e}")
            return []

    def get_course_difficulty(self, course_id: str) -> Dict[str, Any]:
        """
        获取课程难度信息
        """
        if not self.driver:
            return {}

        query = """
        MATCH (c:Course {id: $course_id})
        OPTIONAL MATCH (c)-[:CONTAINS]->(k:KnowledgePoint)-[:REQUIRES]->(s:Skill)
        WITH c, collect(distinct s.level) as skill_levels
        RETURN c.difficulty as base_difficulty, skill_levels
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, course_id=course_id).single()
                if result:
                    return {
                        'base_difficulty': result['base_difficulty'],
                        'skill_levels': result['skill_levels']
                    }
                return {}
        except Exception as e:
            logger.error(f"获取课程难度失败: {e}")
            return {} 
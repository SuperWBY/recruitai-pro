"""
模拟AI客户端，用于测试系统功能
"""
import json
from typing import Dict, List, Any
from datetime import datetime

class MockAIClient:
    """模拟AI客户端"""
    
    def __init__(self):
        self.api_key = "mock_api_key"
    
    def parse_resume(self, resume_content: str) -> Dict[str, Any]:
        """解析简历内容（模拟）"""
        return {
            "name": "张三",
            "contact_info": {
                "phone": "13800138000",
                "email": "zhangsan@example.com",
                "address": "北京市朝阳区"
            },
            "education": {
                "degree": "本科",
                "major": "计算机科学与技术",
                "school": "北京理工大学",
                "graduation_year": 2022
            },
            "work_experience": [
                {
                    "company": "腾讯科技",
                    "position": "后端开发工程师",
                    "duration": "2022-至今",
                    "description": "负责微信支付系统后端开发，使用Python、Java开发微服务架构"
                }
            ],
            "skills": ["Python", "Java", "JavaScript", "Django", "Spring Boot", "MySQL", "Redis"],
            "projects": [
                {
                    "name": "电商平台后端系统",
                    "description": "使用Python Django开发RESTful API，集成支付、物流、库存管理模块"
                }
            ]
        }
    
    def analyze_match(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """分析匹配度（模拟）"""
        return {
            "match_score": 85.0,
            "skills_analysis": {
                "required_skills": ["Python", "Django", "微服务", "MySQL", "Redis"],
                "candidate_skills": ["Python", "Java", "JavaScript", "Django", "Spring Boot", "MySQL", "Redis"],
                "matched_skills": ["Python", "Django", "MySQL", "Redis"],
                "missing_skills": ["微服务"],
                "skill_scores": {
                    "Python": 90.0,
                    "Django": 85.0,
                    "MySQL": 80.0,
                    "Redis": 75.0,
                    "微服务": 60.0
                }
            },
            "experience_analysis": {
                "total_experience": 2.0,
                "relevant_experience": 2.0,
                "company_count": 1,
                "position_progression": ["后端开发工程师"],
                "industry_experience": ["互联网", "支付系统"]
            },
            "education_analysis": {
                "degree_level": "本科",
                "major": "计算机科学与技术",
                "school": "北京理工大学",
                "graduation_year": 2022,
                "education_score": 85.0
            },
            "strengths": ["技术栈匹配度高", "大厂经验", "项目经验丰富", "学习能力强"],
            "weaknesses": ["微服务经验较少", "工作年限较短"],
            "potential": "该候选人技术能力突出，经验丰富，是优秀的候选人选择。"
        }
    
    def generate_interview_questions(self, resume_data: Dict[str, Any], job_description: str, analysis_result: Dict[str, Any]) -> List[str]:
        """生成面试问题（模拟）"""
        return [
            "请介绍一下您最擅长的技术栈？",
            "描述一个您解决过的技术难题？",
            "您在团队项目中通常扮演什么角色？",
            "您如何学习新的技术？",
            "您的职业规划是什么？",
            "描述一个您主导的项目？",
            "您如何处理工作中的压力？",
            "您认为自己的优势是什么？",
            "您希望从这份工作中获得什么？",
            "您还有什么问题要问我们？"
        ]
    
    def generate_analysis_report(self, resume_data: Dict[str, Any], job_description: str, analysis_result: Dict[str, Any], interview_questions: List[str]) -> str:
        """生成分析报告（模拟）"""
        return f"""
# 候选人分析报告

## 基本信息
- **姓名**: {resume_data['name']}
- **联系方式**: {resume_data['contact_info']['phone']} | {resume_data['contact_info']['email']}

## 匹配度分析
- **总体匹配度**: {analysis_result['match_score']}%
- **技能匹配**: 候选人在Python、Django、MySQL、Redis等核心技能方面表现优秀
- **经验匹配**: 具有2年相关工作经验，在腾讯科技担任后端开发工程师
- **教育背景**: 北京理工大学计算机科学与技术本科，符合要求

## 优势分析
1. **技术栈匹配度高**: 熟练掌握Python、Django等核心技术
2. **大厂经验**: 在腾讯科技有实际工作经验
3. **项目经验丰富**: 参与过电商平台等大型项目开发
4. **学习能力强**: 能够快速掌握新技术

## 潜在关注点
1. **微服务经验**: 在微服务架构方面经验相对较少
2. **工作年限**: 工作经验相对较短，需要更多指导

## 推荐评级: A级候选人
该候选人技术能力突出，经验丰富，是优秀的候选人选择。
        """
    
    def generate_chart_data(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成图表数据（模拟）"""
        return {
            "match_score_chart": {
                "type": "gauge",
                "data": {
                    "value": analysis_result['match_score'],
                    "max": 100,
                    "title": "匹配度评分"
                }
            },
            "skills_chart": {
                "type": "radar",
                "data": {
                    "categories": ["Python", "Django", "MySQL", "Redis", "微服务"],
                    "values": [90, 85, 80, 75, 60]
                }
            },
            "experience_chart": {
                "type": "bar",
                "data": {
                    "categories": ["总经验", "相关经验"],
                    "values": [2.0, 2.0]
                }
            },
            "education_chart": {
                "type": "pie",
                "data": {
                    "labels": ["本科", "硕士", "博士"],
                    "values": [85, 10, 5]
                }
            }
        }
    
    def comprehensive_analysis(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """综合分析：一次API调用完成所有分析任务（模拟版本）"""
        return {
            "match_score": 85.0,
            "skills_analysis": {
                "required_skills": ["Python", "Django", "微服务", "MySQL", "Redis"],
                "candidate_skills": ["Python", "Java", "JavaScript", "Django", "Spring Boot", "MySQL", "Redis"],
                "matched_skills": ["Python", "Django", "MySQL", "Redis"],
                "missing_skills": ["微服务"],
                "skill_scores": {
                    "Python": 90.0,
                    "Django": 85.0,
                    "MySQL": 80.0,
                    "Redis": 75.0,
                    "微服务": 60.0
                }
            },
            "experience_analysis": {
                "total_experience": 3.5,
                "relevant_experience": 2.8,
                "company_count": 2,
                "position_progression": "初级开发 -> 高级开发",
                "industry_experience": "互联网、电商"
            },
            "education_analysis": {
                "degree_level": "本科",
                "major": "计算机科学与技术",
                "school": "某某大学",
                "graduation_year": 2020,
                "education_score": 85.0
            },
            "strengths": [
                "技术基础扎实，熟悉Python开发",
                "有实际项目经验",
                "学习能力强",
                "团队合作意识好"
            ],
            "weaknesses": [
                "微服务架构经验不足",
                "大型系统设计经验有限"
            ],
            "potential": "候选人具备良好的技术基础和学习能力，通过培训可以快速适应岗位要求，有较大的发展潜力。"
        }

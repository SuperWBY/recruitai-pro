"""
数据模型定义
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Candidate(Base):
    """候选人表"""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False, comment="简历文件名")
    file_path = Column(String(500), nullable=False, comment="简历文件路径")
    resume_content = Column(Text, comment="简历解析内容")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

class JobDescription(Base):
    """职位描述表"""
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False, comment="关联候选人ID")
    job_description = Column(Text, nullable=False, comment="职位描述内容")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")

class AnalysisResult(Base):
    """分析结果表"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False, comment="关联候选人ID")
    job_description_id = Column(Integer, nullable=False, comment="关联职位描述ID")
    match_score = Column(Float, comment="匹配度评分(0-100)")
    skills_analysis = Column(JSON, comment="技能分析结果")
    experience_analysis = Column(JSON, comment="经验分析结果")
    education_analysis = Column(JSON, comment="教育背景分析结果")
    interview_questions = Column(JSON, comment="面试问题列表")
    questions_generated = Column(Boolean, default=False, comment="面试问题是否已生成")
    candidate_profile = Column(JSON, comment="候选人画像")
    analysis_report = Column(Text, comment="完整分析报告")
    chart_data = Column(JSON, comment="图表数据")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

# Pydantic模型用于API响应
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class FileUploadResponse(BaseModel):
    """文件上传响应"""
    file_id: int
    file_name: str
    status: str
    message: str

class ProcessRequest(BaseModel):
    """处理请求"""
    file_id: int
    job_description: str

class SkillAnalysis(BaseModel):
    """技能分析"""
    required_skills: List[str]
    candidate_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    skill_scores: Dict[str, float]

class ExperienceAnalysis(BaseModel):
    """经验分析"""
    total_experience: float
    relevant_experience: float
    company_count: int
    position_progression: List[str]
    industry_experience: List[str]

class EducationAnalysis(BaseModel):
    """教育背景分析"""
    degree_level: str
    major: str
    school: str
    graduation_year: Optional[int]
    education_score: float

class CandidateProfile(BaseModel):
    """候选人画像"""
    name: str
    contact_info: Dict[str, str]
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    potential: str

class AnalysisResultResponse(BaseModel):
    """分析结果响应"""
    match_score: float
    skills_analysis: SkillAnalysis
    experience_analysis: ExperienceAnalysis
    education_analysis: EducationAnalysis
    interview_questions: List[str]  # 改回字符串数组，与AI返回格式一致
    candidate_profile: CandidateProfile
    analysis_report: str
    chart_data: Dict[str, Any]
    created_at: datetime

class ErrorResponse(BaseModel):
    """错误响应"""
    error: str
    message: str
    detail: Optional[str] = None

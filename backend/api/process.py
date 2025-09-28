"""
AI分析处理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import (
    Candidate, 
    JobDescription, 
    AnalysisResult, 
    ProcessRequest, 
    AnalysisResultResponse,
    SkillAnalysis,
    ExperienceAnalysis,
    EducationAnalysis,
    CandidateProfile
)
from ai_client import ZhipuClient
from mock_ai_client import MockAIClient
from utils import calculate_match_score
import json
import os
from datetime import datetime

router = APIRouter(prefix="/api", tags=["process"])

@router.post("/process", response_model=AnalysisResultResponse)
async def process_analysis(
    request: ProcessRequest,
    db: Session = Depends(get_db)
):
    """处理简历分析和匹配"""
    try:
        # 获取候选人信息
        candidate = db.query(Candidate).filter(Candidate.id == request.file_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="候选人文件不存在")
        
        if not candidate.resume_content:
            raise HTTPException(status_code=400, detail="简历内容为空，无法进行分析")
        
        # 保存职位描述
        job_desc = JobDescription(
            candidate_id=request.file_id,
            job_description=request.job_description
        )
        db.add(job_desc)
        db.commit()
        db.refresh(job_desc)
        
        # 初始化AI客户端（根据环境变量选择）
        use_mock = os.getenv("USE_MOCK_AI", "true").lower() == "true"
        if use_mock:
            ai_client = MockAIClient()
            print("使用模拟AI客户端")
        else:
            ai_client = ZhipuClient()
            print("使用真实AI客户端")
        
        # 超级优化的AI分析流程：减少API调用次数
        print("🚀 开始超级优化AI分析...")
        
        # 第一步：解析简历
        print("📄 解析简历...")
        resume_data = ai_client.parse_resume(candidate.resume_content)
        print("✅ 简历解析完成")
        
        # 第二步：综合分析（一次API调用完成所有分析）
        print("🎯 执行综合分析（匹配度+技能+经验+教育+优势劣势+潜力）...")
        analysis_result = ai_client.comprehensive_analysis(resume_data, request.job_description)
        print("✅ 综合分析完成")
        
        # 第三步：生成图表数据和报告（不包含面试问题）
        import concurrent.futures
        
        print("🔄 并发执行：生成图表数据和分析报告...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # 提交图表数据生成任务
            chart_future = executor.submit(
                ai_client.generate_chart_data, analysis_result
            )
            
            # 提交报告生成任务（不包含面试问题）
            report_future = executor.submit(
                ai_client.generate_analysis_report, resume_data, request.job_description, analysis_result, []
            )
            
            # 等待两个任务完成
            chart_data = chart_future.result()
            analysis_report = report_future.result()
            
        print("✅ 图表数据和分析报告生成完成")
        
        print("🎉 超级优化AI分析完成！总耗时大幅减少！")
        
        # 创建候选人画像
        candidate_profile = CandidateProfile(
            name=resume_data.get("name", "未知"),
            contact_info=resume_data.get("contact_info", {}),
            summary=resume_data.get("summary", ""),
            strengths=analysis_result.get("strengths", []),
            weaknesses=analysis_result.get("weaknesses", []),
            potential=analysis_result.get("potential", "")
        )
        
        # 保存分析结果
        db_analysis = AnalysisResult(
            candidate_id=request.file_id,
            job_description_id=job_desc.id,
            match_score=analysis_result.get("match_score", 0),
            skills_analysis=analysis_result.get("skills_analysis", {}),
            experience_analysis=analysis_result.get("experience_analysis", {}),
            education_analysis=analysis_result.get("education_analysis", {}),
            interview_questions=[],  # 初始为空
            questions_generated=False,  # 标记为未生成
            candidate_profile=candidate_profile.dict(),
            analysis_report=analysis_report,
            chart_data=chart_data
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # 构建响应数据
        print(f"Debug - analysis_result keys: {list(analysis_result.keys())}")
        print(f"Debug - match_score: {analysis_result.get('match_score')}")
        
        response_data = AnalysisResultResponse(
            match_score=analysis_result.get("match_score", 0),
            skills_analysis=SkillAnalysis(**analysis_result.get("skills_analysis", {})),
            experience_analysis=ExperienceAnalysis(**analysis_result.get("experience_analysis", {})),
            education_analysis=EducationAnalysis(**analysis_result.get("education_analysis", {})),
            interview_questions=[],  # 初始为空，不返回面试问题
            candidate_profile=candidate_profile,
            analysis_report=analysis_report,
            chart_data=chart_data,
            created_at=datetime.now()
        )
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析处理失败: {str(e)}")

@router.get("/process/{file_id}/history")
async def get_analysis_history(file_id: int, db: Session = Depends(get_db)):
    """获取候选人的分析历史"""
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人文件不存在")
    
    # 获取所有分析结果
    analyses = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).all()
    
    history = []
    for analysis in analyses:
        job_desc = db.query(JobDescription).filter(
            JobDescription.id == analysis.job_description_id
        ).first()
        
        history.append({
            "id": analysis.id,
            "job_description": job_desc.job_description if job_desc else "",
            "match_score": analysis.match_score,
            "created_at": analysis.created_at,
            "updated_at": analysis.updated_at
        })
    
    return {"history": history}

@router.get("/process/{analysis_id}")
async def get_analysis_result(analysis_id: int, db: Session = Depends(get_db)):
    """获取特定分析结果"""
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    # 获取关联的职位描述
    job_desc = db.query(JobDescription).filter(
        JobDescription.id == analysis.job_description_id
    ).first()
    
    return {
        "id": analysis.id,
        "candidate_id": analysis.candidate_id,
        "job_description": job_desc.job_description if job_desc else "",
        "match_score": analysis.match_score,
        "skills_analysis": analysis.skills_analysis,
        "experience_analysis": analysis.experience_analysis,
        "education_analysis": analysis.education_analysis,
        "interview_questions": analysis.interview_questions,
        "candidate_profile": analysis.candidate_profile,
        "analysis_report": analysis.analysis_report,
        "chart_data": analysis.chart_data,
        "created_at": analysis.created_at,
        "updated_at": analysis.updated_at
    }

@router.post("/process/{analysis_id}/regenerate")
async def regenerate_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """重新生成分析结果"""
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    try:
        # 获取关联数据
        candidate = db.query(Candidate).filter(Candidate.id == analysis.candidate_id).first()
        job_desc = db.query(JobDescription).filter(JobDescription.id == analysis.job_description_id).first()
        
        if not candidate or not job_desc:
            raise HTTPException(status_code=404, detail="关联数据不存在")
        
        # 重新分析（使用优化流程）
        use_mock = os.getenv("USE_MOCK_AI", "true").lower() == "true"
        if use_mock:
            ai_client = MockAIClient()
            print("重新分析：使用模拟AI客户端")
        else:
            ai_client = ZhipuClient()
            print("重新分析：使用真实AI客户端")
        
        print("🔄 开始重新分析...")
        
        # 解析简历
        resume_data = ai_client.parse_resume(candidate.resume_content)
        print("✅ 简历解析完成")
        
        # 综合分析（一次API调用完成所有分析）
        analysis_result = ai_client.comprehensive_analysis(resume_data, job_desc.job_description)
        print("✅ 综合分析完成")
        
        # 提取数据
        interview_questions = analysis_result.get("interview_questions", [])
        
        # 并发生成图表数据和报告
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            chart_future = executor.submit(ai_client.generate_chart_data, analysis_result)
            report_future = executor.submit(
                ai_client.generate_analysis_report, resume_data, job_desc.job_description, analysis_result, interview_questions
            )
            
            chart_data = chart_future.result()
            analysis_report = report_future.result()
        
        print("✅ 重新分析完成")
        
        # 更新分析结果
        analysis.match_score = analysis_result.get("match_score", 0)
        analysis.skills_analysis = analysis_result.get("skills_analysis", {})
        analysis.experience_analysis = analysis_result.get("experience_analysis", {})
        analysis.education_analysis = analysis_result.get("education_analysis", {})
        analysis.interview_questions = interview_questions
        analysis.analysis_report = analysis_report
        analysis.chart_data = chart_data
        
        db.commit()
        db.refresh(analysis)
        
        return {"message": "分析结果重新生成成功", "analysis_id": analysis.id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重新生成失败: {str(e)}")

@router.post("/process/{file_id}/generate-questions")
async def generate_interview_questions(
    file_id: int,
    db: Session = Depends(get_db)
):
    """生成面试问题"""
    # 通过文件ID找到最新的分析结果
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    # 如果已经生成过面试问题，直接返回
    if analysis.questions_generated:
        return {
            "interview_questions": analysis.interview_questions,
            "questions_generated": True,
            "message": "面试问题已存在"
        }
    
    try:
        # 获取关联数据
        candidate = db.query(Candidate).filter(Candidate.id == analysis.candidate_id).first()
        job_desc = db.query(JobDescription).filter(JobDescription.id == analysis.job_description_id).first()
        
        if not candidate or not job_desc:
            raise HTTPException(status_code=404, detail="关联数据不存在")
        
        # 初始化AI客户端
        use_mock = os.getenv("USE_MOCK_AI", "true").lower() == "true"
        if use_mock:
            ai_client = MockAIClient()
            print("生成面试问题：使用模拟AI客户端")
        else:
            ai_client = ZhipuClient()
            print("生成面试问题：使用真实AI客户端")
        
        print("🎯 开始生成面试问题...")
        
        # 解析简历
        resume_data = ai_client.parse_resume(candidate.resume_content)
        print("✅ 简历解析完成")
        
        # 构建分析结果数据用于生成面试问题
        analysis_data = {
            "match_score": analysis.match_score,
            "skills_analysis": analysis.skills_analysis,
            "experience_analysis": analysis.experience_analysis,
            "education_analysis": analysis.education_analysis,
            "strengths": analysis.candidate_profile.get("strengths", []),
            "weaknesses": analysis.candidate_profile.get("weaknesses", []),
            "potential": analysis.candidate_profile.get("potential", "")
        }
        
        # 生成面试问题
        interview_questions = ai_client.generate_interview_questions(
            resume_data, job_desc.job_description, analysis_data
        )
        print("✅ 面试问题生成完成")
        
        # 更新数据库
        analysis.interview_questions = interview_questions
        analysis.questions_generated = True
        db.commit()
        db.refresh(analysis)
        
        return {
            "interview_questions": interview_questions,
            "questions_generated": True,
            "message": "面试问题生成成功"
        }
        
    except Exception as e:
        print(f"生成面试问题失败: {e}")
        raise HTTPException(status_code=500, detail=f"生成面试问题失败: {str(e)}")

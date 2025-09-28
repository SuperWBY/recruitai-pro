"""
报告生成API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import AnalysisResult, Candidate, JobDescription
from typing import Dict, Any
import json

router = APIRouter(prefix="/api", tags=["report"])

@router.get("/report/{file_id}")
async def get_candidate_report(file_id: int, db: Session = Depends(get_db)):
    """获取候选人完整分析报告"""
    # 获取候选人信息
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    # 获取最新的分析结果
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    # 获取职位描述
    job_desc = db.query(JobDescription).filter(
        JobDescription.id == analysis.job_description_id
    ).first()
    
    return {
        "candidate_info": {
            "id": candidate.id,
            "file_name": candidate.file_name,
            "created_at": candidate.created_at
        },
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

@router.get("/report/{file_id}/summary")
async def get_report_summary(file_id: int, db: Session = Depends(get_db)):
    """获取报告摘要"""
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    return {
        "match_score": analysis.match_score,
        "candidate_name": analysis.candidate_profile.get("name", "未知"),
        "summary": analysis.candidate_profile.get("summary", ""),
        "strengths": analysis.candidate_profile.get("strengths", []),
        "weaknesses": analysis.candidate_profile.get("weaknesses", []),
        "potential": analysis.candidate_profile.get("potential", ""),
        "created_at": analysis.created_at
    }

@router.get("/report/{file_id}/charts")
async def get_chart_data(file_id: int, db: Session = Depends(get_db)):
    """获取图表数据"""
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    return {
        "chart_data": analysis.chart_data,
        "match_score": analysis.match_score
    }

@router.get("/report/{file_id}/questions")
async def get_interview_questions(file_id: int, db: Session = Depends(get_db)):
    """获取面试问题"""
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    return {
        "questions": analysis.interview_questions,
        "total_count": len(analysis.interview_questions)
    }

@router.get("/reports")
async def list_all_reports(db: Session = Depends(get_db)):
    """获取所有报告列表"""
    analyses = db.query(AnalysisResult).order_by(AnalysisResult.created_at.desc()).all()
    
    reports = []
    for analysis in analyses:
        candidate = db.query(Candidate).filter(Candidate.id == analysis.candidate_id).first()
        job_desc = db.query(JobDescription).filter(JobDescription.id == analysis.job_description_id).first()
        
        reports.append({
            "analysis_id": analysis.id,
            "candidate_id": analysis.candidate_id,
            "candidate_name": analysis.candidate_profile.get("name", "未知"),
            "file_name": candidate.file_name if candidate else "未知文件",
            "match_score": analysis.match_score,
            "job_description": job_desc.job_description[:100] + "..." if job_desc and len(job_desc.job_description) > 100 else job_desc.job_description if job_desc else "",
            "created_at": analysis.created_at
        })
    
    return {"reports": reports}

@router.post("/report/{file_id}/export")
async def export_report(file_id: int, db: Session = Depends(get_db)):
    """导出报告（返回可打印的HTML格式）"""
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.candidate_id == file_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    job_desc = db.query(JobDescription).filter(JobDescription.id == analysis.job_description_id).first()
    
    # 生成HTML报告
    html_content = generate_html_report(
        candidate, job_desc, analysis
    )
    
    return {
        "html_content": html_content,
        "export_time": analysis.updated_at.isoformat()
    }

def generate_html_report(candidate, job_desc, analysis) -> str:
    """生成HTML格式的报告"""
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>候选人分析报告</title>
        <style>
            body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #007bff; padding-bottom: 20px; }}
            .header h1 {{ color: #007bff; margin: 0; }}
            .header .meta {{ color: #666; margin-top: 10px; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ color: #333; border-left: 4px solid #007bff; padding-left: 15px; margin-bottom: 15px; }}
            .score-display {{ text-align: center; margin: 20px 0; }}
            .score-circle {{ 
                display: inline-block; 
                width: 120px; 
                height: 120px; 
                border-radius: 50%; 
                background: conic-gradient(#007bff {score_percent}%, #e9ecef {score_percent}%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
            .skills-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
            .skill-item {{ background: #f8f9fa; padding: 10px; border-radius: 5px; }}
            .questions-list {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
            .questions-list ol {{ margin: 0; padding-left: 20px; }}
            .questions-list li {{ margin-bottom: 8px; }}
            .profile-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .strengths {{ color: #28a745; }}
            .weaknesses {{ color: #dc3545; }}
            .report-content {{ white-space: pre-line; background: #f8f9fa; padding: 20px; border-radius: 5px; }}
            @media print {{ body {{ margin: 0; }} .section {{ page-break-inside: avoid; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>候选人分析报告</h1>
            <div class="meta">
                <p>候选人：{candidate_name} | 文件：{file_name} | 生成时间：{created_at}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>匹配度评分</h2>
            <div class="score-display">
                <div class="score-circle">{match_score}分</div>
            </div>
        </div>
        
        <div class="section">
            <h2>候选人画像</h2>
            <div class="profile-grid">
                <div>
                    <h3>基本信息</h3>
                    <p><strong>姓名：</strong>{candidate_name}</p>
                    <p><strong>联系方式：</strong>{contact_info}</p>
                    <p><strong>个人简介：</strong>{summary}</p>
                </div>
                <div>
                    <h3>核心特点</h3>
                    <p><strong>优势：</strong></p>
                    <ul class="strengths">
                        {strengths_list}
                    </ul>
                    <p><strong>不足：</strong></p>
                    <ul class="weaknesses">
                        {weaknesses_list}
                    </ul>
                </div>
            </div>
            <p><strong>发展潜力：</strong>{potential}</p>
        </div>
        
        <div class="section">
            <h2>技能分析</h2>
            <div class="skills-grid">
                <div class="skill-item">
                    <h4>候选技能</h4>
                    <p>{candidate_skills}</p>
                </div>
                <div class="skill-item">
                    <h4>匹配技能</h4>
                    <p>{matched_skills}</p>
                </div>
                <div class="skill-item">
                    <h4>缺失技能</h4>
                    <p>{missing_skills}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>面试问题</h2>
            <div class="questions-list">
                <ol>
                    {questions_list}
                </ol>
            </div>
        </div>
        
        <div class="section">
            <h2>详细分析报告</h2>
            <div class="report-content">{analysis_report}</div>
        </div>
        
        <div class="section">
            <h2>职位描述</h2>
            <div class="report-content">{job_description}</div>
        </div>
    </body>
    </html>
    """
    
    # 填充模板数据
    candidate_name = analysis.candidate_profile.get("name", "未知")
    contact_info = ", ".join([f"{k}: {v}" for k, v in analysis.candidate_profile.get("contact_info", {}).items()])
    summary = analysis.candidate_profile.get("summary", "")
    strengths = analysis.candidate_profile.get("strengths", [])
    weaknesses = analysis.candidate_profile.get("weaknesses", [])
    potential = analysis.candidate_profile.get("potential", "")
    
    strengths_list = "".join([f"<li>{s}</li>" for s in strengths])
    weaknesses_list = "".join([f"<li>{w}</li>" for w in weaknesses])
    
    skills_analysis = analysis.skills_analysis or {}
    candidate_skills = ", ".join(skills_analysis.get("candidate_skills", []))
    matched_skills = ", ".join(skills_analysis.get("matched_skills", []))
    missing_skills = ", ".join(skills_analysis.get("missing_skills", []))
    
    questions_list = "".join([f"<li>{q}</li>" for q in (analysis.interview_questions or [])])
    
    # 计算评分百分比用于CSS
    score_percent = (analysis.match_score or 0) * 3.6  # 转换为角度
    
    return html_template.format(
        candidate_name=candidate_name,
        file_name=candidate.file_name if candidate else "未知",
        created_at=analysis.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        match_score=analysis.match_score or 0,
        contact_info=contact_info,
        summary=summary,
        strengths_list=strengths_list,
        weaknesses_list=weaknesses_list,
        potential=potential,
        candidate_skills=candidate_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        questions_list=questions_list,
        analysis_report=analysis.analysis_report or "",
        job_description=job_desc.job_description if job_desc else "",
        score_percent=score_percent
    )

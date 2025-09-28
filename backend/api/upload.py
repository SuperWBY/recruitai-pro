"""
文件上传API
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Candidate, FileUploadResponse
import mimetypes
from utils import (
    validate_file, 
    generate_unique_filename, 
    save_uploaded_file, 
    extract_text_from_file,
    clean_text
)
from ai_client import ZhipuClient
import os

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传简历文件"""
    try:
        # 验证文件
        is_valid, message = validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # 生成唯一文件名
        filename = generate_unique_filename(file.filename)
        
        # 保存文件
        file_path = save_uploaded_file(file, filename)
        
        # 提取文件内容
        try:
            raw_content = extract_text_from_file(file_path)
            cleaned_content = clean_text(raw_content)
        except Exception as e:
            # 如果文件解析失败，仍然保存文件记录，但标记内容为空
            cleaned_content = f"文件解析失败: {str(e)}"
        
        # 保存到数据库
        candidate = Candidate(
            file_name=file.filename,
            file_path=file_path,
            resume_content=cleaned_content
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        
        return FileUploadResponse(
            file_id=candidate.id,
            file_name=file.filename,
            status="success",
            message="文件上传成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/file/{file_id}")
async def get_file_info(file_id: int, db: Session = Depends(get_db)):
    """获取文件信息"""
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return {
        "id": candidate.id,
        "file_name": candidate.file_name,
        "file_path": candidate.file_path,
        "created_at": candidate.created_at,
        "file_size": os.path.getsize(candidate.file_path) if os.path.exists(candidate.file_path) else 0
    }

@router.delete("/file/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    """删除文件"""
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        # 删除物理文件
        if os.path.exists(candidate.file_path):
            os.remove(candidate.file_path)
        
        # 删除数据库记录
        db.delete(candidate)
        db.commit()
        
        return {"message": "文件删除成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")

@router.get("/files")
async def list_files(db: Session = Depends(get_db)):
    """获取文件列表"""
    candidates = db.query(Candidate).order_by(Candidate.created_at.desc()).all()
    
    files = []
    for candidate in candidates:
        file_exists = os.path.exists(candidate.file_path)
        files.append({
            "id": candidate.id,
            "file_name": candidate.file_name,
            "created_at": candidate.created_at,
            "file_size": os.path.getsize(candidate.file_path) if file_exists else 0,
            "status": "存在" if file_exists else "文件丢失"
        })
    
    return {"files": files}

@router.get("/file/{file_id}/download")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    """下载简历文件"""
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if not os.path.exists(candidate.file_path):
        raise HTTPException(status_code=404, detail="物理文件不存在")
    
    # 获取文件的MIME类型
    mime_type, _ = mimetypes.guess_type(candidate.file_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    
    return FileResponse(
        path=candidate.file_path,
        filename=candidate.file_name,
        media_type=mime_type,
        headers={
            "Content-Disposition": f"attachment; filename=\"{candidate.file_name}\""
        }
    )

@router.get("/file/{file_id}/preview")
async def preview_file(file_id: int, db: Session = Depends(get_db)):
    """在线预览简历文件"""
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if not os.path.exists(candidate.file_path):
        raise HTTPException(status_code=404, detail="物理文件不存在")
    
    # 获取文件的MIME类型
    mime_type, _ = mimetypes.guess_type(candidate.file_path)
    
    # 如果是PDF文件，返回PDF预览
    if mime_type == "application/pdf":
        return FileResponse(
            path=candidate.file_path,
            media_type="application/pdf",
            headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": "inline"
            }
        )
    
    # 如果是图片文件，返回图片预览
    elif mime_type and mime_type.startswith("image/"):
        return FileResponse(
            path=candidate.file_path,
            media_type=mime_type,
            headers={
                "Content-Type": mime_type,
                "Content-Disposition": "inline"
            }
        )
    
    # 其他文件类型，返回文本内容
    else:
        try:
            with open(candidate.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(candidate.file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except:
                content = "文件内容无法预览"
        
        return JSONResponse(content={
            "file_name": candidate.file_name,
            "content": content,
            "file_type": mime_type or "text/plain"
        })

@router.get("/file/{file_id}/content")
async def get_file_content(file_id: int, db: Session = Depends(get_db)):
    """获取简历文本内容"""
    candidate = db.query(Candidate).filter(Candidate.id == file_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return {
        "file_id": candidate.id,
        "file_name": candidate.file_name,
        "content": candidate.resume_content,
        "created_at": candidate.created_at
    }

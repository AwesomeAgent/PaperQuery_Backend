# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from core.backend.crud.crud import get_document_by_knowledgeID
import dotenv

from core.backend.utils.utils import get_current_user, get_db
dotenv.load_dotenv()

from fastapi import Depends,File, UploadFile,Form,Path
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import hashlib

from core.backend.crud.crud import *
from core.backend.schema import *
from core.agent.dataprocessAgent import *
from core.agent.chatAgent import *
from core.vectordb.chromadb import *
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()

@router.get("/document/getDocumentList")
async def get_documents_all(knowledgeID:str, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    documents=get_document_by_knowledgeID(db, knowledgeID)
    filtered_documents = [{"documentID": doc.uid,"documentName":doc.documentName, "documentStatus": doc.documentStatus,"documentTags":['tage1','tage2' ,'tage3'],"vectorNum":doc.documentVector,"createTime":doc.createTime_timestamp} for doc in documents]
    return {
            "status_code": 200, 
            "msg":"Get document list successfully", 
            "data":filtered_documents
            }

# 获取document的状态
@router.get("/document/Info")
async def get_document_info(documentID: str,knowledgeID:str,token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user =await get_current_user(token,db)
    print(documentID,knowledgeID)
    paper =db.query(Paper).filter(Paper.uid == documentID,Paper.knowledgeID==knowledgeID).first()
    return {
        "status_code": 200,
        "msg": "Get document info successfully",
        "data": {
            "documentID": paper.uid,
            "documentName": paper.documentName,
            "documentStatus": paper.documentStatus,
            "vectorNum": paper.documentVector,
            "documentTags": paper.tags,
        }
    }

## 根据documentID获取pdf文件
@router.get("/document/getFile")
def get_document(documentID: str,db: Session = Depends(get_db)):
    agent_path = Path.cwd()
    paper =db.query(Paper).filter(Paper.uid == documentID).first()
    if not paper:
        return {
            "status_code": 404,
            "msg": "document not found",
        }
    file_path =os.getenv("AcadeAgent_DIR")+paper.documentPath
    print("File_path",file_path) # 替换成你实际的 PDF 文件路径
    return FileResponse(file_path)

## 多文件上传
@router.post("/document/uploads")
async def  upload_document(knowledgeID:str=Form(),documentFile: List[UploadFile] = File(...), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    agent_path = Path.cwd()
    res_path=Path(agent_path,"res/pdf/")
    pdf_storage_path = res_path
    user =await get_current_user(token,db)
    for file in documentFile:
        print("saving ",file.filename,"...")
        file_path=os.path.join(pdf_storage_path,file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        uid=cal_file_md5(file_path)
        createtime=datetime.datetime.now(timezone.utc)
        ###检测是否已经存在
        paper =db.query(Paper).filter(Paper.uid == uid).first()
        if paper:
            #代表用户已经上传过该文件 or 其他知识中存在该文件 todo: 复制文件状态
            print("file ",file.filename," already exists")
            continue
        ###

        paper = PaperCreate(documentName=file.filename,documentPath=os.path.join("/res/pdf/",file.filename),documentStatus=0,uid=uid,knowledgeID=knowledgeID,lid=user.lid,createTime=createtime)
        print(paper.documentPath)
        create_paper(db=db, paper=paper)
    return {
        "status_code": 200,
        "msg": "upload successfully",
        "data": {
            "documentID": uid,
            "documentName": file.filename,
            "documentStatus": 0,
            "documentTags": [],
            "knowledgeID": knowledgeID,
            "vectorNum": 0,
            "createTime": int(createtime.timestamp())
        }
    }




## 单文件上传
@router.post("/document/upload")
async def  upload_document(knowledgeID:str=Form(),documentFile:UploadFile=File, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    agent_path = Path.cwd()
    res_path=Path(agent_path,"res/pdf/")
    pdf_storage_path = res_path
    user =await get_current_user(token,db)

        # 计算文件的MD5哈希值
    hasher = hashlib.md5()
    file_content = await documentFile.read()
    hasher.update(file_content)
    file_md5 = hasher.hexdigest()
    print("FILE_MD5",file_md5)
    paper =db.query(Paper).filter(Paper.uid ==file_md5).first()
    if paper:
        #代表用户已经上传过该文件 or 其他知识中存在该文件 todo: 复制文件状态

        ### 如果其他知识中已经存在这个Paper则拷贝其状态
        return {
                "status_code": 409,
                "msg": "document already exists",
        }
        
    # 重置文件内容读取位置，以便后续写入文件
    documentFile.file.seek(0)
    print("saving ",documentFile.filename,"...")
    file_path=os.path.join(pdf_storage_path,documentFile.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(documentFile.file.read())
    uid=cal_file_md5(file_path)
    print("UID",uid)
    createtime=datetime.datetime.now(timezone.utc)
    paper = PaperCreate(documentName=documentFile.filename,documentPath=os.path.join("/res/pdf/",documentFile.filename),documentStatus=0,uid=uid,knowledgeID=knowledgeID,lid=user.lid,createTime=createtime)

    create_paper(db=db, paper=paper)
    return {
        "status_code": 200,
        "msg": "upload successfully",
        "data": {
            "documentID": uid,
            "documentName": documentFile.filename,
            "documentStatus": 0,
            "documentTags": [],
            "knowledgeID": knowledgeID,
            "vectorNum": 0,
            "createTime": int(createtime.timestamp())
        }
    }
# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends,status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer

import dotenv

from core.backend.crud.crud_document import *
from core.backend.utils.utils import get_current_user, get_db
dotenv.load_dotenv()

from fastapi import Depends, FastAPI, HTTPException ,File, UploadFile,Form,Path
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import hashlib


from core.backend.schema.schema import *
from core.agent.dataprocessAgent import *
from core.agent.chatAgent import *
from core.vectordb.chromadb import *
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()

@router.get("/document/getDocumentList")
async def get_documents_all(knowledgeID:str, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    documents=get_document_by_knowledgeID(db, knowledgeID)

    filtered_documents = [{"documentID": doc.uid,"documentName":doc.documentName, "documentStatus": doc.documentStatus,"documentTags":[doc.primaryClassification,doc.secondaryClassification]+(doc.tags.split(", ") if doc.tags else []),"vectorNum":doc.documentVector,"createTime":doc.createTime_timestamp} for doc in documents]
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
    Document =db.query(Document).filter(Document.uid == documentID,Document.knowledgeID==knowledgeID).first()
    return {
        "status_code": 200,
        "msg": "Get document info successfully",
        "data": {
            "documentID": Document.uid,
            "documentName": Document.documentName,
            "documentStatus": Document.documentStatus,
            "vectorNum": Document.documentVector,
            "documentTags": Document.tags,
        }
    }

## 根据documentID获取pdf文件
@router.get("/document/getFile")
def get_document(documentID: str,db: Session = Depends(get_db)):
    agent_path = Path.cwd()
    Document =db.query(Document).filter(Document.uid == documentID).first()
    if not Document:
        return {
            "status_code": 404,
            "msg": "document not found",
        }
    file_path =os.getenv("AcadeAgent_DIR")+Document.documentPath
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
        Document =db.query(Document).filter(Document.uid == uid).first()
        if Document:
            #代表用户已经上传过该文件 or 其他知识中存在该文件 todo: 复制文件状态
            print("file ",file.filename," already exists")
            continue
        ###

        Document = DocumentCreate(documentName=file.filename,documentPath=os.path.join("/res/pdf/",file.filename),documentStatus=0,uid=uid,knowledgeID=knowledgeID,lid=user.lid,createTime=createtime)
        print(Document.documentPath)
        create_Document(db=db, Document=Document)
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
    Document =db.query(Document).filter(Document.uid ==file_md5).first()
    if Document:
        #代表用户已经上传过该文件 or 其他知识中存在该文件 todo: 复制文件状态

        ### 如果其他知识中已经存在这个Document则拷贝其状态
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=jsonable_encoder({                
                "status_code": status.HTTP_409_CONFLICT,
                "msg": "文件已存在",
                }),
        )
        
    # 重置文件内容读取位置，以便后续写入文件
    documentFile.file.seek(0)
    print("saving ",documentFile.filename,"...")
    file_path=os.path.join(pdf_storage_path,documentFile.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(documentFile.file.read())
    uid=cal_file_md5(file_path)
    print("UID",uid)
    createtime=datetime.datetime.now(timezone.utc)
    Document = DocumentCreate(documentName=documentFile.filename,documentPath=os.path.join("/res/pdf/",documentFile.filename),documentStatus=0,uid=uid,knowledgeID=knowledgeID,lid=user.lid,createTime=createtime)

    create_Document(db=db, Document=Document)
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
import hashlib
import os
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, File, Form, Path, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.agent.chatAgent import *
from core.agent.dataprocessAgent import *
from core.backend.crud.crud_document import *
from core.backend.router.req_res_schema import DeleteDocument
from core.backend.schema.schema import *
from core.backend.utils.utils import get_current_user, get_db, get_filtered_documents
from core.vectordb.chromadb import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()

@router.get("/document/getDocumentList")
async def get_documents_all(knowledgeID:str, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    documents=get_document_by_knowledgeID(db, knowledgeID)
    
    filtered_documents = get_filtered_documents(documents)
    return {
            "status_code": 200, 
            "msg":"Get document list successfully", 
            "data":filtered_documents
            }

# 获取document的状态
@router.get("/document/Info")
async def get_document_info(documentID: str,knowledgeID:str,token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    await get_current_user(token,db)
    print(documentID,knowledgeID)
    document =db.query(Document).filter(Document.uid == documentID,Document.knowledgeID==knowledgeID).first()
    return {
        "status_code": 200,
        "msg": "Get document info successfully",
        "data": {
            "documentID": document.uid,
            "documentName": document.documentName,
            "documentStatus": document.documentStatus,
            "vectorNum": document.documentVector,
            "documentTags": document.tags if document.tags else [],
        }
    }

## 根据documentID获取pdf文件
@router.get("/document/getFile")
def get_document(documentID: str,knowledgeID:str,db: Session = Depends(get_db)):
    Document =get_document_by_uid_kid(db, documentID,knowledgeID)
    if not Document:
        return {
            "status_code": 404,
            "msg": "document not found",
        }
    file_path =os.getenv("AcadeAgent_DIR")+Document.documentPath
    print("File_path",file_path) # 替换成你实际的 PDF 文件路径
    return FileResponse(file_path)



## 单文件上传
@router.post("/document/upload")
async def  upload_document(knowledgeID:str=Form(),documentFile:UploadFile=File, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    pdf_storage_path =os.getenv("PAPER_SAVE_DIR")
    user =await get_current_user(token,db)

        # 计算文件的MD5哈希值
    hasher = hashlib.md5()
    file_content = await documentFile.read()
    hasher.update(file_content)
    file_md5 = hasher.hexdigest()
    print("FILE_MD5",file_md5)
    document =get_document_by_uid(db, file_md5)
    if document:
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
    document = DocumentCreate(documentName=documentFile.filename,documentPath=os.path.join("/res/pdf/",documentFile.filename),documentStatus=0,uid=uid,knowledgeID=knowledgeID,lid=user.lid,createTime=createtime)

    create_document(db=db, document=document)
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

## 文件删除
@router.post("/document/delete")
async def delete_document(deleteDocument:DeleteDocument,token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    document =get_document_by_uid_kid(db, deleteDocument.documentID,deleteDocument.knowledgeID)
    if not document:
        return {
            "status_code": 404,
            "msg": "文件不存在",
        }
    db.delete(document)
    db.commit()
    doc =get_document_by_uid(db, deleteDocument.documentID)#检查其他知识中是否还有该文档,如果有就不需要删除向量和源文件
    if not doc: #如果没有则进行删除
        file_path =os.getenv("AcadeAgent_DIR")+document.documentPath
        os.remove(file_path)
    return {
        "status_code": 200,
        "msg": "文件删除成功",
    }
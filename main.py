from fastapi import Depends, FastAPI, HTTPException ,File, UploadFile,Form,Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated, Union
import uuid
import dotenv
from langchain_openai import OpenAIEmbeddings
import os
from pathlib import Path
from core.backend.crud import *
from core.backend.schema import *
from core.backend.database import SessionLocal, engine
from core.backend.models import Base,User
from core.backend.translate import Translator
from core.llm.Agent import Agent_v1
from core.agent.dataprocessAgent import *
from core.agent.chatAgent import *
from core.database.chromadb import *

SECRET_KEY = "8590c54f9848254ebe161df5e2ec1823189201fdd524a167d45ab951d6eec026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000

Base.metadata.create_all(bind=engine)
dotenv.load_dotenv()
llm=Agent_v1()
chroma_db=AcadeChroma("/data1/wyyzah-work/AcadeAgent/res/layer1","/data1/wyyzah-work/AcadeAgent/res/layer2",OpenAIEmbeddings(),llm)
chat_agent=ChatAgent(llm.get_llm('openai'),chroma_db)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
class LoginException(HTTPException):
    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code
        self.msg = msg

class Ref(BaseModel):
    documentID: str
    selectedText: str
    page: int

class Chat_Request(BaseModel):
    input: str
    ref: Ref
    context: str

# 使用Data 生成token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=60000)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username") 
    except Exception:
        raise credentials_exception
    user = query_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def generate_future_timestamp(minutes: int):
    """
    生成指定分钟以后的时间戳（以秒为单位的整数）

    :param minutes: 指定的分钟数
    :return: 指定分钟以后的时间戳（以秒为单位的整数）
    """
    now =datetime.datetime.now(timezone.utc)
    future_timestamp= now + timedelta(minutes=minutes)
     
    return int(future_timestamp.timestamp())

@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    user = query_user(db, username)
    if not user or user.password != password:
            return  JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"status_code": status.HTTP_401_UNAUTHORIZED, "msg": "用户名或密码错误"}),
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": username,"lid":user.lid}, expires_delta=access_token_expires
    )
    return {
        "status_code": 200,
        "msg": "登录成功",
        "data":{"access_token": access_token, "token_type": "Bearer","expire":generate_future_timestamp(ACCESS_TOKEN_EXPIRE_MINUTES)}
    }

# 测试登录状态
@app.get("/testlogin")
async def testlogin(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user =await get_current_user(token,db)
    return user

##-----------------------------------------------------------
# 获取用户的知识库描述
@app.get("/knowledges/getLibraryInfo")
async def describe_knowledge(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user =await get_current_user(token,db)
    Knowledgecount,filecount,vectorcount=get_Knowledges_statistics(db, user.lid)
    return {
        "status_code": 200,
        "msg": "Get knowledge statistics successfully",
        "data": {
            "libraryID" : user.lid,
            "knowledgeNumSum": Knowledgecount,
            "documentNumSum": filecount,
            "vectorNumSum": vectorcount
        }
    }

# 获取用户拥有的所有 `知识`
@app.get("/knowledges/getKnowledgeList")
async def get_knowledges_all(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    #获取当前用户
    user =await get_current_user(token,db)
    knowledges=get_Knowledge_by_lid(db, user.lid)
    #根据用户lid获取其拥有的全部知识
    return {"status_code": 200, 
            "msg":"Get knowledge list successfully", 
            "data":{
                "knowledgeList": knowledges
            }
            }

# 用户创建新的知识
@app.post("/knowledges/createKnowledge")
async def create_knowledges(knowledge: KnowledgeCreate, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user =await get_current_user(token,db)
    knowledge.lid = user.lid
    knowledge.knowledgeID = str(uuid.uuid1())
    return create_knowledge(db, knowledge)

# 获取知识所拥有的所有文档
@app.get("/knowledges/{knowledgeID}")
async def get_documents_all(knowledgeID:str= Path(), token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user =await get_current_user(token,db)
    documents=get_document_by_knowledgeID(db, knowledgeID)
    filtered_documents = [{"documentID": doc.id,"documentName":doc.documentName, "documentStatus": doc.documentStatus,"documentTags":doc.tags,"vectorNum":doc.documentVector} for doc in documents]
    return {"status_code": 200, 
            "msg":"Get document list successfully", 
            "data":{
                "documentList": filtered_documents
            }
            }

# 获取document的状态
@app.get("/document/Info")
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
            "tags": paper.tags,
        }
    }

## 根据documentID获取pdf文件
@app.get("/document/getFile")
def get_document(documentID: str,db: Session = Depends(get_db)):
    agent_path = Path.cwd()
    print("AGENT_A",agent_path)
    paper =db.query(Paper).filter(Paper.uid == documentID).first()
    if not paper:
        return {
            "status_code": 404,
            "msg": "document not found",
        }
    file_path ="C:\\Users\\qwrdxer\\Desktop\\AcadeAgent" +paper.documentPath
    print("File_path",file_path) # 替换成你实际的 PDF 文件路径
    return FileResponse(file_path)

## 用户上传新的文档到指定的知识中
@app.post("/document/upload")
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
        ###检测是否已经存在
        paper =db.query(Paper).filter(Paper.uid == uid).first()
        if paper:
            #代表用户已经上传过该文件 or 其他知识中存在该文件 todo: 复制文件状态
            print("file ",file.filename," already exists")
            continue
        ###

        paper = PaperCreate(documentName=file.filename,documentPath=os.path.join("/res/pdf/",file.filename),documentStatus=0,uid=uid,knowledgeID=knowledgeID,lid=user.lid)
        print(paper.documentPath)
        create_paper(db=db, paper=paper)
    return {
        "status_code": 200,
        "msg": "upload successfully",
    }
## 翻译
@app.get("/translate")
def translate(text: str, token: str = Depends(oauth2_scheme)):
    translator = Translator(from_lang="en", to_lang="zh",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    result =translator.translate(text)
    return {
    "status_code": 200,
    "msg": "translate successfully",
    "data": {
        "text": result
    }
}

## 聊天对话
@app.get("/chat/generate")
def chat_with_paper_generate(chat:Chat_Request , token: str = Depends(oauth2_scheme)):
    docs=chroma_db.query_paper_with_score_layer1_by_filter("what is GCHRL)",{"documentID":"fd48386887fae0c08d10d7ef66ddeda8"})
    print(docs)
    output,context=chat_agent.chat_with_memory("","","什么是GCHRL",docs)
    return {
        "status_code": 200,
        "msg": "chat successfully",
        "data": {
            "input": chat.input,
            "output": output,
            "context": context
        }
    
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")
# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from core.backend.router.schema import Chat_Request
from core.backend.crud.crud import get_document_by_knowledgeID
import dotenv

from core.backend.utils.utils import get_current_user, get_db
dotenv.load_dotenv()

from fastapi import Depends, FastAPI, HTTPException ,File, UploadFile,Form,Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated, Union
import uuid
from langchain_openai import OpenAIEmbeddings
import os
from pathlib import Path
import hashlib

from core.backend.crud.crud import *
from core.backend.schema.schema import *
from core.backend.db.database import SessionLocal, engine
from core.backend.db.models import Base,User
from core.backend.services.translate import Translator
from core.llm.Agent import Agent_v1
from core.agent.dataprocessAgent import *
from core.agent.chatAgent import *
from core.vectordb.chromadb import *
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()



## 聊天对话
@router.get("/chat/generate")
def chat_with_paper_generate(chat:Chat_Request , request:Request,token: str = Depends(oauth2_scheme)):
    docs=request.app.chroma_db.query_paper_with_score_layer1_by_filter("what is GCHRL)",{"documentID":"fd48386887fae0c08d10d7ef66ddeda8"})
    print(docs)
    output,context=request.app.chat_agent.chat_with_memory("","","什么是GCHRL",docs)
    return {
        "status_code": 200,
        "msg": "chat successfully",
        "data": {
            "input": chat.input,
            "output": output,
            "context": context
        }
    
    }

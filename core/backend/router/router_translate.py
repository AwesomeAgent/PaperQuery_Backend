# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from core.backend.router.schema import Chat_Request
import dotenv

from core.backend.utils.utils import get_current_user, get_db
dotenv.load_dotenv()

from fastapi import Depends, FastAPI, HTTPException ,File, UploadFile,Form,Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



from core.backend.schema.schema import *

from core.backend.services.translate import Translator

from core.agent.dataprocessAgent import *
from core.agent.chatAgent import *
from core.vectordb.chromadb import *
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()


@router.get("/translate")
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
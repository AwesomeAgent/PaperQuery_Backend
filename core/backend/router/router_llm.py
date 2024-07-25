# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

from core.backend.router.schema import Chat_Request

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

# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
import json
from core.backend.router.req_res_schema import Chat_Request, Summarise_Request
from core.backend.services.translate import Translator
import re
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()



## 聊天对话
@router.post("/chat/generate")
def chat_with_paper_generate(chat:Chat_Request , request:Request,token: str = Depends(oauth2_scheme)):
    docs=request.app.chroma_db.query_paper_with_score_layer1_by_filter(chat.input,{"documentID":chat.ref.documentID})
    print(docs)
    output,context=request.app.chat_agent.chat_with_memory(chat.context,chat.ref.selectedText,input,docs)
    return {
        "status_code": 200,
        "msg": "chat successfully",
        "data": {
            "input": chat.input,
            "output": output,
            "context": context
        }
    
    }
## 流式对话
@router.post("/chat/generate_flow")
def chat_with_paper_generate(chat:Chat_Request , request:Request,token: str = Depends(oauth2_scheme)):
    translator = Translator(from_lang="zh", to_lang="en",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    translatedinput =translator.translate(re.sub(r'[\n\r\t]', '', chat.question))
    #将用户的问题作为RAG进行检索
    docs=request.app.chroma_db.query_paper_with_score_layer1_by_filter(translatedinput,{"documentID":chat.ref.documentID})
    ret=request.app.chat_agent.chat_with_memory_ret(chat.context,chat.ref.selectedText,translatedinput,docs)
    #chat_with_memory_ret(self, conversation_memory,ref,question,paper_content):
    ##      /                                                   |                          \
    # 3 联邦学习中文RAG与论文毫无相关、但是是专业学术问题       什么Python              这篇文章的实验效果如何?(着重强调实验部分)  论文相关,但RAG检索到的内容并不足以支撑回答,则GPT生成检索问题,再次RAG 
    #  ret=request.app.chat_agent.chat_with_memory_ret(chat.context,chat.ref.selectedText,translatedinput,docs)

    def predict():
        text = ""
        for _token in ret:
            token = _token.content
            js_data = {"code": "200", "msg": "ok", "data": token}
            yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
            text += token
        print(text)

    generate = predict()
    return StreamingResponse(generate, media_type="text/event-stream")


## 对话总结
@router.post("/chat/summarize")
def chat_summarise(chat:Summarise_Request,request:Request,token: str = Depends(oauth2_scheme)):
    output=request.app.chat_agent.chat_summarise(chat.context,chat.question,chat.answer)
    return {
        "status_code": 200,
        "msg": "记忆更新成功",
        "data": {
            "context": output
        }
    
    }
## 对话总结
@router.post("/chat/chat_raw")
def chat_summarise(chat:Summarise_Request,request:Request,token: str = Depends(oauth2_scheme)):
    output=request.app.chat_agent.chat_summarise(chat.context,chat.question,chat.answer)
    return {
        "status_code": 200,
        "msg": "记忆更新成功",
        "data": {
            "context": output
        }
    
    }
## 流式对话
@router.post("/chat/generate_flow_test")
def chat_with_paper_generate(chat:Chat_Request , request:Request,token: str = Depends(oauth2_scheme)):

    ret=request.app.chat_agent.chat_simple(chat.question)
    #chat_with_memory_ret(self, conversation_memory,ref,question,paper_content):
    def predict():
        text = ""
        for _token in ret:
            token = _token.content
            js_data = {"code": "200", "msg": "ok", "data": token}
            yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
            text += token
        print(text)

    generate = predict()
    return StreamingResponse(generate, media_type="text/event-stream")


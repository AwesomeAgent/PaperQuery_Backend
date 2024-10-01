# 获取知识所拥有的所有文档
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
import json
from arxiv_client import PARAMS, ArxivClient
from core.backend.router.req_res_schema import Chat_Request, Summarise_Request, TMP_Chat_Request
from core.backend.services.translate import Translator
import re

from core.backend.utils.utils import format_uids_to_json
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
def chunked_yield(data, chunk_size=3):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]
@router.post("/chat/generate_flow")
def chat_with_paper_generate(chat:Chat_Request , request:Request,token: str = Depends(oauth2_scheme)):
    translator = Translator(from_lang="zh", to_lang="en",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    translator_rev = Translator(from_lang="en", to_lang="zh",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    translatedinput =translator.translate(re.sub(r'[\n\r\t]', '', chat.question))
    #将用户的问题作为RAG进行检索
    docs=request.app.chroma_db.query_paper_with_score_layer1_by_filter(translatedinput,{"documentID":chat.ref.documentID})
    judge_result=request.app.chat_agent.chat_judge_relate(chat.context,chat.ref.selectedText,translatedinput,docs)
    print(docs)
    ret=None
    results=None
    if( not judge_result["is_relevant"]) and (judge_result["is_professional"] and len(judge_result["arxiv_query_keyword"])>0):
        fetch_params = [PARAMS.TITLE, PARAMS.PDF_URL, PARAMS.PUBLISHED]
        client = ArxivClient(max_results=10)
        results = client.fetch_results(judge_result["arxiv_query_keyword"], fetch_params)

    else:
        ret=request.app.chat_agent.chat_with_memory_ret_tmp(chat.context,translatedinput,docs)
    def predict():
        text = ""

        for _token in ret:
            token = _token.content
            js_data = {"code": "200", "msg": "ok", "data": token}
            yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
            text += token

    def arxiv_search():
        js_data = {"code": "200", "msg": "ok", "data": "**您的专业性问题似乎跟本篇论文无关,为您联网检索到如下论文:<br>** \r\n"}
        yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
        count=1
        for paper in results:
            datalist=f"**{count}**.<u> [{translator_rev.translate(paper.get(PARAMS.TITLE, 'N/A'))}]({paper.get(PARAMS.PDF_URL, 'N/A')})</u> <br><br>"
            count+=1     
            for chunk in chunked_yield(datalist):
                js_data = {"code": "200", "msg": "ok", "data": chunk}
                yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
    if ret:
        generate = predict()
    else:
        generate = arxiv_search()
    return StreamingResponse(generate, media_type="text/event-stream")


@router.post("/chat/mulit_file_chat_generate_flow")
def chat_with_paper_generate(chat:TMP_Chat_Request , request:Request):#token: str = Depends(oauth2_scheme)):
    translator = Translator(from_lang="zh", to_lang="en",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    translator_rev = Translator(from_lang="en", to_lang="zh",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    translatedinput =translator.translate(re.sub(r'[\n\r\t]', '', chat.question))
    #将用户的问题作为RAG进行检索
    docs=request.app.chroma_db.query_paper_with_score_layer1_by_filter(translatedinput,format_uids_to_json(chat.uid))
    
    print(docs)
    judge_result=request.app.chat_agent.chat_judge_relate(chat.context,"",translatedinput,docs)
    ret=None
    results=None
    if( not judge_result["is_relevant"]) and (judge_result["is_professional"] and len(judge_result["arxiv_query_keyword"])>0):
        fetch_params = [PARAMS.TITLE, PARAMS.PDF_URL, PARAMS.PUBLISHED]
        client = ArxivClient(max_results=10)
        results = client.fetch_results(judge_result["arxiv_query_keyword"], fetch_params)

    else:
        ret=request.app.chat_agent.chat_with_memory_ret(chat.context,"",translatedinput,docs)
    def predict():
        text = ""

        for _token in ret:
            token = _token.content
            js_data = {"code": "200", "msg": "ok", "data": token}
            yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
            text += token

    def arxiv_search():
        js_data = {"code": "200", "msg": "ok", "data": "**您的专业性问题似乎跟本篇论文无关,为您联网检索到如下论文:<br>** \r\n"}
        yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
        count=1
        for paper in results:
            datalist=f"**{count}**. [{translator_rev.translate(paper.get(PARAMS.TITLE, 'N/A'))}]({paper.get(PARAMS.PDF_URL, 'N/A')}) <br><br>"
            count+=1     
            for chunk in chunked_yield(datalist):
                js_data = {"code": "200", "msg": "ok", "data": chunk}
                yield f"data: {json.dumps(js_data,ensure_ascii=False)}\n\n"
    if ret:
        generate = predict()
    else:
        generate = arxiv_search()
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



import json

from langchain_openai import OpenAI

from core.backend.utils.utils import clean_markdown_json_blocks
from core.llm.myprompts import *


# 用于聊天对话的Agent
class ChatAgent:
    def __init__(self,llm,streamllm,chromadb):
        self.llm=llm
        self.streamllm:OpenAI =streamllm
        self.chromadb=chromadb
        self.sqlitconnect=None

    #废弃函数
    def chat_with_memory(self, conversation_memory,ref,question,paper_content):
        prompt=CHAT_WITH_MEMORY_PAPER_ASSISITANT.format(conversation_memory=conversation_memory,ref=ref,question=question,paper_content=paper_content)
       # print(len(prompt))
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                response = self.llm.invoke(prompt)
                break
            except Exception:
                retries += 1
                if retries == max_retries:
                    print("Max retries reached. Exiting...")
                    return None
                print(f"Retrying... (Attempt {retries})")
        print(response.content)
        jsondata=json.loads(response.content)
        print(jsondata)
        return jsondata["answer"],jsondata["conversation_memory"]

    #判断关联性
    def chat_judge_relate(self, conversation_memory,ref,question,paper_content):
        prompt=CONTEXT_RELATE_DETECTION.format(conversation_memory=conversation_memory,ref=ref,question=question,paper_content=paper_content)
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                response = self.llm.invoke(prompt)
                filter_response=clean_markdown_json_blocks(response.content)
                jsondata=json.loads(filter_response)
                break
            except Exception:
                retries += 1
                if retries == max_retries:
                    print("Max retries reached. Exiting...")
                    return None
                print(f"Retrying... (Attempt {retries})")
        return jsondata
    #流式对话
    def chat_with_memory_ret(self, conversation_memory,ref,question,paper_content):
        prompt=CHAT_WITH_MEMORY_PAPER_ASSISITANT_ANSWER_PART.format(conversation_memory=conversation_memory,ref=ref,question=question,paper_content=paper_content)
        #print(prompt)
        return self.streamllm.stream(prompt)
    #临时文件流式对话,
    def chat_with_memory_ret_tmp(self, conversation_memory,question,paper_content):
        prompt=CHAT_WITH_MEMORY_PAPER_ASSISITANT_TMP.format(conversation_memory=conversation_memory,question=question,paper_content=paper_content)
        #print(prompt)
        return self.streamllm.stream(prompt)
    def chat_summarise(self,context,question,answer):
        prompt=CHAT_WITH_MEMORY_PAPER_ASSISITANT_ANSWER_SUMMARY.format(context=context,question=question,answer=answer)
        response = self.llm.invoke(prompt)
        return response.content

    def chat_simple(self,prompt):

        return self.streamllm.stream(prompt)
    def get_llm(self):
        return self.llm
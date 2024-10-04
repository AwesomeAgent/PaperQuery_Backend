import erniebot
import json

from core.backend.utils.utils import clean_markdown_json_blocks
from core.llm.myprompts import *

erniebot.api_type = 'aistudio'
erniebot.access_token = 'e78006946e211683837a6bf32c63788166e55c7c'  # 替换为你在百度 AI Studio 上生成的 Access Token


class ChatAgent:
    def __init__(self, llm, chromadb):
        self.llm = llm  # 这里是文心大模型实例
        self.chromadb = chromadb
        self.sqlitconnect = None

    # 判断关联性
    def chat_judge_relate(self, conversation_memory, ref, question, paper_content):
        prompt = CONTEXT_RELATE_DETECTION.format(
            conversation_memory=conversation_memory,
            ref=ref,
            question=question,
            paper_content=paper_content
        )
        max_retries = 5
        retries = 0
        jsondata = None
        while retries < max_retries:
            try:
                # 文心大模型调用
                response = self.llm.chat_with_llm(prompt)
                filter_response = clean_markdown_json_blocks(response.get_result())
                jsondata = json.loads(filter_response)
                break
            except Exception as e:
                retries += 1
                if retries == max_retries:
                    print(f"Max retries reached. Exiting... Error: {e}")
                    return None
                print(f"Retrying... (Attempt {retries})")
        return jsondata

    # 流式对话
    def chat_with_memory_ret(self, conversation_memory, ref, question, paper_content):
        prompt = CHAT_WITH_MEMORY_PAPER_ASSISITANT_ANSWER_PART.format(
            conversation_memory=conversation_memory,
            ref=ref,
            question=question,
            paper_content=paper_content
        )
        # 调用文心大模型的流式 API
        response = self.llm.ChatCompletion.create(
            model="ernie-3.5", 
            messages=[{
                "role": "user",
                "content": prompt
            }], 
            stream=True
        )
        return response

    # 临时文件流式对话
    def chat_with_memory_ret_tmp(self, conversation_memory, question, paper_content):
        prompt = CHAT_WITH_MEMORY_PAPER_ASSISITANT_TMP.format(
            context=conversation_memory,
            question=question,
            paper_content=paper_content
        )
        # 调用文心大模型的流式 API
        response = self.llm.ChatCompletion.create(
            model="ernie-3.5", 
            messages=[{
                "role": "user",
                "content": prompt
            }], 
            stream=True
        )
        return response

    def chat_summarise(self, context, question, answer):
        prompt = CHAT_WITH_MEMORY_PAPER_ASSISITANT_ANSWER_SUMMARY.format(
            context=context,
            question=question,
            answer=answer
        )
        response = self.llm.ChatCompletion.create(
            model='ernie-3.5',  # 使用文心大模型的版本
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.get_result()

    def chat_simple(self, prompt):
        # 简单的流式对话，使用文心大模型
        response = self.llm.ChatCompletion.create(
            model="ernie-3.5", 
            messages=[{
                "role": "user",
                "content": prompt
            }], 
            stream=True
        )
        return response

    def get_llm(self):
        return self.llm

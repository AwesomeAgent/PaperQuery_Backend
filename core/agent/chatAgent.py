import json

from core.llm.myprompts import *


# 用于聊天对话的Agent
class ChatAgent:
    def __init__(self,llm,chromadb):
        self.llm=llm
        self.chromadb=chromadb
        self.sqlitconnect=None
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
        jsondata=json.loads(response.content)
        print(jsondata)
        return jsondata["answer"],jsondata["conversation_memory"]
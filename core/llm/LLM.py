import tiktoken
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '../..', '.env')  # 假设 .env 文件在上一级目录
load_dotenv(dotenv_path=dotenv_path)
class LLM:
    def __init__(self):
        self.llms = {}
        self.llms['openai'] = ChatOpenAI(model="gpt-4o-mini",openai_api_key=os.getenv("OPENAI_API_KEY"),openai_api_base=os.getenv("OPENAI_API_BASE"),default_headers = {"x-foo": "true"})
        self.tokenizer=tiktoken.encoding_for_model('gpt-4o')
        self.chatllm = self.llms['openai']
    def get_llm(self, name):
        return self.llms[name]

    def get_all_llms(self):
        return self.llms
    def count_doc_token(self,text):
        return len(self.tokenizer(text)['input_ids'])
    
    ## 将提示词发送给大模型，获取回复
    def chat_with_llm(self,chat_prompt):
        print(chat_prompt)
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                response = self.chatllm.invoke(chat_prompt)
                return response
            except Exception:
                retries += 1
                if retries == max_retries:
                    print("Max retries reached. Exiting...")
                    return None
                print(f"Retrying... (Attempt {retries})")

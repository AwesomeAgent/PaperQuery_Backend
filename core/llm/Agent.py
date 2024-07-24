from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.question_answering import load_qa_chain
import tiktoken
class Agent_v1:
    def __init__(self):
        self.llms = {}
        self.llms['openai'] = ChatOpenAI(model="gpt-3.5-turbo",openai_api_key="sk-WMwF3ZICC7ebCTTyC57c38Ff2b4246Ce8108A6DcF8B045C7",openai_api_base="https://api.gpt.ge/v1/",default_headers = {"x-foo": "true"})
        self.tokenizer=tiktoken.encoding_for_model('gpt-3.5-turbo')
    def get_llm(self, name):
        return self.llms[name]

    def get_all_llms(self):
        return self.llms
    def count_doc_token(self,text):
        return len(self.tokenizer(text)['input_ids'])

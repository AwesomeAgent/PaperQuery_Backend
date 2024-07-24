
from langchain_openai import OpenAIEmbeddings
from core.agent.chatAgent import ChatAgent
from core.backend.db.database import SessionLocal
from core.vectordb.chromadb import AcadeChroma

chroma_db = None
chat_agent = None
llm = None
def get_chroma_db():
    print(chroma_db)
    return chroma_db
def get_chat_agent():
    return chat_agent
def get_llm():
    return llm

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

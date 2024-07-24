import dotenv
from contextlib import asynccontextmanager
dotenv.load_dotenv()

from fastapi import Depends, FastAPI
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from fastapi.middleware.cors import CORSMiddleware


from langchain_openai import OpenAIEmbeddings
import os

from core.backend.crud.crud import *
from core.backend.schema import *
from core.backend.db.database import SessionLocal, engine
from core.backend.db.models import Base,User
from core.backend.services.translate import Translator
from core.llm.Agent import Agent_v1
from core.agent.dataprocessAgent import *
from core.agent.chatAgent import *
from core.vectordb.chromadb import *
from core.backend.router import router_document,router_knowledge,router_llm,router_user,router_translate
SECRET_KEY = "8590c54f9848254ebe161df5e2ec1823189201fdd524a167d45ab951d6eec026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000

Base.metadata.create_all(bind=engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    global chroma_db, chat_agent, llm
    llm=Agent_v1()
    chroma_db=AcadeChroma(os.getenv("CHROMA_LAYER1_DIR"),os.getenv("CHROMA_LAYER2_DIR"),OpenAIEmbeddings(),llm)
    chat_agent=ChatAgent(llm.get_llm('openai'),chroma_db)
    print(chroma_db)
    yield
    # Clean up the ML models and release resources
    print("shoutdown!")
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


app.include_router(router_user.router, tags=["router_user"])
app.include_router(router_knowledge.router, tags=["knowledge"])
app.include_router(router_document.router, tags=["router_document"])
app.include_router(router_llm.router, tags=["router_llm"])
app.include_router(router_translate.router, tags=["router_translate"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
from contextlib import asynccontextmanager

import dotenv

dotenv.load_dotenv()

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from core.agent.chatAgent import *
from core.agent.dataprocessAgent import *
from core.backend.crud.crud_document import *
from core.backend.crud.crud_knowledge import *
from core.backend.crud.crud_user import *
from core.backend.db.database import engine
from core.backend.db.models import Base
from core.backend.router import (
    router_document,
    router_knowledge,
    router_llm,
    router_translate,
    router_user,
    router_note
)
from core.backend.schema.schema import *
from core.llm.LLM import LLM
from core.vectordb.chromadb import *


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.llm=LLM()
    app.chroma_db=AcadeChroma(os.getenv("CHROMA_LAYER1_DIR"),os.getenv("CHROMA_LAYER2_DIR"),OpenAIEmbeddings(),app.llm)
    app.chat_agent=ChatAgent(app.llm.get_llm('openai'),ChatOpenAI(model="gpt-4o-mini",streaming=True,openai_api_key="sk-WMwF3ZICC7ebCTTyC57c38Ff2b4246Ce8108A6DcF8B045C7",openai_api_base="https://api.gpt.ge/v1/",default_headers = {"x-foo": "true"}),app.chroma_db)
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
app.include_router(router_note.router, tags=["router_note"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import time

import dotenv
from colorama import Fore, Style
from langchain_openai import OpenAIEmbeddings

from core.agent.dataprocessAgent import *
from core.backend.crud.crud_document import (
    get_document_status_equal_zero,
    update_document_content,
    update_document_status,
)
from core.backend.crud.crud_knowledge import update_knowledge_content
from core.backend.db.database import SessionLocal
from core.llm.LLM import *
from core.vectordb.chromadb import *

db = SessionLocal()

def test_add():
    dotenv.load_dotenv()
    llms=LLM()
    chroma_db=AcadeChroma("/data1/wyyzah-work/PaperQuery_Backend/res/layer2","/data1/wyyzah-work/PaperQuery_Backend/res/layer2",OpenAIEmbeddings(),llms.get_llm('openai'))
    dp=DataProcessAgent(llms.get_llm('openai'),chroma_db)
    directory = os.getenv("document_SAVE_DIR")

    dp.batch_add_newdocument(directory,"kid1")
            
if __name__ == '__main__':
    dotenv.load_dotenv()
    llm=LLM()
    chroma_db=AcadeChroma(os.getenv("CHROMA_LAYER1_DIR"),os.getenv("CHROMA_LAYER2_DIR"),OpenAIEmbeddings(),llm)
    dp=DataProcessAgent(llm,chroma_db)
    db = SessionLocal()
    while True:
        document=get_document_status_equal_zero(db)
        time.sleep(3)
        if document:
            print(Fore.RED,f"开始处理{document.documentName}",Style.RESET_ALL)
            print(type(document)) 

            print(Fore.BLUE,f"更新状态为 1",Style.RESET_ALL)
            document.documentStatus=1
            update_document_status(db,document)
            result=dp.add_newpaper(os.getenv("AcadeAgent_DIR")+document.documentPath,document.knowledgeID)
            print(result)
            result["uid"]=document.uid
            print(Fore.YELLOW,f"更新向量,",Style.RESET_ALL)
            print(Fore.YELLOW,f"更新描述标签信息,",Style.RESET_ALL)
            update_document_content(db,result)
            print(Fore.YELLOW,f"更新知识库信息,",Style.RESET_ALL)
            ## 更新知识库状态, 总向量数+N,总文件数＋1 
            update_knowledge_content(db,result["documentVector"],1,document.knowledgeID)
            print(Fore.GREEN,f"处理完成更新状态为 2,",Style.RESET_ALL)
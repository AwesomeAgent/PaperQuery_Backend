import dotenv
from colorama import Fore, Back, Style
from core.backend.crud.crud import get_paper_status_equal_zero, update_paper_content, update_paper_status
from core.backend.db.database import SessionLocal
from core.vectordb.chromadb import *
from core.llm.Agent import *
from core.agent.dataprocessAgent import *


from langchain_openai import OpenAIEmbeddings
import time
db = SessionLocal()

def test_add():
    dotenv.load_dotenv()
    llm=Agent_v1()
    chroma_db=AcadeChroma("/data1/wyyzah-work/AcadeAgent/res/layer1","/data1/wyyzah-work/AcadeAgent/res/layer2",OpenAIEmbeddings(),llm)
    dp=DataProcessAgent(llm,chroma_db)
    directory = os.getenv("PAPER_SAVE_DIR")

    dp.batch_add_newpaper(directory,"kid1")
            
if __name__ == '__main__':
    dotenv.load_dotenv()
    llm=Agent_v1()
    chroma_db=AcadeChroma(os.getenv("CHROMA_LAYER1_DIR"),os.getenv("CHROMA_LAYER2_DIR"),OpenAIEmbeddings(),llm)
    dp=DataProcessAgent(llm,chroma_db)
    db = SessionLocal()
    while True:
        paper=get_paper_status_equal_zero(db)
        time.sleep(1)
        if paper:
            print(Fore.RED,f"开始处理{paper.documentName}",Style.RESET_ALL)
            print(type(paper)) 

            print(Fore.BLUE,f"更新状态为 1",Style.RESET_ALL)
            paper.documentStatus=1
            update_paper_status(db,paper)
            result=dp.add_newpaper(os.getenv("AcadeAgent_DIR")+paper.documentPath,paper.knowledgeID)
            print(result)
            result["uid"]=paper.uid
            print(Fore.YELLOW,f"更新向量,",Style.RESET_ALL)
            print(Fore.YELLOW,f"更新描述标签信息,",Style.RESET_ALL)
            update_paper_content(db,result)
            time.sleep(10)
            print(Fore.GREEN,f"处理完成更新状态为 2,",Style.RESET_ALL)
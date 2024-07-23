import dotenv
from core.vectordb.chromadb import *
from core.llm.Agent import *
from core.agent.dataprocessAgent import *
from langchain_openai import OpenAIEmbeddings
import time


def test_retrivel():
    dotenv.load_dotenv()
    llm=Agent_v1()
    chroma_db=AcadeChroma("/data1/wyyzah-work/AcadeAgent/res/layer1","/data1/wyyzah-work/AcadeAgent/res/layer2",OpenAIEmbeddings(),llm)
    print(f"当前存储的向量数{chroma_db.chroma_db_layer1._collection.count()}")
    start_time = time.time()
    chroma_db.summarize_paper("/data1/wyyzah-work/AcadeAgent/pdf/23USENIX-Rosetta Enabling Robust TLS Encrypted Traffic Classification in Diverse Network Environments with TCP-Aware Traffic Augmentation.pdf")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"代码执行耗时：{elapsed_time} 秒")

def test_add():
    dotenv.load_dotenv()
    llm=Agent_v1()
    chroma_db=AcadeChroma("/data1/wyyzah-work/AcadeAgent/res/layer1","/data1/wyyzah-work/AcadeAgent/res/layer2",OpenAIEmbeddings(),llm)
    dp=DataProcessAgent(llm,chroma_db)
    directory = r'/data1/wyyzah-work/AcadeAgent/res/pdf'

    dp.batch_add_newpaper(directory,"kid1")
            
if __name__ == '__main__':
    test_add()
    #test_retrivel()
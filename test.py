from langchain_openai import OpenAIEmbeddings
from core.vectordb.chromadb import AcadeChroma
import dotenv

dotenv.load_dotenv()


if __name__ == '__main__':
    chroma_db=AcadeChroma("/data1/wyyzah-work/PaperQuery_Backend/res/layer1","/data1/wyyzah-work/PaperQuery_Backend/res/layer2",OpenAIEmbeddings(),None)
    sres=chroma_db.query_paper_with_score_layer1_by_filter("1",{"documentID":"ed9852d1334f204e4f6faf04897a2b08"})
    print(sres)
    
from langchain_openai import OpenAIEmbeddings
from core.backend.utils.utils import format_uids_to_json
from core.vectordb.chromadb import AcadeChroma
import dotenv

dotenv.load_dotenv()


if __name__ == '__main__':
    chroma_db=AcadeChroma("/data1/wyyzah-work/PaperQuery_Backend/res/layer1","/data1/wyyzah-work/PaperQuery_Backend/res/layer2",OpenAIEmbeddings(),None)
    x={
    "$or": [
        {
            "documentID": {
               "$eq": "92557e08092fb856bca961e816f4110b"
            }
        },
        {
            "documentID": {
                "$eq": "1ea21b3369043655250dd228a3e21486"
            }
        }
    ]
                                                           
}   
    print(type(x))
    sres=chroma_db.query_paper_with_score_layer1_by_filter("1",
    x
                                                        )
    print(sres)
    uid_list = [
    "1ea21b3369043655250dd228a3e21486",
    "92557e08092fb856bca961e816f4110b"
]

    json_output = format_uids_to_json(uid_list)
    print(type(json_output))
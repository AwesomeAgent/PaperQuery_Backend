from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
import json
from ..llm import myprompts
from ..utils.util import cal_file_md5,check_and_parse_json
from rich.progress import Progress
import os


class DataProcessAgent:
    def __init__(self,llm,chromadb):
        self.llm=llm
        self.chromadb=chromadb
        self.sqlitconnect=None

    # 将新的论文增加到layer1和layer2
    def add_newpaper(self,filepath,knowledgeID):
        loader  = PyPDFLoader(filepath)
        file_hash=cal_file_md5(filepath)
        pages = loader.load_and_split()
        # 将完整的论文加载到layer1
        texts = [doc.page_content for doc in pages]
        metadatas = [doc.metadata for doc in pages]
        for metadata in metadatas:
            metadata['documentID'] = file_hash  # 添加新的键值对，例如 'new_key': 'new_value'
            metadata['knowledge_name']=knowledgeID
        
        self.chromadb.add_paper_to_layer1(texts, metadatas)

        
        # 调用大模型的RAG进行论文摘要,并将摘要存储到layer2
        json_paper= self.summarize_paper(filepath)
        metadataofpaper={
            "source":filepath,
            "Primary Classification":json_paper["Primary Classification"],# 二级分类
            "Secondary Classification":json_paper["Secondary Classification"], #一级分类
            "documentID":file_hash, #文件的hash
            "knowledgeID":knowledgeID, #所在的知识库
            }
        self.chromadb.add_paper_to_layer2([json.dumps(json_paper, indent=2)], [metadataofpaper])

        # todo 将摘要存储到数据库中
    def batch_add_newpaper(self, dir,knowledgeID):
        with Progress() as progress:
            task = progress.add_task("[green]Processing files", total=len(os.listdir(dir)))
            for file_name in os.listdir(dir):
                # 进行文件处理操作
                file_path = os.path.join(dir, file_name)       
                progress.update(task, advance=1, description=f"[cyan]processing ... {file_name}")
                # 执行其他操作，例如添加文章
                self.add_newpaper(file_path,knowledgeID)
                # 更新进度条

            print("[bold green]Batch processing completed!")

        # 完成后显示完成信息
        print("[bold green]Batch processing completed!")

    def summarize_paper(self,filename):
        ## 获得retriver
        fileRetriver=self.chromadb.chroma_db_layer1.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3,'filter':{'source':filename}},
            
            )
        ## 检索出论文相关内容
        docs=fileRetriver.batch(["Retrieve detailed information about the document's key contributions, innovative methods, experimental results, thorough analysis, and significant advancements."])

        prompt=myprompts.SUMMRISE_TEMPLET.format(SUMMRISZ_TEMPLTE=myprompts.SUMMRISZ_TEMPLTE2,context=docs[0])
        print(prompt)
       # print(len(prompt))
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                response = self.llm.get_llm("openai").invoke(prompt)
                if check_and_parse_json(response)!=None:
                    break
            except Exception as e:
                retries += 1
                if retries == max_retries:
                    print("Max retries reached. Exiting...")
                    return None
                print(f"Retrying... (Attempt {retries})")
        return check_and_parse_json(response)
    





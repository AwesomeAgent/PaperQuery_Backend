from langchain_chroma import Chroma


# 提供对向量数据库的操作
class AcadeChroma:
    def __init__(self,persist_directory_layer1,persist_directory_layer2,embedding_model,llm_model):
        self.chroma_db_layer1 = Chroma(persist_directory=persist_directory_layer1, embedding_function=embedding_model)
        self.chroma_db_layer2 = Chroma(persist_directory=persist_directory_layer2, embedding_function=embedding_model)
        self.current_layer1_count=self.chroma_db_layer1._collection.count()
        self.current_layer2_count=self.chroma_db_layer2._collection.count()
    # 增
    def add_paper_to_layer1(self,texts,metadatas):
        self.chroma_db_layer1.add_texts(texts, metadatas)
        self.current_layer1_count=self.chroma_db_layer1._collection.count()
    
    def add_paper_to_layer2(self,texts,metadatas):
        self.chroma_db_layer2.add_texts(texts, metadatas)
        self.current_layer2_count=self.chroma_db_layer1._collection.count()

    # 查 
    # 全局查询 , 根据问题返回检索出来的文档
    def query_paper_with_score_layer1(self,query_str):
        return self.chroma_db_layer1.similarity_search_with_score(query_str)
    # 根据问题返回检索出来的文档
    def query_paper_with_score_layer2(self,query_str):
        return self.chroma_db_layer2.similarity_search_with_score(query_str)
    
    # 过滤器查询
    def query_paper_with_score_layer1_by_filter(self,query_str,filter):
        fileRetriver=self.chroma_db_layer1.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5,'filter':filter},
                )
        docs=fileRetriver.batch([query_str])
        return str(docs)
    # 过滤器查询
    def query_paper_with_score_layer2_by_filter(self,query_str,filters):
        pass

    
    # 删除指定 kid下的文档
    def delete_paper_from_layer1(self,kid,documentid):
        filterDocs=self.chroma_db_layer1.get(where={"$and":[{"knowledge_name":kid},{"documentID":documentid}]},include=["metadatas"])
        if len(filterDocs["ids"])>0:
            self.chroma_db_layer1.delete(filterDocs['ids'])

    def delete_paper_from_layer2(self,kid,documentid):
        filterDocs=self.chroma_db_layer2.get(where={"$and":[{"knowledgeID":kid},{"documentID":documentid}]},include=["metadatas"])
        if len(filterDocs["ids"])>0:
            self.chroma_db_layer2.delete(filterDocs['ids'])
    # 改
    def alter_paper_from_layer1(self,ids,text):
        pass 
    
    # 状态查询
    def get_layer_vector_count(self):
        return self.current_layer1_count,self.current_layer2_count



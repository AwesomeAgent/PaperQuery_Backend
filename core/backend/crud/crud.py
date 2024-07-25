'''
@Description: 
@Author: qwrdxer
@Date: 2024-07-22 21:31:52
@LastEditTime: 2024-07-23 14:35:16
@LastEditors: qwrdxer
'''
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Tuple

from core.backend.db.models import *
from core.backend.schema.schema import *

#--------------------------

# 统计知识库的知识数量
def get_Knowledges_statistics(db: Session, lid: int) -> Tuple[int, int,int ]:
    # 构造查询
    Knowledgecount = db.query(func.count(Knowledge.documentNum)).filter(Knowledge.lid == lid).scalar()
    filecount = db.query(func.sum(Knowledge.documentNum)).filter(Knowledge.lid == lid).scalar()
    vectorcount = db.query(func.sum(Knowledge.vectorNum)).filter(Knowledge.lid == lid).scalar()
    return Knowledgecount,filecount,vectorcount
# 获取用户拥有的所有`知识`
def get_Knowledge_by_lid(db: Session, lid: str) :
    return db.query(Knowledge).filter(Knowledge.lid == lid).all()


# 为用户增加新的`知识`
def create_knowledge(db: Session, knowledge: KnowledgeCreate):
    db_knowledge = Knowledge(**knowledge.model_dump())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge
## 根据知识名获取知识
def get_knowledge_by_name(db: Session, knowledgeName: str):
    return db.query(Knowledge).filter(Knowledge.knowledgeName == knowledgeName).first()

#----------------------------
# 获取用户指定知识下所有文档信息
def get_document_by_knowledgeID(db: Session, knowledgeID: str) :
    return db.query(Paper).filter(Paper.knowledgeID == knowledgeID).all()

def get_paper_by_filename(db: Session, filename: str):
    return db.query(Paper).filter(Paper.filename == filename).first()

def get_paper_status_equal_zero(db: Session):
    return db.query(Paper).filter(Paper.documentStatus == 0).first()

def update_paper_status(db: Session,paper: Paper):
    db.query(Paper).filter(Paper.uid == paper.uid).update({Paper.documentStatus: paper.documentStatus})
    db.commit()
    return 1

def update_paper_content(db: Session,result: dict):
    db.query(Paper).filter(Paper.uid == result["uid"]).update({Paper.documentVector: result["documentVector"],
                                                           Paper.primaryClassification: result["Primary Classification"],
                                                           Paper.secondaryClassification: result["Secondary Classification"],
                                                           Paper.tags: ','.join(result["Research Direction Tags"]),
                                                           Paper.documentDescription: result["Abstract"],
                                                           Paper.documentStatus: 2
                                                           })
    db.commit()
    return 1
# 增
def create_paper(db: Session, paper: PaperCreate):
    db_paper = Paper(**paper.model_dump())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

# 改
def update_paper(db: Session, paper: PaperUpdate):
    db.query(Paper).filter(Paper.filename == paper.filename).update(**paper.model_dump())
    db.commit()
    return db.query(Paper).filter(Paper.filename == paper.filename).first()
def get_papers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Paper).offset(skip).limit(limit).all()






#----------------------用户相关
def create_user(db: Session, user: UserCreate):
    db_user = User(user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def query_user(db: Session, username: str) :
    return db.query(User).filter(User.username == username).first()
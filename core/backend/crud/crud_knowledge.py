from typing import Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from core.backend.db.models import *
from core.backend.schema.schema import *

#--------------------------

# 统计知识库的知识数量
def get_knowledges_statistics(db: Session, lid: int) -> Tuple[int, int,int ]:
    # 构造查询
    Knowledgecount = db.query(func.count(Knowledge.documentNum)).filter(Knowledge.lid == lid).scalar()
    filecount = db.query(func.sum(Knowledge.documentNum)).filter(Knowledge.lid == lid).scalar()
    vectorcount = db.query(func.sum(Knowledge.vectorNum)).filter(Knowledge.lid == lid).scalar()
    return Knowledgecount,filecount,vectorcount
# 获取用户拥有的所有`知识`
def get_knowledge_by_lid(db: Session, lid: str) :
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
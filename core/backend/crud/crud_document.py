from sqlalchemy.orm import Session

from core.backend.db.models import *
from core.backend.schema.schema import *


# 获取用户指定知识下所有文档信息
def get_document_by_knowledgeID(db: Session, knowledgeID: str) :
    return db.query(Document).filter(Document.knowledgeID == knowledgeID).all()

def get_document_by_filename(db: Session, filename: str):
    return db.query(Document).filter(Document.filename == filename).first()

def get_document_status_equal_zero(db: Session):
    return db.query(Document).filter(Document.documentStatus == 0).first()

def update_document_status(db: Session,Document: Document):
    db.query(Document).filter(Document.uid == Document.uid).update({Document.documentStatus: Document.documentStatus})
    db.commit()
    return 1

def update_Document_content(db: Session,result: dict):
    db.query(Document).filter(Document.uid == result["uid"]).update({Document.documentVector: result["documentVector"],
                                                           Document.primaryClassification: result["Primary Classification"],
                                                           Document.secondaryClassification: result["Secondary Classification"],
                                                           Document.tags: ','.join(result["Research Direction Tags"]),
                                                           Document.documentDescription: result["Abstract"],
                                                           Document.documentStatus: 2
                                                           })
    db.commit()
    return 1
# 增
def create_Document(db: Session, Document: DocumentCreate):
    db_Document = Document(**Document.model_dump())
    db.add(db_Document)
    db.commit()
    db.refresh(db_Document)
    return db_Document

# 改
def update_document(db: Session, Document: DocumentUpdate):
    db.query(Document).filter(Document.filename == Document.filename).update(**Document.model_dump())
    db.commit()
    return db.query(Document).filter(Document.filename == Document.filename).first()
def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Document).offset(skip).limit(limit).all()


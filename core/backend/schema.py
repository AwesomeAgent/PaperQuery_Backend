'''
@Description: 
@Author: qwrdxer
@Date: 2024-07-22 21:31:52
@LastEditTime: 2024-07-23 14:35:53
@LastEditors: qwrdxer
'''
from pydantic import BaseModel
import datetime
from typing import List
class Response(BaseModel):
    status_code: int
    msg: str

# 知识创建
class KnowledgeCreate(BaseModel):
    knowledgeID: str | None = None #
    lid: str | None = None # 
    knowledgeName: str 
    knowledgeDescription: str  | None = None # 
    documentNum:int =0
    vectorNum:int  =0


# 知识更新
class KnowledgeUpdate(KnowledgeCreate):
    documentNum: int | None = None
    vectorNum: int | None = None
# 用户所有知识描述

# 知识获取
class KnowledgeGet(KnowledgeCreate):
    documentNum: int | None = None
    vectorNum: int | None = None
    
# 返回知识
class KnowledgeQuery(Response):
    data: List[KnowledgeGet] | None = None

class LoginRequest(BaseModel):
    username: str
    password: str
# 文件paper创建
class PaperCreate(BaseModel):
    uid : str 
    knowledgeID : str 
    lid: str 
    documentName: str
    documentPath: str
    documentStatus: int
# 向量相关更新
class PaperUpdate(PaperCreate):
    fvector: int
    primary_classification: str | None = None
    secondary_classification: str | None = None
    tags: str | None = None
    fdesc: str | None = None

#文件查询
class PaperQuery(PaperCreate):
    fvector: int
    primary_classification: str | None = None
    secondary_classification: str | None = None
    tags: str | None = None
    description: str | None = None




class UserCreate(BaseModel):
    username: str
    password: str

class UserQuery(BaseModel):
    username: str | None = None
    password: str | None = None

##------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    lid: str | None = None
    exp: datetime.datetime | None = None
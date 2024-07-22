# @File : models.py


from .database import Base

from sqlalchemy import  Column , Integer, String,Text



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)  # 最多50个字符的变长字符串，不允许为空
    password = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    lid = Column(Text, nullable=False)  # 文本类型，不允许为空

# 定义 Knowledge 表
class Knowledge(Base):
    __tablename__ = 'knowledges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledgeID = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    lid = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    knowledgeName = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    knowledgeDescription = Column(Text)  # 文本类型，可以存储较长的描述信息
    documentNum = Column(Integer)  # 整数类型，用于存储文件相关信息
    vectorNum = Column(Integer)  # 整数类型，用于存储向量信息

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    knowledgeID = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    lid = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    documentName = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    documentPath = Column(String(255), nullable=False)  # 最多255个字符的变长字符串，不允许为空
    documentStatus = Column(Integer)  # 整数类型，用于存储文件状态
    documentVector = Column(Integer)  # 整数类型，用于存储文件向量
    primaryClassification = Column(String(255))  # 最多255个字符的变长字符串，用于存储主分类
    secondaryClassification = Column(String(255))  # 最多255个字符的变长字符串，用于存储次分类
    tags = Column(String(255))  # 最多255个字符的变长字符串，用于存储标签
    documentDescription = Column(Text)  # 文本类型，可以存储较长的描述信息
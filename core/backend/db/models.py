'''
@Description: 
@Author: qwrdxer
@Date: 2024-07-22 21:31:52
@LastEditTime: 2024-07-23 15:56:37
@LastEditors: qwrdxer
'''
# @File : models.py


from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, func
from sqlalchemy.orm import column_property

from .database import Base


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

# 定义 Document 表
class Document(Base):
    __tablename__ = 'documents'
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
    createTime = Column(TIMESTAMP, server_default=func.now())  # 增加的时间戳字段，默认当前时间
    createTime_timestamp = column_property(func.extract('epoch', createTime).cast(Integer))
# 临时文件存储
# 定义 Document 表
class TMPDocument(Base):
    __tablename__ = 'tmpdocuments'
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
    createTime = Column(TIMESTAMP, server_default=func.now())  # 增加的时间戳字段，默认当前时间
    createTime_timestamp = column_property(func.extract('epoch', createTime).cast(Integer))


class Note(Base):
    __tablename__ = 'notes'
    # 表字段映射
    id = Column(Integer, primary_key=True, autoincrement=True)
    lid = Column(String(255), nullable=False)
    knowledgeID = Column(String(255), nullable=False)
    uid = Column(String(255), nullable=False)
    note = Column(Text)
# 使用Data 生成token
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt,os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.backend.crud.crud_user import query_user
from core.backend.router.dependencies import *



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60000)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt




def generate_future_timestamp(minutes: int):
    """
    生成指定分钟以后的时间戳（以秒为单位的整数）

    :param minutes: 指定的分钟数
    :return: 指定分钟以后的时间戳（以秒为单位的整数）
    """
    now =datetime.now(timezone.utc)
    future_timestamp= now + timedelta(minutes=minutes)
     
    return int(future_timestamp.timestamp())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("username") 
    except Exception:
        raise credentials_exception
    user = query_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_document_tags(doc):
    """
    从文档对象中提取并过滤分类和标签
    """
    tags = [doc.primaryClassification, doc.secondaryClassification] + (doc.tags.split(",") if doc.tags else [])
    # 使用列表推导式去除空字符串
    filtered_tags = [tag.strip() for tag in tags if tag and tag.strip()]
    return filtered_tags


def get_filtered_documents(documents):
    """
    从文档列表中创建过滤后的文档字典列表
    """
    filtered_documents = [{
        "documentID": doc.uid,
        "documentName": doc.documentName,
        "documentStatus": doc.documentStatus,
        "documentTags": get_document_tags(doc) if (doc.primaryClassification or doc.secondaryClassification or doc.tags) else [],
        "vectorNum": doc.documentVector,
        "createTime": doc.createTime_timestamp
    } for doc in documents]
    return filtered_documents
from fastapi import HTTPException
from pydantic import BaseModel


class LoginException(HTTPException):
    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code
        self.msg = msg

class Ref(BaseModel):
    knowledgeID: str
    documentID: str
    selectedText: str
    page: int

class Chat_Request(BaseModel):
    input: str
    ref: Ref
    context: str


class DeleteDocument(BaseModel):
    documentID: str
    knowledgeID: str


class TranslateRequest(BaseModel):
    text: str

class Summarise_Request(BaseModel):
    input: str
    answer: str
    context: str
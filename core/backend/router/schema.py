from fastapi import HTTPException
from pydantic import BaseModel


class LoginException(HTTPException):
    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code
        self.msg = msg

class Ref(BaseModel):
    documentID: str
    selectedText: str
    page: int

class Chat_Request(BaseModel):
    input: str
    ref: Ref
    context: str
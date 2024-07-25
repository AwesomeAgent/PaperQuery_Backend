
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from core.backend.services.translate import Translator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter()


@router.get("/translate")
def translate(text: str, token: str = Depends(oauth2_scheme)):
    translator = Translator(from_lang="en", to_lang="zh",secret_id="AKIDdA0xAOMfptoks0ERZk3WxIiDoP0cFqU5",secret_key="jcPB0mo6NofWI5EEHUycWgsz34xpeWTU")
    result =translator.translate(text)
    return {
    "status_code": 200,
    "msg": "translate successfully",
    "data": {
        "text": result
    }
}
from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from core.backend.crud.crud_commit import create_commit, query_all_commits_by_pid
from core.backend.router.dependencies import get_db
from core.backend.router.router_user import get_current_user
from core.backend.schema.commitschema import CommitCreate, CommitCreateRequest, QueryCommitResponse

oauth2_schema=OAuth2PasswordBearer(tokenUrl="/login")
router=APIRouter()


#创建评论
@router.post("/forum/createcommit")
async def create_commit_handler(commitCreateRequest:CommitCreateRequest,token:str=Depends(oauth2_schema),db:Session=Depends(get_db)):
    #获取当前用户
    user =await get_current_user(token,db)
    createtime=datetime.now(timezone.utc)
    commitdata=CommitCreate(
        lid=user.lid,
        postid=commitCreateRequest.postid,
        username=user.username,
        content=commitCreateRequest.content,
        publishtime=int(createtime.timestamp())
    )
    create_commit(db,commitdata)
    return{
            "status_code": 200, 
            "msg":"create commit suscessfully."
            }

#获取指定帖子对应的所有评论
@router.get("/forum/getpostcommit")
async def get_post_commit_handler(postid:str,token:str=Depends(oauth2_schema),db:Session=Depends(get_db)):
    
    commits=query_all_commits_by_pid(db,postid)
    commitsData=[QueryCommitResponse.model_validate(commit) for commit in commits]
    return {
            "status_code": 200, 
            "msg":"get commit suscessfully.",
            "data":commitsData
        }
from datetime import datetime

from fastapi import Depends, Response
from pydantic import BaseModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class CreateCommentRequest(BaseModel):
    content: str

@router.post("/{shanyrak_id:str}/comment")
def upload_comment(
        shanyrak_id: str,
        comment: CreateCommentRequest,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    if shanyrak is None:
        return Response(status_code=404)
    #
    # comment["created_at"] = datetime.now()
    # comment["author_id"] = jwt_data.user_id
    svc.repository.add_comment(shanyrak_id, jwt_data.user_id, comment.content)

    return Response(status_code=200)

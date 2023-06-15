from fastapi import Depends, Response
from pydantic import BaseModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete("/{shanyrak_id:str}/comment/{comment_id:str}")
def delete_comment(
        shanyrak_id: str,
        comment_id: str,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    if shanyrak is None:
        return Response(status_code=404)

    svc.repository.delete_comment(shanyrak_id, jwt_data.user_id, comment_id)

    return Response(status_code=200)

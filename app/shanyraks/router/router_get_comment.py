from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router

class GetMyShanyrakResponse(AppModel):

    comment: List

@router.get("/{shanyrak_id:str/comment}", response_model=GetMyShanyrakResponse)
def get_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    if shanyrak is None:
        return Response(status_code=404)

    return GetMyShanyrakResponse(**shanyrak)
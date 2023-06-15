from typing import List

from fastapi import Depends, Response
from pydantic.main import BaseModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class CreatePaterRequest(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

@router.post("/")
def create_pater(
    input: CreatePaterRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    svc.repository.create_pater(user_id, input.dict())
    return Response(status_code=200)

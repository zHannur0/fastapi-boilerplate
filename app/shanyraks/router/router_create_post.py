from fastapi import Depends, UploadFile,Response
from typing import List

from app.auth.adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from app.auth.router.dependencies import parse_jwt_user_data


@router.post("/file")
def upload_file(
        file: UploadFile,
        svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    url = svc.s3_service.upload_file(file.file, file.filename)

    return {"msg": url}


@router.post("/{shanyrak_id:str}/media")
def upload_files(
        shanyrak_id: str,
        files: List[UploadFile],
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    if shanyrak is None:
        return Response(status_code=404)

    for file in files:
            url = svc.s3_service.upload_file(file.file, shanyrak_id, file.filename)
            svc.repository.add_shanyrak_post(shanyrak_id, jwt_data.user_id, url)

    return {"msg": files}

from fastapi import Depends, Response
from typing import List

from app.auth.adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
class DeleteRequest(AppModel):
    media: List[str]

@router.delete("/{shanyrak_id:str}/media")
def delete_files(
    shanyrak_id: str,
    input: DeleteRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    if shanyrak is None:
        return Response(status_code=404)

    delete_result = None
    for file in input.media:
        # Delete the file using the S3 service
        svc.s3_service.delete_file(shanyrak_id, file)

        # Remove the file reference from the repository
        print(file)
        delete_result = svc.repository.delete_shanyrak_post(shanyrak_id, jwt_data.user_id, file)

    if delete_result:
        return Response(status_code=200)
    # return Response(status_code=404)
    return delete_result

from http import HTTPStatus

from fastapi import APIRouter

from ..models.app_status import AppStatus
from ..database.engine import check_availability

router = APIRouter()

@router.get(path='/status', status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_availability())
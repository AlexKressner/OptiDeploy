# project/app/api/healthcheck.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
def get_healthstatus():
    return {"Status": "Healthy"}

from fastapi import APIRouter, Depends
from application.external_data.list_extracts import ListExternalDataExtracts

router = APIRouter(prefix="/external-data", tags=["External Data"])

@router.get("/extract-definitions")
def list_extract_definitions(
    service: ListExternalDataExtracts = Depends(),
):
    return service.execute()
from fastapi import APIRouter
from fastapi.responses import FileResponse

from ..config.paths import CHART_PAGE_HTML, INDEX_HTML


router = APIRouter(tags=["pages"])


@router.get("/", include_in_schema=False)
def index_page() -> FileResponse:
    return FileResponse(INDEX_HTML)


@router.get("/chart", include_in_schema=False)
def chart_page() -> FileResponse:
    return FileResponse(CHART_PAGE_HTML)

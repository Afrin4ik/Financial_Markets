import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse

from ..config.paths import CHART_PAGE_HTML, INDEX_HTML


router = APIRouter(tags=["pages"])
logger = logging.getLogger(__name__)


@router.get("/", include_in_schema=False)
def index_page() -> FileResponse:
    try:
        if not INDEX_HTML.exists():
            logger.error(f"Файл index.html не найден: {INDEX_HTML}")
            raise HTTPException(status_code=500, detail="Страница index не найдена")
        return FileResponse(INDEX_HTML)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Ошибка при отдаче index.html")
        raise HTTPException(status_code=500, detail="Ошибка загрузки страницы") from exc


@router.get("/chart", include_in_schema=False)
def chart_page() -> FileResponse:
    try:
        if not CHART_PAGE_HTML.exists():
            logger.error(f"Файл chart.html не найден: {CHART_PAGE_HTML}")
            raise HTTPException(status_code=500, detail="Страница графика не найдена")
        return FileResponse(CHART_PAGE_HTML)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Ошибка при отдаче chart.html")
        raise HTTPException(status_code=500, detail="Ошибка загрузки страницы") from exc

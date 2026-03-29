from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "views" / "static"
TEMPLATES_DIR = BASE_DIR / "views" / "templates"

INDEX_HTML = TEMPLATES_DIR / "index.html"
CHART_PAGE_HTML = TEMPLATES_DIR / "chart.html"

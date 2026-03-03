import os

# ── 경로 설정 ──────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR     = os.path.join(BASE_DIR, "storage", "data")
HISTORY_FILE  = os.path.join(DATA_DIR, "history.json")
DATASET_FILE  = os.path.join(DATA_DIR, "datasets.json")

# ── HTTP 설정 ──────────────────────────────────────────────────────────────
DEFAULT_TIMEOUT = 30
MAX_HISTORY     = 50
HTTP_METHODS    = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

# ── 메서드별 색상 (UI 공통) ────────────────────────────────────────────────
METHOD_COLORS = {
    "GET":     "#28a745",
    "POST":    "#007bff",
    "PUT":     "#ffc107",
    "DELETE":  "#dc3545",
    "PATCH":   "#fd7e14",
    "HEAD":    "#6c757d",
    "OPTIONS": "#6c757d",
}

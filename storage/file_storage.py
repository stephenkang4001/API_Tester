import json
import os
from config import DATA_DIR, HISTORY_FILE


class FileStorage:
    def __init__(self) -> None:
        os.makedirs(DATA_DIR, exist_ok=True)

    # ── History ───────────────────────────────────────────────────────────
    def load_history(self) -> list:
        if not os.path.exists(HISTORY_FILE):
            return []
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
            return json.loads(content) if content else []
        except Exception:
            return []

    def save_history(self, history: list) -> None:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

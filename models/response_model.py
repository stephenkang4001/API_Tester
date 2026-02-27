from dataclasses import dataclass, field, asdict
from typing import Dict, Optional


@dataclass
class ApiResponse:
    status_code: int             = 0
    headers:     Dict[str, str]  = field(default_factory=dict)
    body:        str             = ""
    elapsed_ms:  float           = 0.0
    size_bytes:  int             = 0
    timestamp:   str             = ""
    error:       Optional[str]   = None
    error_type:  Optional[str]   = None

    # ── 직렬화 ────────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ApiResponse":
        return cls(
            status_code = data.get("status_code", 0),
            headers     = data.get("headers", {}),
            body        = data.get("body", ""),
            elapsed_ms  = data.get("elapsed_ms", 0.0),
            size_bytes  = data.get("size_bytes", 0),
            timestamp   = data.get("timestamp", ""),
            error       = data.get("error"),
            error_type  = data.get("error_type"),
        )

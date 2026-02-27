from dataclasses import dataclass, field, asdict
from typing import Dict, Optional


@dataclass
class ApiRequest:
    method: str                  = "GET"
    url:    str                  = ""
    params: Dict[str, str]       = field(default_factory=dict)
    headers: Dict[str, str]      = field(default_factory=dict)
    body:   Optional[str]        = None

    # ── 직렬화 ────────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ApiRequest":
        return cls(
            method  = data.get("method", "GET"),
            url     = data.get("url", ""),
            params  = data.get("params", {}),
            headers = data.get("headers", {}),
            body    = data.get("body"),
        )

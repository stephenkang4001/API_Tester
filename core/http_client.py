import json
import time
from datetime import datetime

import requests

from models.request_model import ApiRequest
from models.response_model import ApiResponse


def send_request(request: ApiRequest, timeout: int = 30) -> ApiResponse:
    """HTTP 요청을 실행하고 ApiResponse를 반환한다."""

    # 빈 키 필터링
    headers = {k: v for k, v in request.headers.items() if k.strip()}
    params  = {k: v for k, v in request.params.items()  if k.strip()}

    try:
        kwargs: dict = dict(
            method         = request.method,
            url            = request.url,
            headers        = headers,
            params         = params,
            timeout        = timeout,
            allow_redirects= True,
        )

        # Body 처리 (GET / HEAD / OPTIONS 는 body 없음)
        if request.body and request.method not in ("GET", "HEAD", "OPTIONS"):
            try:
                parsed = json.loads(request.body)
                kwargs["json"] = parsed
                headers.setdefault("Content-Type", "application/json")
            except json.JSONDecodeError:
                kwargs["data"] = request.body

        t0   = time.time()
        resp = requests.request(**kwargs)
        elapsed_ms = (time.time() - t0) * 1000

        # 응답 body 파싱 (JSON 우선, 아니면 text)
        try:
            body_text = json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except Exception:
            body_text = resp.text

        return ApiResponse(
            status_code = resp.status_code,
            headers     = dict(resp.headers),
            body        = body_text,
            elapsed_ms  = round(elapsed_ms, 2),
            size_bytes  = len(resp.content),
            timestamp   = datetime.now().isoformat(),
        )

    except requests.exceptions.MissingSchema:
        return _err("URL은 http:// 또는 https:// 로 시작해야 합니다.", "INVALID_URL")
    except requests.exceptions.InvalidURL:
        return _err("유효하지 않은 URL입니다.", "INVALID_URL")
    except requests.exceptions.ConnectionError as e:
        s = str(e)
        detail = (
            "DNS 조회 실패 – 도메인이 존재하지 않거나 인터넷 연결을 확인하세요."
            if ("Name or service not known" in s or "nodename" in s)
            else "서버에 연결할 수 없습니다. URL 또는 네트워크를 확인하세요."
        )
        return _err(f"연결 오류: {detail}", "CONNECTION_ERROR")
    except requests.exceptions.Timeout:
        return _err(f"타임아웃: {timeout}초 이내에 서버가 응답하지 않았습니다.", "TIMEOUT")
    except requests.exceptions.SSLError:
        return _err("SSL 오류: 인증서가 유효하지 않거나 만료되었습니다.", "SSL_ERROR")
    except Exception as e:
        return _err(f"알 수 없는 오류: {e}", "UNKNOWN")


def _err(msg: str, etype: str) -> ApiResponse:
    return ApiResponse(
        error      = msg,
        error_type = etype,
        timestamp  = datetime.now().isoformat(),
    )

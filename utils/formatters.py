def format_size(n: int) -> str:
    """바이트 수를 읽기 쉬운 문자열로 변환"""
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.1f} MB"


def format_elapsed(ms: float) -> str:
    """밀리초를 읽기 쉬운 문자열로 변환"""
    return f"{ms:.0f} ms" if ms < 1000 else f"{ms / 1000:.2f} s"


def status_badge_html(code: int) -> str:
    """HTTP 상태 코드를 색상 배지 HTML로 변환"""
    if   200 <= code < 300: bg, label = "#28a745", f"✅ {code}"
    elif 300 <= code < 400: bg, label = "#ffc107", f"↩️ {code}"
    elif 400 <= code < 500: bg, label = "#fd7e14", f"⚠️ {code}"
    elif 500 <= code < 600: bg, label = "#dc3545", f"❌ {code}"
    else:                   bg, label = "#6c757d", f"❓ {code}"
    return (
        f'<span style="background:{bg};color:#fff;'
        f'padding:4px 12px;border-radius:6px;'
        f'font-weight:bold;font-size:1.0rem">{label}</span>'
    )


def error_hint(etype: str) -> str:
    """에러 타입별 해결 힌트 반환"""
    return {
        "INVALID_URL":      "💡 URL은 반드시 `http://` 또는 `https://`로 시작해야 합니다.",
        "CONNECTION_ERROR": "💡 도메인이 올바른지, 인터넷 연결 상태를 확인하세요.",
        "TIMEOUT":          "💡 서버가 응답하지 않습니다. 서버 상태나 방화벽 설정을 확인하세요.",
        "SSL_ERROR":        "💡 자체 서명 인증서이거나 만료된 인증서일 수 있습니다.",
        "UNKNOWN":          "💡 요청 설정을 다시 확인하거나 콘솔 로그를 참고하세요.",
    }.get(etype, "")

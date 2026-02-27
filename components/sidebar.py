import streamlit as st

from config import METHOD_COLORS
from core.history_manager import HistoryManager
from models.request_model import ApiRequest


# ── 내부 헬퍼 ─────────────────────────────────────────────────────────────

def _load_entry(entry: dict) -> None:
    """히스토리 항목을 session_state 에 복원한다."""
    req = entry["request"]
    st.session_state.current_request = ApiRequest.from_dict(req)

    params  = req.get("params",  {}) or {}
    headers = req.get("headers", {}) or {}

    st.session_state.param_rows  = (
        [{"key": k, "value": v} for k, v in params.items()]
        or [{"key": "", "value": ""}]
    )
    st.session_state.header_rows = (
        [{"key": k, "value": v} for k, v in headers.items()]
        or [{"key": "", "value": ""}]
    )
    # body 초기화 및 ace editor 강제 리셋
    st.session_state.body_draft  = req.get("body") or ""
    st.session_state.ace_version = st.session_state.get("ace_version", 0) + 1
    st.session_state.current_response = None


def _status_info(res: dict) -> tuple[str, str]:
    """(badge, emoji) 반환"""
    code  = res.get("status_code", 0)
    error = res.get("error")
    if error:
        return "ERR", "❌"
    if 200 <= code < 300: return str(code), "✅"
    if 300 <= code < 400: return str(code), "↩️"
    if 400 <= code < 500: return str(code), "⚠️"
    return str(code), "🔴"


# ── 퍼블릭 렌더 함수 ──────────────────────────────────────────────────────

def render_sidebar() -> None:
    hm = HistoryManager()

    # 헤더
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("## 📋 History")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️", help="히스토리 전체 삭제", use_container_width=True):
            hm.clear()
            st.rerun()

    history = hm.get_all()

    if not history:
        st.info("히스토리가 없습니다.\nAPI를 호출하면 여기에 기록됩니다.")
        return

    for i, entry in enumerate(history):
        req = entry["request"]
        res = entry["response"]

        method    = req.get("method", "GET")
        url       = req.get("url", "")
        badge, emoji = _status_info(res)
        color     = METHOD_COLORS.get(method, "#6c757d")
        short_url = (url[:33] + "…") if len(url) > 35 else url

        with st.container(border=True):
            # 메서드 뱃지 + 상태 코드
            st.markdown(
                f'<span style="background:{color};color:#fff;'
                f'padding:1px 7px;border-radius:4px;'
                f'font-size:0.72rem;font-weight:bold">{method}</span>'
                f'&nbsp; {emoji} <b>{badge}</b>',
                unsafe_allow_html=True,
            )
            st.caption(short_url)
            if st.button("불러오기", key=f"hist_load_{i}", use_container_width=True):
                _load_entry(entry)
                st.rerun()

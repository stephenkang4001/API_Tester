"""
API Tester – Postman 스타일 API 테스트 도구 (Streamlit 기반)
실행: streamlit run app.py
"""
import streamlit as st

from components.request_builder import render_request_builder
from components.response_viewer import render_response_viewer
from components.sidebar import render_sidebar
from models.request_model import ApiRequest

# ── 페이지 설정 ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="API Tester",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 전역 CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* 상단 여백 줄이기 */
    .block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
    /* 사이드바 상단 여백 */
    div[data-testid="stSidebarContent"] { padding-top: 0.8rem; }
    /* 버튼 둥근 모서리 */
    .stButton > button { border-radius: 6px; }
    /* 탭 글씨 살짝 굵게 */
    .stTabs [data-baseweb="tab"] { font-weight: 500; }
</style>
""", unsafe_allow_html=True)


# ── Session State 초기화 ───────────────────────────────────────────────────
def _init() -> None:
    defaults: dict = {
        "current_request":  ApiRequest(),   # 현재 편집 중인 요청
        "current_response": None,           # 마지막 응답
        "param_rows":  [{"key": "", "value": ""}],  # Params 에디터 행
        "header_rows": [{"key": "", "value": ""}],  # Headers 에디터 행
        "body_draft":  "",                  # Body 에디터 임시 저장
        "ace_version": 0,                   # 히스토리 로드 시 ace 리셋용
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init()

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    render_sidebar()

# ── 헤더 ──────────────────────────────────────────────────────────────────
st.markdown("# 🚀 API Tester")
st.caption("Postman 스타일 API 테스트 도구 · Streamlit 기반 · MVP v1.0")
st.divider()

# ── 요청 빌더 ─────────────────────────────────────────────────────────────
render_request_builder()

# ── 응답 뷰어 ─────────────────────────────────────────────────────────────
if st.session_state.current_response is not None:
    st.divider()
    render_response_viewer(st.session_state.current_response)

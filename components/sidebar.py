import streamlit as st

from config import METHOD_COLORS
from core.dataset_manager import DataSetManager
from models.request_model import ApiRequest


# ── 내부 헬퍼 ─────────────────────────────────────────────────────────────

def _load_dataset(entry: dict) -> None:
    """Data Set 항목을 session_state 에 복원한다."""
    req = entry["request"]
    st.session_state.current_request    = ApiRequest.from_dict(req)
    st.session_state.dataset_name       = entry["name"]
    st.session_state.current_dataset_id = entry["id"]
    # 이름 입력 위젯 강제 리셋 (value= 인자가 반영되도록)
    st.session_state.ds_version = st.session_state.get("ds_version", 0) + 1

    params  = req.get("params",  {}) or {}
    headers = req.get("headers", {}) or {}

    # 이전 위젯 state 제거 (첫 번째 행이 무시되는 버그 방지)
    for k in list(st.session_state.keys()):
        if k.startswith("param_rows_") or k.startswith("header_rows_"):
            del st.session_state[k]

    st.session_state.param_rows = (
        [{"key": k, "value": v} for k, v in params.items()]
        or [{"key": "", "value": ""}]
    )
    st.session_state.header_rows = (
        [{"key": k, "value": v} for k, v in headers.items()]
        or [{"key": "", "value": ""}]
    )
    st.session_state.body_draft      = req.get("body") or ""
    st.session_state.ace_version     = st.session_state.get("ace_version", 0) + 1
    st.session_state.current_response = None


# ── 퍼블릭 렌더 함수 ──────────────────────────────────────────────────────

def render_sidebar() -> None:
    dm = DataSetManager()

    st.markdown("## 💾 Data Sets")

    datasets = dm.get_all()

    if not datasets:
        st.info("저장된 Data Set이 없습니다.\n요청 화면 하단에서 저장하세요.")
        return

    current_id = st.session_state.get("current_dataset_id")

    for i, entry in enumerate(datasets):
        req        = entry.get("request", {})
        method     = req.get("method", "GET")
        url        = req.get("url", "")
        name       = entry.get("name", "(이름 없음)")
        updated_at = entry.get("updated_at", "")[:16].replace("T", " ")
        color      = METHOD_COLORS.get(method, "#6c757d")
        short_url  = (url[:28] + "…") if len(url) > 30 else url
        is_current = entry["id"] == current_id

        with st.container(border=True):
            # 현재 로드된 Data Set 표시
            label = f"**{name}**" + (" ✏️" if is_current else "")
            st.markdown(label)

            st.markdown(
                f'<span style="background:{color};color:#fff;'
                f'padding:1px 7px;border-radius:4px;'
                f'font-size:0.72rem;font-weight:bold">{method}</span>'
                f'&nbsp;<span style="font-size:0.78rem;color:#888">{short_url}</span>',
                unsafe_allow_html=True,
            )
            st.caption(f"업데이트: {updated_at}")

            load_col, del_col = st.columns(2)
            with load_col:
                if st.button("불러오기", key=f"ds_load_{i}", use_container_width=True):
                    _load_dataset(entry)
                    st.rerun()
            with del_col:
                if st.button("삭제", key=f"ds_del_{i}", use_container_width=True):
                    dm.delete(entry["id"])
                    # 현재 로드된 항목이 삭제되면 상태 초기화
                    if entry["id"] == current_id:
                        st.session_state.current_dataset_id = None
                        st.session_state.dataset_name       = ""
                        st.session_state.ds_version = st.session_state.get("ds_version", 0) + 1
                    st.rerun()

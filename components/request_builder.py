import streamlit as st
from streamlit_ace import st_ace

from config import DEFAULT_TIMEOUT, HTTP_METHODS, METHOD_COLORS
from core.dataset_manager import DataSetManager
from core.http_client import send_request
from models.request_model import ApiRequest


# ── 키-값 편집기 (Params / Headers 공용) ──────────────────────────────────

def _kv_editor(state_key: str, kph: str = "Key", vph: str = "Value") -> dict:
    """
    session_state[state_key] 를 rows(list[dict]) 로 관리하는
    범용 키-값 테이블 에디터.
    반환값: {key: value, ...}  (빈 key 제외)
    """
    if state_key not in st.session_state:
        st.session_state[state_key] = [{"key": "", "value": ""}]

    rows   = st.session_state[state_key]
    to_del = None

    # 컬럼 헤더
    hc1, hc2, hc3 = st.columns([5, 5, 1])
    hc1.caption("Key")
    hc2.caption("Value")

    for i, row in enumerate(rows):
        c1, c2, c3 = st.columns([5, 5, 1])
        rows[i]["key"] = c1.text_input(
            "k", value=row.get("key", ""),
            key=f"{state_key}_k_{i}",
            placeholder=kph,
            label_visibility="collapsed",
        )
        rows[i]["value"] = c2.text_input(
            "v", value=row.get("value", ""),
            key=f"{state_key}_v_{i}",
            placeholder=vph,
            label_visibility="collapsed",
        )
        if c3.button("✕", key=f"{state_key}_d_{i}", help="행 삭제"):
            to_del = i

    if to_del is not None:
        rows.pop(to_del)
        st.rerun()

    if st.button("＋ 행 추가", key=f"{state_key}_add"):
        rows.append({"key": "", "value": ""})
        st.rerun()

    return {r["key"]: r["value"] for r in rows if r.get("key", "").strip()}


# ── 메인 렌더 함수 ─────────────────────────────────────────────────────────

def render_request_builder() -> None:
    cur = st.session_state.current_request

    # ── URL 바 ────────────────────────────────────────────────────────────
    c_method, c_url, c_send = st.columns([1.5, 7, 1.5])

    with c_method:
        method_idx = HTTP_METHODS.index(cur.method) if cur.method in HTTP_METHODS else 0
        method = st.selectbox(
            "Method", HTTP_METHODS,
            index=method_idx,
            label_visibility="collapsed",
        )

    with c_url:
        url = st.text_input(
            "URL", value=cur.url,
            placeholder="https://api.example.com/endpoint",
            label_visibility="collapsed",
        )

    with c_send:
        color = METHOD_COLORS.get(method, "#007bff")
        st.markdown(
            f"<style>.send-btn button{{background:{color}!important;"
            f"color:#fff!important;border:none!important;}}</style>",
            unsafe_allow_html=True,
        )
        send_clicked = st.button(
            "📤 Send", type="primary", use_container_width=True
        )

    # ── 요청 구성 탭 ──────────────────────────────────────────────────────
    no_body = method in ("GET", "HEAD", "OPTIONS")

    t_params, t_headers, t_body = st.tabs(
        ["📋 Params", "🔧 Headers", "📄 Body (JSON)"]
    )

    with t_params:
        params = _kv_editor("param_rows", "Parameter name", "Value")

    with t_headers:
        headers = _kv_editor("header_rows", "Header name", "Value")

    with t_body:
        if no_body:
            st.info(f"ℹ️ {method} 요청은 Body를 지원하지 않습니다.")
        else:
            st.caption("JSON 형식으로 입력하세요.")
            ace_key  = f"ace_body_{st.session_state.get('ace_version', 0)}"
            init_val = st.session_state.get("body_draft", cur.body or "")
            body_val = st_ace(
                value       = init_val,
                language    = "json",
                theme       = "monokai",
                height      = 250,
                key         = ace_key,
                auto_update = True,
                wrap        = True,
                font_size   = 14,
            )
            if body_val is not None:
                st.session_state.body_draft = body_val

    # ── Send 처리 ─────────────────────────────────────────────────────────
    if send_clicked:
        if not url.strip():
            st.error("❗ URL을 입력해주세요.")
            return

        body = (
            st.session_state.get("body_draft", "").strip() or None
            if not no_body
            else None
        )

        request = ApiRequest(
            method  = method,
            url     = url,
            params  = params,
            headers = headers,
            body    = body,
        )
        st.session_state.current_request = request

        with st.spinner("🔄 요청을 전송하는 중..."):
            response = send_request(request, timeout=DEFAULT_TIMEOUT)

        st.session_state.current_response = response
        st.rerun()

    # ── Data Set 저장 ─────────────────────────────────────────────────────
    st.divider()
    st.markdown("**💾 Data Set**")

    ds_ver = st.session_state.get("ds_version", 0)
    name_col, add_col, upd_col = st.columns([5, 1.5, 1.5])

    with name_col:
        ds_name = st.text_input(
            "Data Set 이름",
            value=st.session_state.get("dataset_name", ""),
            key=f"ds_name_{ds_ver}",
            placeholder="Data Set 이름을 입력하세요",
            label_visibility="collapsed",
        )
        st.session_state.dataset_name = ds_name

    current_ds_id = st.session_state.get("current_dataset_id")
    name_ok = bool(ds_name.strip())

    with add_col:
        add_clicked = st.button(
            "➕ 추가", disabled=not name_ok, use_container_width=True
        )
    with upd_col:
        upd_clicked = st.button(
            "🔄 업데이트",
            disabled=not (name_ok and current_ds_id),
            use_container_width=True,
        )

    if add_clicked or upd_clicked:
        body = (
            st.session_state.get("body_draft", "").strip() or None
            if not no_body
            else None
        )
        req = ApiRequest(method=method, url=url, params=params, headers=headers, body=body)
        dm  = DataSetManager()

        if upd_clicked and current_ds_id:
            dm.update(current_ds_id, ds_name.strip(), req)
            st.toast(f"'{ds_name.strip()}' 업데이트 완료!")
        else:
            new_id = dm.add(ds_name.strip(), req)
            st.session_state.current_dataset_id = new_id
            st.toast(f"'{ds_name.strip()}' 추가 완료!")

        st.rerun()

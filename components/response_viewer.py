import streamlit as st
from streamlit_ace import st_ace

from models.response_model import ApiResponse
from utils.formatters import error_hint, format_elapsed, format_size, status_badge_html


def render_response_viewer(response: ApiResponse) -> None:
    st.markdown("### 📨 Response")

    # ── 에러 처리 ─────────────────────────────────────────────────────────
    if response.error:
        st.error(f"**{response.error}**")
        hint = error_hint(response.error_type or "")
        if hint:
            st.warning(hint)
        return

    # ── 메타 정보 (Status / Time / Size) ─────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.caption("Status")
        st.markdown(
            status_badge_html(response.status_code),
            unsafe_allow_html=True,
        )
    with c2:
        st.caption("Time")
        st.markdown(f"⏱️ &nbsp;`{format_elapsed(response.elapsed_ms)}`",
                    unsafe_allow_html=True)
    with c3:
        st.caption("Size")
        st.markdown(f"📦 &nbsp;`{format_size(response.size_bytes)}`",
                    unsafe_allow_html=True)

    st.divider()

    # ── 응답 탭 ───────────────────────────────────────────────────────────
    tab_body, tab_headers = st.tabs(["📄 Body", "🔧 Headers"])

    with tab_body:
        # 언어 자동 감지
        body = response.body or ""
        lang = "html" if body.strip().startswith("<") else "json"

        # 읽기 전용 ace 에디터 (timestamp 를 key 에 포함 → 응답마다 리셋)
        st_ace(
            value       = body,
            language    = lang,
            theme       = "monokai",
            height      = 380,
            readonly    = True,
            key         = f"resp_body_{response.timestamp}",
            auto_update = False,
            wrap        = True,
            font_size   = 14,
        )

        # 텍스트 그대로 복사할 수 있도록 st.code 도 제공 (토글)
        with st.expander("📋 Raw 텍스트로 보기 (복사용)"):
            st.code(body, language=lang)

    with tab_headers:
        if response.headers:
            st.dataframe(
                [{"Header": k, "Value": v} for k, v in response.headers.items()],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("응답 헤더가 없습니다.")

# API Tester – 소프트웨어 설계 문서

> Version: 1.0.0 (MVP)
> 작성일: 2026-02-27
> 기술 스택: Python 3.9+, Streamlit, requests, streamlit-ace

---

## 1. 프로젝트 개요

Postman과 유사한 API 테스트 도구를 Streamlit 기반으로 구현한 웹 애플리케이션입니다.
별도 설치 없이 브라우저에서 HTTP 요청을 구성·전송하고 응답을 확인할 수 있습니다.

### 1.1 MVP 범위

| 기능 | 포함 여부 |
|------|-----------|
| HTTP 메서드 (GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS) | ✅ |
| Query Params / Headers / Body(JSON) 편집 | ✅ |
| 응답 뷰어 (Status, Time, Size, Body, Headers) | ✅ |
| JSON 코드 하이라이팅 (streamlit-ace) | ✅ |
| 요청 히스토리 (JSON 저장, 최근 50건) | ✅ |
| 에러 분류 및 힌트 메시지 | ✅ |
| Auth 탭 (Bearer/Basic/API Key) | ❌ Phase 2 |
| 컬렉션 관리 | ❌ Phase 2 |
| 환경변수 치환 (`{{var}}`) | ❌ Phase 2 |

---

## 2. 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        app.py (진입점)                       │
│           Session State 초기화 · 레이아웃 조립               │
├──────────────┬──────────────────────────────────────────────┤
│  UI Layer    │              Core Layer                      │
│              │                                              │
│  sidebar.py  │   http_client.py   history_manager.py        │
│  request_    │   (HTTP 실행)      (히스토리 CRUD)            │
│  builder.py  │                                              │
│  response_   │           Storage Layer                      │
│  viewer.py   │   file_storage.py  →  storage/data/          │
│              │   (JSON 읽기/쓰기)     history.json           │
├──────────────┴──────────────────────────────────────────────┤
│                      models/  utils/                        │
│            (dataclass)       (포매터·뱃지)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 디렉토리 구조

```
API_Tester/
├── app.py                      # 진입점: 페이지 설정, 세션 초기화, 레이아웃
├── config.py                   # 전역 상수 (경로, timeout, HTTP 메서드, 색상)
├── run.sh                      # venv 활성화 + 앱 실행 스크립트
├── requirements.txt
│
├── components/                 # Streamlit UI 컴포넌트
│   ├── sidebar.py              # 히스토리 패널 (조회·불러오기·삭제)
│   ├── request_builder.py      # URL바 + Params/Headers/Body 탭 + Send
│   └── response_viewer.py      # 응답 메타정보 + Body/Headers 탭
│
├── core/                       # 비즈니스 로직 (UI 독립)
│   ├── http_client.py          # requests 래퍼 + 에러 분류
│   └── history_manager.py      # 히스토리 CRUD (FileStorage 위임)
│
├── models/                     # 데이터 모델 (Python dataclass)
│   ├── request_model.py        # ApiRequest
│   └── response_model.py       # ApiResponse
│
├── storage/                    # 영속성 레이어
│   ├── file_storage.py         # JSON 파일 읽기/쓰기
│   └── data/
│       └── history.json        # 런타임 생성 (gitignore)
│
├── utils/
│   └── formatters.py           # 크기·시간 포매팅, HTML 뱃지, 에러 힌트
│
└── docs/
    ├── DESIGN.md               # 본 문서
    ├── INSTALL.md              # 설치 매뉴얼
    └── USER_MANUAL.md          # 사용자 매뉴얼
```

---

## 4. 데이터 모델

### 4.1 ApiRequest

```python
@dataclass
class ApiRequest:
    method:  str              # HTTP 메서드 (기본: "GET")
    url:     str              # 요청 URL
    params:  Dict[str, str]   # Query Parameters
    headers: Dict[str, str]   # Request Headers
    body:    Optional[str]    # JSON 문자열 (None = body 없음)
```

### 4.2 ApiResponse

```python
@dataclass
class ApiResponse:
    status_code: int           # HTTP 상태 코드 (0 = 에러)
    headers:     Dict[str,str] # 응답 헤더
    body:        str           # 응답 본문 (JSON pretty-print)
    elapsed_ms:  float         # 응답 시간 (밀리초)
    size_bytes:  int           # 응답 크기 (bytes)
    timestamp:   str           # ISO 8601 타임스탬프
    error:       Optional[str] # 에러 메시지 (None = 정상)
    error_type:  Optional[str] # 에러 분류 코드
```

### 4.3 히스토리 JSON 스키마

```json
[
  {
    "request": { "method": "GET", "url": "...", "params": {}, "headers": {}, "body": null },
    "response": { "status_code": 200, "headers": {}, "body": "...", "elapsed_ms": 123.4, ... }
  }
]
```

---

## 5. 핵심 모듈 상세

### 5.1 http_client.py — 에러 분류 체계

| error_type | 원인 | 힌트 |
|------------|------|------|
| `INVALID_URL` | schema 누락, 잘못된 URL | `http://` 또는 `https://` 확인 |
| `CONNECTION_ERROR` | DNS 실패, 서버 다운 | 도메인·네트워크 확인 |
| `TIMEOUT` | 서버 무응답 (30초 초과) | 서버 상태·방화벽 확인 |
| `SSL_ERROR` | 인증서 만료·자체서명 | 인증서 확인 |
| `UNKNOWN` | 기타 예외 | 콘솔 로그 확인 |

### 5.2 Session State 구조

```python
st.session_state = {
    "current_request":  ApiRequest(),        # 현재 편집 중인 요청
    "current_response": None,                # 마지막 수신 응답
    "param_rows":  [{"key":"","value":""}],  # Params 에디터 행 목록
    "header_rows": [{"key":"","value":""}],  # Headers 에디터 행 목록
    "body_draft":  "",                       # ace 에디터 임시 저장
    "ace_version": 0,                        # 히스토리 로드 시 ace 리셋 트리거
}
```

### 5.3 ace 에디터 동기화 전략

Streamlit의 매 rerun 특성상 ace 에디터 값을 `session_state.body_draft`에 항상 동기화하여,
Send 버튼 클릭 rerun 시에도 최신 Body 값이 유지되도록 설계합니다.

히스토리 불러오기 시에는 `ace_version`을 +1 증가시켜 ace editor key를 변경함으로써
강제 리셋(초기값 재설정)을 유발합니다.

---

## 6. 구현 단계 로드맵

```
Phase 1 (MVP) ✅ 완료
├── 기본 HTTP 요청/응답
├── Params / Headers / Body(JSON) 편집기
├── 응답 코드 하이라이팅 (streamlit-ace)
└── 요청 히스토리 (JSON 파일)

Phase 2 (예정)
├── Auth 탭 (Bearer Token, Basic Auth, API Key)
├── 환경변수 관리 및 {{variable}} 치환
├── 컬렉션 저장/불러오기
└── 응답 시간 차트

Phase 3 (예정)
├── Postman Collection v2.1 Import/Export
├── 응답 검증 테스트 스크립트
└── 다중 요청 연속 실행
```

---

## 7. 기술적 결정 사항

| 결정 항목 | 선택 | 이유 |
|-----------|------|------|
| 데이터 저장 | JSON 파일 | 의존성 없이 단순하게 구현 가능 |
| Body 타입 | JSON only | MVP 범위 최소화, 가장 보편적 형식 |
| 코드 에디터 | streamlit-ace | syntax highlighting + 읽기 전용 모드 지원 |
| HTTP 클라이언트 | requests | 가장 범용적인 Python HTTP 라이브러리 |
| 상태 관리 | st.session_state | Streamlit 공식 방식 |
| Auth | Phase 2 | MVP 복잡도 관리 |

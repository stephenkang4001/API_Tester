# API Tester – 설치 매뉴얼

> Version: 1.0.0 (MVP)
> 최종 수정: 2026-02-27

---

## 1. 시스템 요구사항

| 항목 | 최소 요구사항 |
|------|--------------|
| OS | macOS 11+, Ubuntu 20.04+, Windows 10+ |
| Python | 3.9 이상 |
| 메모리 | 512MB 이상 |
| 디스크 | 500MB 이상 (venv 포함) |
| 네트워크 | 인터넷 연결 (패키지 설치 시) |

---

## 2. 설치 방법 (권장: venv 사용)

### Step 1. 저장소 클론 또는 다운로드

```bash
git clone https://github.com/YOUR_USERNAME/API_Tester.git
cd API_Tester
```

> 또는 ZIP 파일을 다운로드한 경우:
> ```bash
> unzip API_Tester.zip
> cd API_Tester
> ```

---

### Step 2. Python 버전 확인

```bash
python3 --version
# Python 3.9.x 이상이어야 합니다.
```

---

### Step 3. 가상환경(venv) 생성

```bash
python3 -m venv .venv
```

> `.venv` 폴더가 프로젝트 루트에 생성됩니다.

---

### Step 4. 가상환경 활성화

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (cmd):**
```cmd
.venv\Scripts\activate.bat
```

활성화 성공 시 터미널 프롬프트 앞에 `(.venv)` 가 표시됩니다:
```
(.venv) $
```

---

### Step 5. 패키지 설치

```bash
pip install -r requirements.txt
```

설치되는 주요 패키지:

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `streamlit` | ≥ 1.30.0 | UI 프레임워크 |
| `requests` | ≥ 2.31.0 | HTTP 클라이언트 |
| `streamlit-ace` | ≥ 0.1.1 | JSON 코드 에디터 |

---

### Step 6. 앱 실행

**방법 A – 스크립트 사용 (macOS/Linux 권장):**
```bash
./run.sh
```

**방법 B – 직접 실행:**
```bash
# 가상환경이 활성화된 상태에서
streamlit run app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501` 에 접속됩니다.

---

## 3. 디렉토리 구조 (설치 후)

```
API_Tester/
├── .venv/              ← 가상환경 (gitignore, 직접 수정 금지)
├── storage/
│   └── data/
│       └── history.json  ← 앱 실행 후 자동 생성 (gitignore)
└── ...
```

---

## 4. 업그레이드

최신 버전으로 업데이트할 때:

```bash
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 5. 가상환경 비활성화

작업 종료 후:
```bash
deactivate
```

---

## 6. 문제 해결 (Troubleshooting)

### 6.1 `streamlit: command not found`

venv 활성화 후 재시도하거나, 직접 python 모듈로 실행:
```bash
python3 -m streamlit run app.py
```

### 6.2 패키지 설치 실패 (SSL Error)

```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### 6.3 포트 충돌 (이미 8501 사용 중)

다른 포트로 실행:
```bash
streamlit run app.py --server.port 8502
```

### 6.4 `ModuleNotFoundError`

venv가 활성화되지 않은 상태일 수 있습니다:
```bash
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
streamlit run app.py
```

### 6.5 Windows에서 PowerShell 실행 정책 오류

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 7. 제거 방법

### 가상환경만 제거 (앱 파일 유지)
```bash
rm -rf .venv
```

### 히스토리 초기화
```bash
rm -f storage/data/history.json
```

### 완전 제거
```bash
cd ..
rm -rf API_Tester
```

---

## 8. 의존성 전체 목록

`requirements.txt` 설치 시 함께 설치되는 패키지:

```
altair, attrs, blinker, cachetools, certifi, charset-normalizer,
click, gitdb, gitpython, idna, jinja2, jsonschema, markupsafe,
narwhals, numpy, packaging, pandas, pillow, protobuf, pyarrow,
pydeck, python-dateutil, pytz, referencing, rpds-py, six, smmap,
streamlit, streamlit-ace, tenacity, toml, tornado,
typing-extensions, tzdata, urllib3
```

> 모두 `streamlit` 의존성 패키지이며, 직접 수정하지 않아도 됩니다.

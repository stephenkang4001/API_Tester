#!/bin/bash
# API Tester 실행 스크립트
# 사용법: ./run.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# venv 활성화
source .venv/bin/activate

# 앱 실행
echo "🚀 API Tester 시작 중..."
streamlit run app.py

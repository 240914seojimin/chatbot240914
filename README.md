# 💬 챗봇 템플릿

OpenAI 모델을 사용해 챗봇을 만드는 방법을 보여주는 간단한 Streamlit 앱 예제입니다.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

### 로컬에서 실행하는 방법

1. 의존성 설치

   ```bash
   pip install -r requirements.txt
   ```

2. OpenAI API 키 설정

   앱에서 직접 입력하거나 `OPENAI_API_KEY` 환경 변수를 설정할 수 있습니다.

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. 앱 실행

   ```bash
   streamlit run streamlit_app.py
   ```

사용 방법(요약)

- **모델 설정:** 사이드바의 "모델 설정"을 열어 모델을 선택하세요. 드롭다운에서 모델을 바꿔가며 테스트할 수 있습니다.
- **시스템 프롬프트:** 시스템 프롬프트 텍스트 영역을 사용해 어시스턴트의 동작(컨텍스트)을 조절할 수 있습니다. 변경 시 대화의 첫 메시지로 반영됩니다.
- **온도(Temperature):** 슬라이더로 응답의 무작위성(창의성)을 조절합니다. 값이 낮을수록 보수적, 높을수록 창의적입니다.
- **최대 토큰:** 어시스턴트가 반환할 최대 토큰 수를 제한합니다.
- **스트리밍:** 사이드바에서 스트리밍 응답을 켜거나 끌 수 있으며, `대화 초기화` 버튼으로 대화를 초기화할 수 있습니다.

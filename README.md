# Korean Preprocessor(한국어 전처리기)

### Goal
데이터 처리 관련 라이브러리는 주로 파이썬 패키지로 제공된다. 따라서 만약 개발환경 언어가 파이썬이 아닌 경우에는 데이터 처리에 어려움을 겪었다. 이러한 문제를 개선하기 위해 데이터 처리 API를 제공하고, 이를 테스트하기 쉽도록 Swagger과 프로토타입을 모두 제공하기로 결정하였다.

프로토타이핑은 opyrator를 사용하는 편이었으나, 지나친 정형성으로 인해 직접 UI 역할을 하는 [streamlit](https://github.com/streamlit/streamlit)과 [FastAPI](https://github.com/tiangolo/fastapi)을 결합하여 컨테이너로 배포하도록 하였다. 

참고: 현재는 opyrator에 `Export To Docker Image` 기능이 추가되었다.
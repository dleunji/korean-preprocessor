# Korean Preprocessor(한국어 전처리기)
![스크린샷 2021-10-06 오후 5 45 03](https://user-images.githubusercontent.com/46207836/136170103-a357e088-763c-4ed1-9c60-f38e5daa449d.png)
## Goal
데이터 처리 관련 라이브러리는 주로 파이썬 패키지로 제공된다.<br> 따라서 만약 개발환경 언어가 파이썬이 아닌 경우에는 데이터 처리에 어려움을 겪었다.<br> 이러한 문제를 개선하기 위해 대표적으로 한국어 정규화 API를 제공하고, 이를 테스트하기 쉽도록 Swagger과 프로토타입을 배포하기로 결정하였다.

프로토타이핑은 간단하게 마이크로 서비스의 형태로 배포하는 오픈소스인 opyrator를 사용하는 편이었으나, 지나친 정형성으로 인해 직접 opyrator에 사용된 애플리케이션을 결합해 프로토타이핑을 진행하였다. UI 역할을 하는 [streamlit](https://github.com/streamlit/streamlit)과 [FastAPI](https://github.com/tiangolo/fastapi)을 결합하여 컨테이너로 배포하도록 하였다.<br>
참고로 현재는 opyrator에 `Export To Docker Image` 기능이 추가되었다.


## Deployment
Docker에서 한 컨테이너당 하나의 애플리케이션을 가동하고, 각각의 애플리케이션을 결합하는 MSA(Micro Service Architecture)의 형태로 설계할 것을 권장한다. 하지만 `docker-compose`를 사용하지 못하고 하나의 `dockerfile`만을 사용할 수 있다는 현재의 ainize의 특성상 `supervisord.conf`를 사용해 하나의 컨테이너에 streamlit과 FastAPI를 동시에 가동하는 방식을 활용하는 것도 하나의 방법이다.
따라서 배포를 위해 마이크로서비스와 모놀리식 아키텍처, 두 가지 모두 활용해보았다. 필요에 따라 두 가지 배포 방식 중 편리한 방식을 사용하면 된다.

## 1. Monolitic Architecture
컨테이너에 두 가지 애플리케이션을 동시에 띄우기 위해 프로세스를 모니터링하고 관리하는 프로그램인 `supervisord`를 사용한다.<br>참고로 현재는 간단한 프로젝트 구동을 위한 최소한의 명령어로만 구성되어있으므로 안정적인 컨테이너 구동을 위해서는 추가 옵션을 더해야한다. <br> 이 프로젝트에는 각각의 프로그램의 실행 명령어, 환경 설정만이 되어있다.<br>
중요한 점은 **nodaemon=true**이다. nodaemon이 `true`로 설정하여 foreground로 활동하도록 하여 컨테이너 라이프사이클을 직접 관리하도록 한다.

그리고 프론트엔드와 백엔드 애플리케이션을 각각 구동한다.<br>여기에서는 따로 에러 로그를 따로 핸들링할 필요가 없다고 판단하여 아래와 같이 설정하였다.

```conf
[supervisord]
nodaemon=true

[program:fastapi]
command=/bin/bash -c "uvicorn server:app --host 0.0.0.0 --port 8000"
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:streamlit]
command=/bin/bash -c "streamlit run ui.py"
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```
이러한 하나의 실행파일인 `supervisord.conf`를 실행할 수 있도록 dockerfile을 작성한다. streamlit의 default port는 8501, FastAPI의 default port는 8000이라는 점을 참고하여 8501, 8000포트를 모두 `EXPOSE`한다.
```docker
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
RUN mkdir -p /etc/supervisor/conf.d
...
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
```
상세한 내용은 Dockerfile을 참고하면 된다.

### Execution
빌드한 다음 `docker run -p 8501:8501 image_name`을 실행함으로써 한 컨테이너에 streamlit과 FastAPI를 동시에 실행할 수 있다.
추가적으로 컨테이너의 8000번 포트 또한 호스트 포트에 매핑하도록 하여 호스트에서 FastAPI에도 접근가능하도록 한다. `docker run -p 8501:8501 -p 8000:8000 image_name`을 실행함으로써 `0.0.0.0/8000`에 접속한 후 FastAPI의 Swagger를 활용할 수 있다. 편의상 호스트 포트와 컨테이너의 포트를 동일하게 처리하였다.

![스크린샷 2021-10-06 오후 5 50 32](https://user-images.githubusercontent.com/46207836/136170980-c3fe5a1e-d7f2-467d-b67f-8398c915e785.png)

## 2. Microservice Architecure
`supervisord.conf`를 사용하였던 1번과 달리 `docker-compose.yml`을 사용하여 컨테이너 2개를 동시에 띄우고 컨테이너 간 통신을 통해 애플리케이션을 구동할 수 있다.
```yaml
version: '3'
services:
  fastapi:
    build: fastapi/
    ports:
      - "8000:8000"
    networks:
      - deploy_network  
  streamlit:
    build: streamlit/
    depends_on:
      - fastapi
    ports:
      - "8501:8501"
    expose:
      - "8000"
      - "8501"
    networks:
      - deploy_network
networks:
  deploy_network:
    driver: bridge
```
컨테이너별 관리가 용이하도록 일부 파일의 위치도 재조정하였으니 구체적인 내용은 branch 'msa'에 확인 가능하다.
아래 명령어로 실행 또한 가능하다.
```
docker-compose up --build -d
```

## Reference
- https://advancedweb.hu/supervisor-with-docker-lessons-learned/
- https://docs.microsoft.com/ko-kr/dotnet/architecture/microservices/multi-container-microservice-net-applications/multi-container-applications-docker-compose
- https://docs.docker.com/compose/gettingstarted/
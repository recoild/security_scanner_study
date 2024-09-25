# Dockerfile
FROM python:3.9-slim

# 필요한 패키지 설치
RUN pip install --no-cache-dir requests

# Trivy 설치
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/aquasecurity/trivy/releases/download/v0.55.2/trivy_0.55.2_Linux-64bit.tar.gz \
    && tar zxvf trivy_0.55.2_Linux-64bit.tar.gz \
    && mv trivy /usr/local/bin/ \
    && rm trivy_0.55.2_Linux-64bit.tar.gz


# 작업 디렉터리 설정
WORKDIR /app

# 코드 복사
COPY . .

# 메일 전송 스크립트 복사
COPY send_email.py .

CMD ["python", "send_email.py"]

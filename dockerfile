# Python 3.12 slim 이미지를 베이스로 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app



# 필요한 시스템 패키지 설치 및 Trivy 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gcc \
    libpq-dev \
    && TRIVY_VERSION="0.55.2" \
    && wget https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-64bit.deb \
    && dpkg -i trivy_${TRIVY_VERSION}_Linux-64bit.deb \
    && rm trivy_${TRIVY_VERSION}_Linux-64bit.deb \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 종속성 파일 복사
COPY requirements.txt .

# 종속성 설치 (캐시 사용 방지를 위해 --no-cache-dir 옵션 사용)
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Flask 환경 변수 설정
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Flask 서버 실행 포트 설정
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "app.py"]

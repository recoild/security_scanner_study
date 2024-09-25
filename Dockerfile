# Python 3.7-alpine 이미지를 기반으로 설정
FROM python:3.7-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 목록 복사 및 설치
COPY requirements.txt /app
RUN pip install -r requirements.txt

# 애플리케이션 파일 복사
COPY . /app

# 애플리케이션 실행
CMD ["python", "app.py"]
from flask import Flask, render_template, request, redirect, url_for
import os
import json
import smtplib
import subprocess
from email.mime.text import MIMEText

app = Flask(__name__)

def send_email(body, sender_email, password):
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # 이메일 구성
    msg = MIMEText(body)
    msg['Subject'] = 'Trivy Vulnerability Report'
    msg['From'] = sender_email
    msg['To'] = sender_email  # 수신자 이메일도 본인으로 설정

    # 이메일 전송
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS 보안 연결 시작
            server.login(sender_email, password)  # 애플리케이션 비밀번호 사용
            server.send_message(msg)  # 이메일 전송
            print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")

def scan_repository(repo_url):
    # Trivy를 사용하여 Git 저장소 취약점 검사
    command = f"trivy repo --format json -o result.json {repo_url}"
    subprocess.run(command, shell=True)
    
    # JSON 파일 읽기
    with open('result.json', 'r') as file:
        scan_result = json.load(file)
    
    vulnerabilities = scan_result['Results'][0].get('Vulnerabilities', [])
    return vulnerabilities

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_image():
    # 폼에서 입력된 값 받기
    sender_email = request.form['email']
    password = request.form['password']
    repo_url = request.form['repo_url']

    # Git 레포지토리 스캔
    vulnerabilities = scan_repository(repo_url)
    
    # 취약점 정보를 텍스트로 변환
    if vulnerabilities:
        vulnerability_info = "\n".join([f"{vuln['Title']}: {vuln['Severity']}" for vuln in vulnerabilities])
    else:
        vulnerability_info = "취약점이 발견되지 않았습니다."

    # 이메일로 취약점 정보 전송
    send_email(vulnerability_info, sender_email, password)

    return render_template('result.html', vulnerabilities=vulnerabilities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


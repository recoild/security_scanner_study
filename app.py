from flask import Flask, render_template, request
import os
import json
import smtplib
import subprocess
from email.mime.text import MIMEText

app = Flask(__name__)

sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('EMAIL_PASSWORD')


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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan_image():
    docker_images = request.form.getlist('docker_image')  # 여러 URL을 받음
    all_vulnerabilities = {}

    for docker_image in docker_images:
        # Trivy 명령어 실행, 결과를 JSON 파일로 저장
        result_file = f'result_{docker_image.replace("/", "_")}.json'
        os.system(f'rm -f {result_file}')
        os.system(f'trivy repo --format json -o {result_file} {docker_image}')

        # JSON 파일 읽기
        if os.path.exists(result_file):
            with open(result_file, 'r') as file:
                scan_result = json.load(file)

            if scan_result.get('Results'):
                vulnerabilities = scan_result['Results'][0].get('Vulnerabilities', [])
                all_vulnerabilities[docker_image] = vulnerabilities

    # 메일에 포함할 문자열 생성
    vulnerability_info = ""
    for docker_image, vulnerabilities in all_vulnerabilities.items():
        vulnerability_info += f"Image: {docker_image}\n"
        if vulnerabilities:
            for vuln in vulnerabilities:
                vulnerability_info += f"- {vuln['Title']}: {vuln['Severity']}\n"
        else:
            vulnerability_info += "No vulnerabilities found.\n"
        vulnerability_info += "\n"  # 이미지별로 구분하기 위해 개행 추가

    # 생성된 문자열을 이메일로 전송
    send_email(vulnerability_info, sender_email, password)

    return render_template('result.html', all_vulnerabilities=all_vulnerabilities)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

import smtplib
import subprocess
from email.mime.text import MIMEText

def send_email(body):
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "kyw4330@gmail.com"  # 본인의 Gmail 주소
    password = ""  # Gmail 앱 비밀번호

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
    command = f"trivy repo {repo_url}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    repo_url = "https://github.com/yuwankang/01.lab.git"
    vulnerabilities = scan_repository(repo_url)
    send_email(vulnerabilities)

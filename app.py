from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_image():
    docker_image = request.form['docker_image']
    
    # Trivy 명령어 실행, JSON 파일로 저장
    os.system(f'trivy repo --format json -o result.json {docker_image}')
    
    # JSON 파일 읽기
    with open('result.json', 'r') as file:
        scan_result = json.load(file)
    
    vulnerabilities = scan_result['Results'][0]['Vulnerabilities']
    
    return render_template('result.html', vulnerabilities=vulnerabilities)

if __name__ == '__main__':
    app.run(debug=True)

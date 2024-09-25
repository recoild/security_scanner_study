import requests
import json

# Elasticsearch 인덱스 URL
es_url = "http://localhost:9200/trivy-vulnerabilities/_doc/"

# Trivy 결과 파일 로드
with open("results.json", "r") as file:
    data = json.load(file)

# Elasticsearch에 데이터 전송
for vuln in data['Results'][0]['Vulnerabilities']:
    response = requests.post(es_url, json=vuln)
    print(response.status_code, response.json())

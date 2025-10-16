# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Flask 설치
RUN pip install --no-cache-dir flask

# 버전 파일 복사
COPY VERSION .

# 앱 파일 복사
COPY app.py .
COPY vcardToCSV.py .

# 템플릿 폴더 복사
COPY templates/ templates/

# 정적 파일 복사
COPY static/ static/

# 포트 노출
EXPOSE 5000

# 앱 실행
CMD ["python", "app.py"]


# ===========================================
# docker-compose.yml (편의성을 위해)
# ===========================================
# version: '3.8'
# services:
#   vcf-converter:
#     build: .
#     ports:
#       - "5000:5000"
#     volumes:
#       - ./app.py:/app/app.py


# ===========================================
# 사용 방법
# ===========================================

# 1. 프로젝트 디렉토리 구조:
#    vcf-web-converter/
#    ├── Dockerfile
#    ├── app.py (이전 아티팩트의 Flask 코드를 이 파일로 저장)
#    └── docker-compose.yml (선택사항)

# 2. Docker 이미지 빌드:
#    docker build -t vcf-web-converter .

# 3. 컨테이너 실행:
#    docker run -p 5000:5000 vcf-web-converter

# 4. 브라우저에서 접속:
#    http://localhost:5000

# 5. VCF 파일 업로드하고 CSV로 다운로드!

# ===========================================
# Docker Compose 사용 (더 편리함)
# ===========================================

# docker-compose up -d
# 
# 그러면 http://localhost:5000 에서 바로 사용 가능!
# 
# 종료: docker-compose down
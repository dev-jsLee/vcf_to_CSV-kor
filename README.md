# 📇 VCF to CSV 변환기

한글 연락처가 포함된 VCF(vCard) 파일을 CSV로 변환하는 웹 애플리케이션입니다.

## ✨ 주요 기능

- ✅ **한글 이름 자동 디코딩** - Quoted-Printable, Base64 인코딩 자동 처리
- ✅ **다양한 전화번호 포맷** - 사용자가 원하는 형식으로 변환
- ✅ **실시간 미리보기** - 선택한 포맷의 결과를 바로 확인
- ✅ **Excel 호환** - UTF-8 BOM으로 인코딩하여 Excel에서 바로 열기 가능
- ✅ **개인정보 보호** - 모든 처리가 로컬(또는 Docker 컨테이너)에서 진행

## 📱 전화번호 포맷 옵션

### 1. 숫자만
```
01012345678
'01012345678  (자동변환 방지 체크 시)
```
⚠️ **주의:** 자동변환 방지를 체크하지 않으면 Excel에서 전화번호가 숫자로 변환될 수 있습니다.

### 2. 대시 구분
```
010-1234-5678  (따옴표 없음)
'010-1234-5678 (따옴표 있음)
```

### 3. 공백 구분
```
010 1234 5678  (따옴표 없음)
'010 1234 5678 (따옴표 있음)
```

### 4. 커스텀 구분자
원하는 구분자를 직접 입력 (예: `.`, `/`, `_` 등)
```
010.1234.5678
010/1234/5678
```

### Excel 자동변환 방지 옵션
전화번호 앞에 작은따옴표(`'`)를 추가하여 Excel에서 숫자로 자동변환되는 것을 방지합니다.

**스마트 경고:**
- "숫자만" 선택 시 자동변환 방지가 체크되지 않으면 경고 메시지가 표시됩니다.
- 실시간 미리보기로 결과를 미리 확인할 수 있습니다.

## 🚀 사용 방법

### 방법 1: 자동 배포 스크립트 (권장)

버전 관리와 함께 자동으로 빌드 및 배포:

```cmd
# Major 버전 업데이트 (v1.0.0 -> v2.0.0)
deploy.cmd major

# Minor 버전 업데이트 (v1.0.0 -> v1.1.0)
deploy.cmd minor

# Hotfix 버전 업데이트 (v1.0.0 -> v1.0.1)
deploy.cmd hotfix
```

배포 스크립트가 자동으로:
- ✅ VERSION 파일 업데이트
- ✅ Docker 이미지 빌드 (버전 태그 + latest 태그)
- ✅ 기존 컨테이너 중지
- ✅ 새 컨테이너 실행

### 방법 2: 수동 Docker 빌드

```bash
# 1. Docker 이미지 빌드
docker build -t vcf-web-converter .

# 2. 컨테이너 실행
docker run -p 5000:5000 vcf-web-converter

# 3. 브라우저에서 접속
# http://localhost:5000
```

### 방법 3: Python 직접 실행

```bash
# 1. 의존성 설치
pip install flask

# 2. 앱 실행
python app.py

# 3. 브라우저에서 접속
# http://localhost:5000
```

### 방법 4: 명령줄 스크립트 (vcardToCSV.py)

```bash
python vcardToCSV.py
```

실행 후 VCF 파일 경로를 입력하면 자동으로 CSV 파일이 생성됩니다.

## 🔧 코드 구조

```
extract_phones/
├── app.py                    # Flask 웹 애플리케이션 (261줄)
├── templates/
│   └── index.html           # HTML 템플릿 (80줄)
├── static/
│   ├── css/
│   │   └── style.css        # CSS 스타일 (260줄)
│   └── js/
│       └── script.js        # JavaScript (100줄)
├── vcardToCSV.py            # CLI 변환 스크립트
├── Dockerfile               # Docker 설정
├── VERSION                  # 버전 정보 (2.1.0)
├── deploy.config            # 배포 설정 (개인 설정, gitignore)
├── deploy.config.example    # 배포 설정 예시
├── deploy.cmd               # 자동 배포 스크립트
├── version.cmd              # 버전 확인 스크립트
├── DEPLOY_GUIDE.md          # 배포 가이드
├── TEMPLATE_GUIDE.md        # 템플릿 가이드 (AI/개발자용)
└── README.md                # 이 파일
```

> 💡 **이 프로젝트를 템플릿으로 사용하고 싶으신가요?**  
> [`TEMPLATE_GUIDE.md`](TEMPLATE_GUIDE.md) 문서를 참고하세요. AI 어시스턴트와 개발자를 위한 상세한 구조 설명이 포함되어 있습니다.

## 📦 버전 관리 및 배포

### 1️⃣ 첫 설정: 배포 구성 파일 생성
```cmd
# 예제 파일을 복사하여 본인의 설정으로 수정
copy deploy.config.example deploy.config
# 그리고 deploy.config를 편집하여 본인의 정보를 입력하세요
```

**deploy.config 예시:**
```ini
DEPLOYER=jslee7518              # Docker Hub 사용자명
IMAGE_NAME=vcftocsv             # 이미지 이름
CONTAINER_NAME=vcftocsv         # 컨테이너 이름
HOST_PORT=5000                  # 호스트 포트
CONTAINER_PORT=5000             # 컨테이너 포트
PUSH_TO_REGISTRY=false          # Docker Hub 자동 푸시 여부
```

이렇게 설정하면 이미지가 `jslee7518/vcftocsv:v1.0.0` 형태로 생성됩니다.

### 2️⃣ 버전 확인
```cmd
version.cmd
```

### 3️⃣ 배포 (버전 자동 업데이트)

**Major 버전** - 대규모 변경, API 호환성 깨짐
```cmd
deploy.cmd major
# v1.0.0 -> v2.0.0
```

**Minor 버전** - 새 기능 추가, 하위 호환 유지
```cmd
deploy.cmd minor
# v1.0.0 -> v1.1.0
```

**Hotfix 버전** - 버그 수정, 패치
```cmd
deploy.cmd hotfix
# v1.0.0 -> v1.0.1
```

### Docker 이미지 태그
각 배포는 두 개의 태그를 생성합니다:
- `jslee7518/vcftocsv:2.1.0` (특정 버전)
- `jslee7518/vcftocsv:latest` (최신 버전)

### Docker Hub에 푸시하기
`deploy.config`에서 `PUSH_TO_REGISTRY=true`로 설정하면 배포 시 자동으로 Docker Hub에 푸시됩니다.

```cmd
# 먼저 Docker Hub 로그인 (최초 1회)
docker login

# 그 후 deploy.cmd 실행 시 자동 푸시
deploy.cmd hotfix
```

### 유용한 Docker 명령어
```cmd
# 실행 중인 컨테이너 확인
docker ps

# 로그 확인
docker logs vcftocsv

# 컨테이너 중지/시작
docker stop vcftocsv
docker start vcftocsv

# 특정 버전 실행
docker run -d -p 5000:5000 jslee7518/vcftocsv:2.1.0
```

## 🎯 지원하는 인코딩

- UTF-8 (Quoted-Printable)
- Base64
- EUC-KR / CP949
- ISO-8859-1

## 💡 사용 예시

1. **웹 브라우저에서**:
   - VCF 파일을 드래그 앤 드롭 또는 클릭하여 선택
   - 원하는 전화번호 포맷 선택
   - 미리보기로 결과 확인
   - "CSV로 변환하기" 버튼 클릭
   - 변환된 CSV 파일 자동 다운로드

2. **명령줄에서**:
   ```bash
   python vcardToCSV.py
   # VCF 파일 경로 입력 (예: contacts.vcf)
   # 자동으로 contacts.csv 생성
   ```

## 📊 CSV 출력 형식

| 이름 | 전화번호1 | 전화번호2 | 전화번호3 | 이메일1 | 이메일2 | 회사 | 메모 |
|------|----------|----------|----------|---------|---------|------|------|
| 홍길동 | '010-1234-5678 | '02-1234-5678 | | hong@example.com | | 삼성전자 | |
| 김철수 | '010-9876-5432 | | | | | | |

## 🐛 문제 해결

### 한글이 깨져 보일 때
- Excel에서 열 때: "데이터" 탭 > "텍스트 나누기" > "구분 기호로 분리됨" > UTF-8 선택
- 또는 Google Sheets에서 열면 자동으로 UTF-8 인식

### 전화번호가 숫자로 변환될 때
- "Excel 자동변환 방지" 옵션을 체크하거나
- "작은따옴표 + 숫자" 포맷 선택

## 📝 라이선스

MIT License

## 🙏 개선 사항

**v2.1 (최신)**
- ✅ 스마트 경고 시스템 - "숫자만" 선택 시 자동변환 방지 권장 알림
- ✅ UI 간소화 - 불필요한 옵션 제거
- ✅ 사용성 개선 - 더 직관적인 포맷 선택
- ✅ 코드 구조 개선 - HTML/CSS/JS 완전 분리
  - app.py: 658줄 → 261줄
  - index.html: 396줄 → 80줄
  - 표준 Flask 프로젝트 구조 적용

**v2.0**
- ✅ 사용자가 전화번호 포맷을 선택할 수 있는 기능 추가
- ✅ 실시간 미리보기 기능
- ✅ 커스텀 구분자 입력 기능
- ✅ Excel 자동변환 방지 옵션

**v1.0**
- ✅ 한글 인코딩 개선 (UTF-8 우선 디코딩)
- ✅ 다양한 전화번호 형식 지원
- ✅ 웹 UI 개선


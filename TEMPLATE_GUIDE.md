# 🎨 Flask 프로젝트 템플릿 가이드

> **목적**: 이 문서는 Flask 웹 애플리케이션의 표준화된 개발 및 배포 구조를 설명합니다.  
> **대상**: AI 코딩 어시스턴트, 개발자, 새 프로젝트를 시작하는 팀

---

## 📋 목차

1. [템플릿 개요](#템플릿-개요)
2. [프로젝트 구조](#프로젝트-구조)
3. [핵심 설계 원칙](#핵심-설계-원칙)
4. [파일별 상세 설명](#파일별-상세-설명)
5. [배포 시스템](#배포-시스템)
6. [새 프로젝트 적용 가이드](#새-프로젝트-적용-가이드)
7. [AI 어시스턴트를 위한 가이드](#ai-어시스턴트를-위한-가이드)

---

## 🎯 템플릿 개요

### 핵심 철학

이 템플릿은 다음 원칙을 기반으로 설계되었습니다:

1. **관심사의 분리 (Separation of Concerns)**
   - HTML, CSS, JavaScript를 각각 별도 파일로 분리
   - 애플리케이션 로직과 프레젠테이션 완전 분리

2. **설정의 외부화 (Configuration Externalization)**
   - 배포 설정을 별도 파일(`deploy.config`)로 관리
   - 개인 설정과 공유 코드 분리 (`.gitignore` 활용)

3. **자동화 우선 (Automation First)**
   - 버전 관리 자동화 (Semantic Versioning)
   - Docker 빌드/배포 자동화
   - 단일 명령어로 전체 배포 완료

4. **표준 준수 (Standards Compliance)**
   - Flask 프로젝트 표준 구조 사용
   - Semantic Versioning 2.0.0 준수
   - Docker 베스트 프랙티스 적용

### 적용 대상

이 템플릿은 다음과 같은 프로젝트에 적합합니다:

- ✅ Flask 기반 웹 애플리케이션
- ✅ Docker로 배포되는 프로젝트
- ✅ Windows 환경에서 개발/배포
- ✅ 버전 관리가 중요한 프로젝트
- ✅ 여러 개발자가 협업하는 프로젝트

---

## 📁 프로젝트 구조

```
project_root/
│
├── app.py                      # Flask 애플리케이션 메인 파일
│   ├── Flask 앱 초기화
│   ├── 라우트 정의
│   ├── 비즈니스 로직
│   └── get_version() 함수 (VERSION 파일 읽기)
│
├── templates/                  # Jinja2 템플릿 디렉토리
│   └── index.html             # HTML 구조만 포함
│       ├── {{ url_for('static', ...) }} 사용
│       └── {{ version }} 등 템플릿 변수 사용
│
├── static/                     # 정적 파일 디렉토리
│   ├── css/
│   │   └── style.css          # 모든 CSS 스타일
│   └── js/
│       └── script.js          # 모든 JavaScript 로직
│
├── Dockerfile                  # Docker 이미지 빌드 설정
│   ├── Python 베이스 이미지
│   ├── 의존성 설치
│   ├── 앱 파일 복사
│   └── 실행 명령어
│
├── VERSION                     # 버전 번호 파일 (MAJOR.MINOR.HOTFIX)
│   └── 예: 2.1.0
│
├── deploy.config              # 배포 설정 파일 (개인, .gitignore)
│   ├── DEPLOYER (Docker Hub 사용자명)
│   ├── IMAGE_NAME (이미지 이름)
│   ├── CONTAINER_NAME (컨테이너 이름)
│   ├── HOST_PORT / CONTAINER_PORT
│   ├── PUSH_TO_REGISTRY (자동 푸시 여부)
│   └── REGISTRY (레지스트리 URL)
│
├── deploy.config.example      # 배포 설정 예시 (Git 커밋)
│   └── 다른 개발자를 위한 템플릿
│
├── deploy.cmd                 # 배포 자동화 스크립트 (Windows)
│   ├── deploy.config 로드
│   ├── 버전 증가 (major/minor/hotfix)
│   ├── Docker 이미지 빌드
│   ├── Docker Hub 푸시 (선택)
│   ├── 기존 컨테이너 중지/제거
│   └── 새 컨테이너 시작
│
├── version.cmd                # 버전 확인 스크립트
│   ├── 현재 버전 표시
│   ├── 배포 설정 표시
│   └── Docker 이미지 목록
│
├── README.md                  # 프로젝트 문서
│   ├── 프로젝트 소개
│   ├── 설치 및 실행 방법
│   ├── 배포 가이드
│   └── 기능 설명
│
├── DEPLOY_GUIDE.md            # 상세 배포 가이드
│   ├── 첫 설정 방법
│   ├── 버전 관리 전략
│   ├── 배포 프로세스
│   └── 트러블슈팅
│
├── TEMPLATE_GUIDE.md          # 이 문서 (템플릿 가이드)
│   └── AI와 개발자를 위한 구조 설명
│
└── .gitignore                 # Git 무시 파일
    ├── __pycache__/
    ├── *.pyc
    ├── deploy.config          # 개인 설정 제외
    └── test_*, temp_* 등
```

---

## 🏗️ 핵심 설계 원칙

### 1. 관심사의 분리

#### HTML/CSS/JS 분리

**나쁜 예 (Anti-pattern):**
```python
# app.py
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: blue; }  <!-- CSS가 HTML 안에 -->
    </style>
</head>
<body>
    <script>
        function hello() { ... }  <!-- JS가 HTML 안에 -->
    </script>
</body>
</html>
"""
```

**좋은 예 (이 템플릿의 방식):**
```python
# app.py
@app.route('/')
def index():
    return render_template('index.html', version=APP_VERSION)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```

**장점:**
- 각 파일이 단일 책임만 수행
- 브라우저 캐싱 활용 (CSS/JS 파일 캐시)
- 유지보수 용이 (CSS 수정 시 CSS 파일만 편집)
- 협업 효율성 (디자이너는 CSS, 개발자는 JS)

### 2. 설정의 외부화

#### 배포 설정 분리

**핵심 아이디어:**
- 코드에 하드코딩된 설정 제거
- 개인별 다른 설정 사용 가능
- Git에 민감한 정보 커밋 방지

**구현 방법:**

```batch
# deploy.cmd에서 설정 파일 읽기
for /f "usebackq tokens=1,* delims==" %%a in ("deploy.config") do (
    set "line=%%a"
    if not "!line:~0,1!"=="#" (
        if not "%%a"=="" (
            if not "%%b"=="" (
                set "%%a=%%b"
            )
        )
    )
)
```

**설정 파일 구조:**

```ini
# deploy.config
DEPLOYER=username              # 개발자마다 다름
IMAGE_NAME=myapp               # 프로젝트별로 다름
CONTAINER_NAME=myapp-container
HOST_PORT=5000
CONTAINER_PORT=5000
PUSH_TO_REGISTRY=false
REGISTRY=
```

**Git 관리:**

```gitignore
# .gitignore
deploy.config                  # 개인 설정 제외
```

```ini
# deploy.config.example (Git 커밋)
DEPLOYER=your-dockerhub-username
IMAGE_NAME=your-app-name
...
```

### 3. Semantic Versioning 자동화

#### 버전 번호 규칙

```
MAJOR.MINOR.HOTFIX

예: 2.1.3
     │ │ │
     │ │ └─ Hotfix: 버그 수정, 패치
     │ └─── Minor: 새 기능, 하위 호환
     └───── Major: API 변경, 호환성 깨짐
```

#### 자동 증가 로직

```batch
# deploy.cmd
if /i "!VERSION_TYPE!"=="major" (
    set /a MAJOR+=1
    set "MINOR=0"
    set "HOTFIX=0"
) else if /i "!VERSION_TYPE!"=="minor" (
    set /a MINOR+=1
    set "HOTFIX=0"
) else if /i "!VERSION_TYPE!"=="hotfix" (
    set /a HOTFIX+=1
)
```

#### 사용 예시

```cmd
# 현재: v2.1.3

deploy.cmd hotfix   # → v2.1.4 (버그 수정)
deploy.cmd minor    # → v2.2.0 (새 기능)
deploy.cmd major    # → v3.0.0 (대규모 변경)
```

### 4. Docker 이미지 태그 전략

#### 이미지 태그 형식

```
[DEPLOYER/]IMAGE_NAME:VERSION
[DEPLOYER/]IMAGE_NAME:latest

예:
jslee7518/vcftocsv:2.1.0
jslee7518/vcftocsv:latest
```

#### 태그 생성 로직

```batch
# deploy.cmd
if not "%DEPLOYER%"=="" (
    set "IMAGE_TAG=%DEPLOYER%/%IMAGE_NAME%"
) else (
    set "IMAGE_TAG=%IMAGE_NAME%"
)

docker build -t !IMAGE_TAG!:!NEW_VERSION! -t !IMAGE_TAG!:latest .
```

#### 장점

- 특정 버전 롤백 가능: `docker run myapp:2.0.0`
- 최신 버전 간편 사용: `docker run myapp:latest`
- Docker Hub 네임스페이스 관리
- 팀별/프로젝트별 구분 명확

---

## 📄 파일별 상세 설명

### app.py (Flask 애플리케이션)

**핵심 구조:**

```python
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# 1. 버전 정보 읽기
def get_version():
    """VERSION 파일에서 버전 정보를 읽어옴"""
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return '1.0.0'

APP_VERSION = get_version()

# 2. 비즈니스 로직 함수들
def process_data(data):
    # 핵심 로직 구현
    pass

# 3. 라우트 정의
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # POST 처리
        pass
    # 템플릿 렌더링 (버전 정보 전달)
    return render_template('index.html', version=APP_VERSION)

@app.route('/api/data', methods=['POST'])
def api_endpoint():
    # API 엔드포인트
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**중요 포인트:**

1. **버전 정보 관리**
   ```python
   APP_VERSION = get_version()  # 전역 변수로 한 번만 읽기
   ```

2. **템플릿 변수 전달**
   ```python
   render_template('index.html', version=APP_VERSION, data=data)
   ```

3. **Docker 호환성**
   ```python
   app.run(host='0.0.0.0', port=5000)  # 모든 인터페이스에서 접근 가능
   ```

### templates/index.html

**핵심 구조:**

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>앱 이름</title>
    
    <!-- CSS 링크 (Flask url_for 사용) -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>앱 이름 <span class="version">v{{ version }}</span></h1>
        
        <!-- HTML 구조만 포함 -->
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" id="fileInput">
            <button type="submit">업로드</button>
        </form>
    </div>
    
    <!-- JavaScript 링크 -->
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```

**중요 포인트:**

1. **Flask 템플릿 문법**
   ```html
   {{ variable }}                    <!-- 변수 출력 -->
   {% if condition %}...{% endif %}  <!-- 조건문 -->
   {% for item in items %}...{% endfor %}  <!-- 반복문 -->
   {{ url_for('static', filename='css/style.css') }}  <!-- 정적 파일 URL -->
   ```

2. **인라인 스타일/스크립트 금지**
   - `<style>` 태그 사용 금지 → `style.css`로 분리
   - `<script>` 태그 내 코드 금지 → `script.js`로 분리

### static/css/style.css

**구조 예시:**

```css
/* 전역 스타일 */
* { 
    margin: 0; 
    padding: 0; 
    box-sizing: border-box; 
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f5f5f5;
}

/* 컴포넌트별 스타일 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.button {
    background: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
}
```

### static/js/script.js

**구조 예시:**

```javascript
// DOM 요소 선택
const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');

// 이벤트 리스너
fileInput.addEventListener('change', handleFileSelect);
uploadButton.addEventListener('click', handleUpload);

// 함수 정의
function handleFileSelect(event) {
    const file = event.target.files[0];
    console.log('File selected:', file.name);
}

function handleUpload() {
    // 업로드 로직
}

// 초기화
document.addEventListener('DOMContentLoaded', function() {
    console.log('App initialized');
});
```

### Dockerfile

**표준 구조:**

```dockerfile
# 1. 베이스 이미지
FROM python:3.9-slim

# 2. 작업 디렉토리
WORKDIR /app

# 3. 의존성 파일 복사 및 설치 (캐싱 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 또는 Flask만 사용하는 경우
RUN pip install --no-cache-dir flask

# 4. 버전 파일 복사
COPY VERSION .

# 5. 애플리케이션 파일 복사
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# 6. 포트 노출
EXPOSE 5000

# 7. 실행 명령
CMD ["python", "app.py"]
```

**중요 포인트:**

1. **레이어 캐싱 최적화**
   - 자주 변경되지 않는 파일부터 복사 (의존성)
   - 자주 변경되는 파일은 나중에 복사 (앱 코드)

2. **보안**
   - `--no-cache-dir`: 패키지 캐시 저장 안 함 (이미지 크기 감소)
   - `python:3.9-slim`: 최소 이미지 사용

### deploy.cmd (배포 스크립트)

**핵심 로직:**

```batch
@echo off
setlocal enabledelayedexpansion

:: 1. 설정 파일 로드
for /f "usebackq tokens=1,* delims==" %%a in ("deploy.config") do (
    set "%%a=%%b"
)

:: 2. 현재 버전 읽기
set /p CURRENT_VERSION=<VERSION

:: 3. 버전 파싱
for /f "tokens=1,2,3 delims=." %%a in ("!CURRENT_VERSION!") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "HOTFIX=%%c"
)

:: 4. 버전 증가
if /i "%1"=="major" (
    set /a MAJOR+=1
    set "MINOR=0"
    set "HOTFIX=0"
) else if /i "%1"=="minor" (
    set /a MINOR+=1
    set "HOTFIX=0"
) else if /i "%1"=="hotfix" (
    set /a HOTFIX+=1
)

:: 5. 새 버전 저장
set "NEW_VERSION=!MAJOR!.!MINOR!.!HOTFIX!"
echo !NEW_VERSION! > VERSION

:: 6. 이미지 태그 생성
if not "%DEPLOYER%"=="" (
    set "IMAGE_TAG=%DEPLOYER%/%IMAGE_NAME%"
) else (
    set "IMAGE_TAG=%IMAGE_NAME%"
)

:: 7. Docker 빌드
docker build -t !IMAGE_TAG!:!NEW_VERSION! -t !IMAGE_TAG!:latest .

:: 8. Docker Hub 푸시 (옵션)
if /i "%PUSH_TO_REGISTRY%"=="true" (
    docker push !IMAGE_TAG!:!NEW_VERSION!
    docker push !IMAGE_TAG!:latest
)

:: 9. 컨테이너 재시작
docker stop %CONTAINER_NAME%
docker rm %CONTAINER_NAME%
docker run -d -p %HOST_PORT%:%CONTAINER_PORT% --name %CONTAINER_NAME% !IMAGE_TAG!:!NEW_VERSION!

endlocal
```

### VERSION 파일

**형식:**

```
2.1.0
```

**중요:**
- 단일 라인
- 공백 없음
- 형식: `MAJOR.MINOR.HOTFIX`
- 항상 3개의 숫자

---

## 🚀 배포 시스템

### 배포 워크플로우

```
1. 개발자 코드 수정
   └─> app.py, templates/, static/ 등

2. 버전 타입 결정
   ├─> Hotfix: 버그 수정
   ├─> Minor: 새 기능
   └─> Major: API 변경

3. deploy.cmd 실행
   └─> deploy.cmd [major|minor|hotfix]

4. 자동 프로세스 실행
   ├─> VERSION 파일 업데이트
   ├─> Docker 이미지 빌드
   ├─> Docker Hub 푸시 (선택)
   ├─> 기존 컨테이너 중지
   └─> 새 컨테이너 시작

5. 배포 완료
   └─> http://localhost:5000 접속
```

### 설정 관리

```
초기 설정 (1회)
├─> copy deploy.config.example deploy.config
└─> deploy.config 편집 (본인 정보 입력)

Git 커밋
├─> deploy.config.example (O) - 공유
└─> deploy.config (X) - 개인 설정
```

### 버전 전략

| 변경 유형 | 명령어 | 예시 | 사용 시기 |
|----------|--------|------|----------|
| **Hotfix** | `deploy.cmd hotfix` | 2.1.0 → 2.1.1 | 버그 수정, 패치 |
| **Minor** | `deploy.cmd minor` | 2.1.0 → 2.2.0 | 새 기능, 개선 |
| **Major** | `deploy.cmd major` | 2.1.0 → 3.0.0 | API 변경, 대규모 수정 |

---

## 🆕 새 프로젝트 적용 가이드

### Step 1: 프로젝트 구조 생성

```bash
mkdir my_new_project
cd my_new_project

# 디렉토리 생성
mkdir templates
mkdir static
mkdir static/css
mkdir static/js
```

### Step 2: 필수 파일 복사

이 템플릿에서 다음 파일들을 복사:

```
✅ deploy.config.example
✅ deploy.cmd
✅ version.cmd
✅ .gitignore
✅ Dockerfile
✅ TEMPLATE_GUIDE.md (이 문서)
```

### Step 3: VERSION 파일 생성

```bash
echo 1.0.0 > VERSION
```

### Step 4: Flask 앱 생성

```python
# app.py
from flask import Flask, render_template
import os

app = Flask(__name__)

def get_version():
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return '1.0.0'

APP_VERSION = get_version()

@app.route('/')
def index():
    return render_template('index.html', version=APP_VERSION)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 5: HTML 템플릿 생성

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>내 프로젝트 v{{ version }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>내 프로젝트</h1>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```

### Step 6: CSS/JS 파일 생성

```css
/* static/css/style.css */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}
```

```javascript
// static/js/script.js
console.log('App loaded');
```

### Step 7: 배포 설정

```bash
# deploy.config 생성
copy deploy.config.example deploy.config

# deploy.config 편집
notepad deploy.config
```

```ini
DEPLOYER=your-username
IMAGE_NAME=my-new-project
CONTAINER_NAME=my-new-project
HOST_PORT=5000
CONTAINER_PORT=5000
PUSH_TO_REGISTRY=false
REGISTRY=
```

### Step 8: Dockerfile 수정

```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY VERSION .
COPY app.py .
COPY templates/ templates/
COPY static/ static/
EXPOSE 5000
CMD ["python", "app.py"]
```

### Step 9: 첫 배포

```cmd
# 버전 확인
version.cmd

# 배포
deploy.cmd hotfix

# 접속 테스트
# http://localhost:5000
```

---

## 🤖 AI 어시스턴트를 위한 가이드

### AI가 이 템플릿을 이해하는 방법

#### 1. 구조 인식

AI가 프로젝트를 분석할 때 확인해야 할 사항:

```python
# 체크리스트
✅ templates/ 디렉토리 존재?
✅ static/css/ 디렉토리 존재?
✅ static/js/ 디렉토리 존재?
✅ deploy.config.example 파일 존재?
✅ VERSION 파일 존재?
✅ deploy.cmd 파일 존재?
```

#### 2. 파일 수정 시 원칙

**HTML 수정 요청 시:**
```python
# templates/index.html 수정
# ❌ app.py에 HTML 문자열 추가하지 않음
# ✅ templates/index.html 파일 직접 수정
```

**CSS 수정 요청 시:**
```python
# static/css/style.css 수정
# ❌ index.html에 <style> 태그 추가하지 않음
# ✅ style.css 파일 직접 수정
```

**JavaScript 수정 요청 시:**
```python
# static/js/script.js 수정
# ❌ index.html에 <script> 태그 내 코드 추가하지 않음
# ✅ script.js 파일 직접 수정
```

#### 3. 새 기능 추가 시 프로세스

```python
def add_new_feature_process():
    """
    AI가 새 기능을 추가할 때 따라야 할 프로세스
    """
    steps = [
        "1. app.py에 라우트 추가",
        "2. templates/에 새 HTML 파일 생성 (필요시)",
        "3. static/css/style.css에 스타일 추가",
        "4. static/js/script.js에 로직 추가",
        "5. Dockerfile 확인 (새 의존성 필요 시 수정)",
        "6. README.md 업데이트 (새 기능 설명)",
        "7. 사용자에게 deploy.cmd minor 실행 안내"
    ]
    return steps
```

#### 4. 배포 관련 질문 대응

사용자가 다음과 같이 질문하면:

**"배포하고 싶어"**
```
1. 변경 내용 확인
2. 버전 타입 제안:
   - 버그 수정 → "deploy.cmd hotfix 실행하세요"
   - 새 기능 → "deploy.cmd minor 실행하세요"
   - 대규모 변경 → "deploy.cmd major 실행하세요"
```

**"버전을 올리고 싶어"**
```
1. "version.cmd로 현재 버전 확인하세요"
2. "deploy.cmd [타입] 실행하세요"
3. 자동으로 VERSION 파일 업데이트됨을 안내
```

**"Docker 이미지 이름 바꾸고 싶어"**
```
1. "deploy.config 파일 수정하세요"
2. IMAGE_NAME=새이름
3. "deploy.cmd 다시 실행하면 새 이름으로 빌드됩니다"
```

#### 5. 트러블슈팅 가이드

| 문제 | 진단 | 해결 |
|------|------|------|
| **CSS/JS가 적용 안 됨** | `url_for()` 확인 | `{{ url_for('static', filename='css/style.css') }}` 형식 확인 |
| **버전이 표시 안 됨** | `get_version()` 확인 | VERSION 파일 존재 확인, `app.py`에 `get_version()` 함수 있는지 확인 |
| **deploy.cmd 실패** | `deploy.config` 확인 | 파일 존재 여부, 형식 확인 |
| **Docker 빌드 실패** | `Dockerfile` 확인 | COPY 경로가 올바른지 확인 |
| **포트 충돌** | `deploy.config` 확인 | HOST_PORT 변경 (예: 5000 → 5001) |

#### 6. 코드 생성 템플릿

AI가 새 파일을 생성할 때 사용할 템플릿:

**새 Flask 라우트:**
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html', version=APP_VERSION)
```

**새 HTML 페이지:**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>페이지 제목 v{{ version }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- 내용 -->
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```

#### 7. 반드시 지켜야 할 규칙

```python
MUST_FOLLOW_RULES = {
    "separation": {
        "HTML": "templates/ 폴더에만",
        "CSS": "static/css/ 폴더에만",
        "JS": "static/js/ 폴더에만",
        "Python": "app.py 또는 별도 .py 파일에만"
    },
    "configuration": {
        "deploy_settings": "deploy.config에만 (코드에 하드코딩 금지)",
        "version": "VERSION 파일에만 (코드에 하드코딩 금지)"
    },
    "versioning": {
        "format": "MAJOR.MINOR.HOTFIX (예: 2.1.0)",
        "update": "deploy.cmd 사용 (수동 수정 금지)"
    },
    "docker": {
        "naming": "deploy.config의 IMAGE_NAME 사용",
        "tagging": "버전 태그 + latest 태그 모두 생성"
    }
}
```

---

## 📚 참고 자료

### 관련 문서

- **README.md**: 프로젝트 사용자 가이드
- **DEPLOY_GUIDE.md**: 상세 배포 매뉴얼
- **TEMPLATE_GUIDE.md**: 이 문서 (템플릿 가이드)

### 외부 참조

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [Semantic Versioning](https://semver.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask 프로젝트 구조](https://flask.palletsprojects.com/en/2.3.x/tutorial/layout/)

---

## 🎓 학습 경로

### 초급: 템플릿 사용하기

1. 이 프로젝트를 복제
2. `deploy.config` 설정
3. `deploy.cmd hotfix` 실행
4. HTML/CSS/JS 수정 연습

### 중급: 템플릿 커스터마이징

1. 새 라우트 추가
2. 새 페이지 생성
3. API 엔드포인트 추가
4. 데이터베이스 연결

### 고급: 템플릿 확장

1. 다른 Python 프레임워크 적용 (Django, FastAPI)
2. CI/CD 파이프라인 통합
3. 다중 환경 지원 (dev, staging, prod)
4. Kubernetes 배포 추가

---

## ✅ 체크리스트

### 새 프로젝트 시작 전

- [ ] Python 3.9+ 설치됨
- [ ] Docker Desktop 설치됨
- [ ] Git 설치됨
- [ ] 텍스트 에디터 준비됨

### 프로젝트 생성 후

- [ ] 디렉토리 구조 생성 완료
- [ ] 필수 파일 복사 완료
- [ ] `deploy.config` 생성 및 설정 완료
- [ ] `VERSION` 파일 생성 완료
- [ ] `app.py` 작성 완료
- [ ] `templates/index.html` 작성 완료
- [ ] `static/css/style.css` 작성 완료
- [ ] `static/js/script.js` 작성 완료
- [ ] `Dockerfile` 작성 완료

### 첫 배포 전

- [ ] `version.cmd` 실행하여 버전 확인
- [ ] Docker Desktop 실행 중
- [ ] 포트 5000 사용 가능한지 확인
- [ ] `deploy.cmd hotfix` 실행 준비

### 배포 후

- [ ] http://localhost:5000 접속 확인
- [ ] 기능 테스트 완료
- [ ] Git 커밋 (deploy.config 제외)
- [ ] README.md 업데이트

---

## 🚨 주의사항

### 하지 말아야 할 것

1. ❌ `deploy.config`를 Git에 커밋하지 마세요
2. ❌ HTML에 인라인 CSS/JS를 추가하지 마세요
3. ❌ VERSION 파일을 수동으로 수정하지 마세요
4. ❌ 코드에 포트/이미지 이름을 하드코딩하지 마세요
5. ❌ `deploy.cmd`를 수정 없이 사용하세요 (버그 수정 제외)

### 해야 할 것

1. ✅ `deploy.config.example`을 항상 최신으로 유지하세요
2. ✅ 파일을 올바른 디렉토리에 배치하세요
3. ✅ Semantic Versioning 규칙을 따르세요
4. ✅ 배포 전 로컬 테스트를 하세요
5. ✅ 변경사항을 문서화하세요

---

## 🙏 마치며

이 템플릿은 Flask 프로젝트의 **표준화**, **자동화**, **관리 편의성**을 목표로 설계되었습니다.

### 핵심 가치

1. **일관성**: 모든 Flask 프로젝트가 동일한 구조 사용
2. **효율성**: 배포 자동화로 시간 절약
3. **확장성**: 쉽게 기능 추가 가능
4. **협업**: 명확한 규칙으로 팀 작업 용이

### 다음 단계

- 이 템플릿을 본인의 프로젝트에 적용해보세요
- 개선 사항이 있다면 공유해주세요
- 다른 팀과 이 구조를 공유해보세요

---

**작성일**: 2024-10-16  
**버전**: 1.0.0  
**작성자**: AI Assistant (Claude)  
**목적**: Flask 프로젝트 템플릿 표준화

---

## 📞 지원

이 템플릿에 대한 질문이나 개선 제안은 이슈로 등록해주세요.

**Happy Coding! 🎉**


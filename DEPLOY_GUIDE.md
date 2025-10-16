# 🚀 배포 가이드

## 📋 목차
1. [첫 설정: 배포 구성](#첫-설정-배포-구성)
2. [버전 관리 전략](#버전-관리-전략)
3. [배포 프로세스](#배포-프로세스)
4. [사용 예시](#사용-예시)
5. [트러블슈팅](#트러블슈팅)

## ⚙️ 첫 설정: 배포 구성

### 1. deploy.config 파일 생성

배포 스크립트를 처음 사용하려면 먼저 배포 설정 파일을 만들어야 합니다:

```cmd
# 예제 파일을 복사
copy deploy.config.example deploy.config
```

### 2. 본인의 정보로 수정

`deploy.config` 파일을 편집기로 열어 본인의 정보를 입력하세요:

```ini
# VCF to CSV Converter - Deploy Configuration

# 배포 주체 (Docker Hub 사용자명)
DEPLOYER=jslee7518

# Docker 이미지 이름 (소문자 권장)
IMAGE_NAME=vcftocsv

# 컨테이너 이름
CONTAINER_NAME=vcftocsv

# 포트 설정 (호스트:컨테이너)
HOST_PORT=5000
CONTAINER_PORT=5000

# Docker Hub에 푸시할지 여부 (true/false)
PUSH_TO_REGISTRY=false

# Docker Hub 레지스트리 (비어있으면 Docker Hub 기본)
REGISTRY=
```

### 3. 설정 설명

| 설정 항목 | 설명 | 예시 |
|----------|------|------|
| **DEPLOYER** | Docker Hub 사용자명 또는 조직명 | `jslee7518` |
| **IMAGE_NAME** | Docker 이미지 이름 (소문자 권장) | `vcftocsv` |
| **CONTAINER_NAME** | 실행될 컨테이너 이름 | `vcftocsv` |
| **HOST_PORT** | 호스트에서 접근할 포트 | `5000` |
| **CONTAINER_PORT** | 컨테이너 내부 포트 | `5000` |
| **PUSH_TO_REGISTRY** | 빌드 후 Docker Hub 자동 푸시 | `false` / `true` |
| **REGISTRY** | 사설 레지스트리 URL (선택사항) | 비워두면 Docker Hub |

### 4. 이미지 태그 형식

설정에 따라 이미지 태그가 다르게 생성됩니다:

```
# DEPLOYER가 설정된 경우
jslee7518/vcftocsv:2.1.0
jslee7518/vcftocsv:latest

# DEPLOYER가 비어있는 경우
vcftocsv:2.1.0
vcftocsv:latest
```

### 5. Docker Hub 푸시 설정 (선택)

Docker Hub에 자동으로 푸시하려면:

```cmd
# 1. Docker Hub 로그인 (최초 1회)
docker login

# 2. deploy.config 수정
PUSH_TO_REGISTRY=true

# 3. 이제 deploy.cmd 실행 시 자동으로 푸시됩니다
deploy.cmd hotfix
```

> **참고:** `deploy.config` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다. 개인 설정이므로 각자 관리하세요.

## 📌 버전 관리 전략

### Semantic Versioning (v{MAJOR}.{MINOR}.{HOTFIX})

- **MAJOR (1.x.x → 2.x.x)**: 대규모 변경사항
  - API 호환성이 깨지는 변경
  - 완전히 새로운 기능 추가
  - 아키텍처 변경
  
- **MINOR (x.1.x → x.2.x)**: 중간 규모 변경사항
  - 새로운 기능 추가
  - 하위 호환성 유지
  - 성능 개선
  
- **HOTFIX (x.x.1 → x.x.2)**: 작은 수정사항
  - 버그 수정
  - 패치
  - 문서 수정

## 🔄 배포 프로세스

### 1. 현재 버전 확인
```cmd
version.cmd
```

출력 예시:
```
========================================
Current Version Information
========================================

Application Version: v2.1.0

Configuration:
----------------------------------------
Deployer       : jslee7518
Image Name     : vcftocsv
Container Name : vcftocsv
Port Mapping   : 5000:5000

Docker Images:
----------------------------------------
TAG       CREATED AT                      SIZE
2.1.0     2025-10-16 10:19:59 +0900 KST   221MB
latest    2025-10-16 10:19:59 +0900 KST   221MB
```

### 2. 버전 선택 및 배포

#### Hotfix 배포 (v2.0.0 → v2.0.1)
작은 버그 수정이나 패치를 배포할 때:
```cmd
deploy.cmd hotfix
```

#### Minor 배포 (v2.0.0 → v2.1.0)
새로운 기능을 추가할 때:
```cmd
deploy.cmd minor
```

#### Major 배포 (v2.0.0 → v3.0.0)
대규모 변경사항이 있을 때:
```cmd
deploy.cmd major
```

### 3. 배포 과정 (자동)

스크립트가 자동으로 다음 작업을 수행합니다:

```
1. 배포 설정 읽기 ✅
   └─> deploy.config 파일에서 설정 로드
   └─> DEPLOYER, IMAGE_NAME, PORT 등 확인

2. 현재 버전 읽기 ✅
   └─> VERSION 파일에서 v2.0.0 확인

3. 버전 증가 ✅
   └─> v2.0.0 → v2.1.0 (minor 예시)

4. VERSION 파일 업데이트 ✅
   └─> 2.1.0 저장

5. Docker 이미지 빌드 ✅
   ├─> jslee7518/vcftocsv:2.1.0
   └─> jslee7518/vcftocsv:latest

6. Docker Hub 푸시 (PUSH_TO_REGISTRY=true인 경우) ✅
   ├─> jslee7518/vcftocsv:2.1.0 푸시
   └─> jslee7518/vcftocsv:latest 푸시

7. 기존 컨테이너 중지 및 제거 ✅
   └─> vcftocsv 컨테이너 종료 및 제거

8. 새 컨테이너 시작 ✅
   └─> v2.1.0 컨테이너 실행 (설정된 포트로)

9. 완료! 🎉
   └─> http://localhost:5000 접속 가능
```

## 💡 사용 예시

### 예시 1: 버그 수정 배포

문제 발견:
```
❌ 전화번호 포맷팅 버그 발견
```

수정 후 배포:
```cmd
# 1. 코드 수정 완료

# 2. Hotfix 배포
deploy.cmd hotfix

# 결과: v2.0.0 → v2.0.1
```

### 예시 2: 새 기능 추가

새 기능 개발:
```
✨ 커스텀 구분자 기능 추가
```

배포:
```cmd
# 1. 기능 개발 완료

# 2. Minor 버전 배포
deploy.cmd minor

# 결과: v2.0.1 → v2.1.0
```

### 예시 3: 대규모 업데이트

주요 변경사항:
```
🔥 전면 리뉴얼
   - UI 완전 변경
   - API 구조 변경
   - 새로운 인코딩 방식 지원
```

배포:
```cmd
# 1. 모든 변경사항 완료

# 2. Major 버전 배포
deploy.cmd major

# 결과: v2.1.0 → v3.0.0
```

## 🔍 트러블슈팅

### 문제 1: 포트 충돌
```
Error: Port 5000 is already in use
```

**해결책:**
```cmd
# 기존 컨테이너 확인
docker ps

# 수동으로 중지
docker stop vcf-web-converter
docker rm vcf-web-converter

# 다시 배포
deploy.cmd hotfix
```

### 문제 2: Docker 빌드 실패
```
Error: Failed to build Docker image
```

**해결책:**
```cmd
# Docker가 실행 중인지 확인
docker ps

# Dockerfile 문법 확인
# 수동 빌드로 에러 확인
docker build -t test .

# 문제 해결 후 다시 배포
```

### 문제 3: VERSION 파일 손상
```
Error: Invalid version format
```

**해결책:**
```cmd
# VERSION 파일 확인
type VERSION

# 올바른 형식으로 수정 (예: 2.0.0)
echo 2.0.0 > VERSION

# 다시 배포
deploy.cmd hotfix
```

## 📊 버전 히스토리 관리

### 태그된 이미지 확인
```cmd
docker images vcf-web-converter
```

### 특정 버전 실행
```cmd
# v2.0.0 실행
docker run -d -p 5000:5000 --name vcf-v2 vcf-web-converter:2.0.0

# v2.1.0 실행 (다른 포트)
docker run -d -p 5001:5000 --name vcf-v2.1 vcf-web-converter:2.1.0
```

### 롤백 (이전 버전으로 되돌리기)
```cmd
# 1. 현재 컨테이너 중지
docker stop vcf-web-converter
docker rm vcf-web-converter

# 2. 이전 버전 실행
docker run -d -p 5000:5000 --name vcf-web-converter vcf-web-converter:2.0.0

# 3. VERSION 파일도 되돌리기
echo 2.0.0 > VERSION
```

## 🎯 베스트 프랙티스

### 1. 배포 전 체크리스트
- [ ] 코드 변경사항 확인
- [ ] 로컬 테스트 완료
- [ ] VERSION 파일 확인
- [ ] 올바른 버전 타입 선택 (major/minor/hotfix)

### 2. 배포 후 확인사항
- [ ] 웹 페이지 정상 접속 (http://localhost:5000)
- [ ] 버전 번호 확인 (페이지 상단)
- [ ] 주요 기능 동작 확인
- [ ] Docker 컨테이너 상태 확인 (`docker ps`)

### 3. 정기 점검
```cmd
# 주간 점검 루틴
version.cmd                        # 현재 버전 확인
docker ps                          # 컨테이너 상태
docker logs vcf-web-converter      # 로그 확인
docker system df                   # 디스크 사용량
```

## 📝 체인지로그 작성 (권장)

`CHANGELOG.md` 파일 생성 예시:

```markdown
# Changelog

## [2.1.0] - 2025-10-16
### Added
- 전화번호 포맷 선택 기능
- 커스텀 구분자 입력
- 실시간 미리보기

### Changed
- UI 개선

## [2.0.1] - 2025-10-15
### Fixed
- 한글 인코딩 버그 수정
```

---

## 🤝 도움이 필요하신가요?

문제가 발생하면:
1. Docker 로그 확인: `docker logs vcf-web-converter`
2. VERSION 파일 확인: `type VERSION`
3. Docker 상태 확인: `docker ps -a`


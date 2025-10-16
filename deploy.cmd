@echo off
setlocal enabledelayedexpansion

:: 스크립트가 있는 디렉토리로 이동
cd /d "%~dp0"

:: deploy.config 파일 읽기
if not exist deploy.config (
    echo ERROR: deploy.config file not found!
    echo Please create deploy.config file with deployment settings.
    exit /b 1
)

echo Loading deployment configuration...
for /f "usebackq tokens=1,* delims==" %%a in ("deploy.config") do (
    set "line=%%a"
    :: 주석(#) 또는 빈 줄 무시
    if not "!line:~0,1!"=="#" (
        if not "%%a"=="" (
            if not "%%b"=="" (
                set "%%a=%%b"
            )
        )
    )
)

echo.
echo ========================================
echo Deployment Configuration
echo ========================================
echo Deployer     : %DEPLOYER%
echo Image Name   : %IMAGE_NAME%
echo Container    : %CONTAINER_NAME%
echo Port Mapping : %HOST_PORT%:%CONTAINER_PORT%
echo Push Registry: %PUSH_TO_REGISTRY%
echo ========================================
echo.

:: 사용법 체크
if "%~1"=="" (
    echo Usage: deploy.cmd [major^|minor^|hotfix]
    echo.
    echo Examples:
    echo   deploy.cmd major   - v1.0.0 -^> v2.0.0
    echo   deploy.cmd minor   - v1.0.0 -^> v1.1.0
    echo   deploy.cmd hotfix  - v1.0.0 -^> v1.0.1
    exit /b 1
)

set "VERSION_TYPE=%~1"

:: VERSION 파일에서 현재 버전 읽기
if not exist VERSION (
    echo 1.0.0 > VERSION
    echo Created VERSION file with 1.0.0
)

set /p CURRENT_VERSION=<VERSION
echo Current version: v!CURRENT_VERSION!

:: 버전 파싱 (major.minor.hotfix)
for /f "tokens=1,2,3 delims=." %%a in ("!CURRENT_VERSION!") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "HOTFIX=%%c"
)

:: 버전 증가
if /i "!VERSION_TYPE!"=="major" (
    set /a MAJOR+=1
    set "MINOR=0"
    set "HOTFIX=0"
    echo Bumping MAJOR version...
) else if /i "!VERSION_TYPE!"=="minor" (
    set /a MINOR+=1
    set "HOTFIX=0"
    echo Bumping MINOR version...
) else if /i "!VERSION_TYPE!"=="hotfix" (
    set /a HOTFIX+=1
    echo Bumping HOTFIX version...
) else (
    echo Invalid version type: !VERSION_TYPE!
    echo Use: major, minor, or hotfix
    exit /b 1
)

:: 새 버전 생성
set "NEW_VERSION=!MAJOR!.!MINOR!.!HOTFIX!"
echo New version: v!NEW_VERSION!
echo.

:: VERSION 파일 업데이트
echo !NEW_VERSION! > VERSION
echo Updated VERSION file

:: 이미지 태그 생성 (DEPLOYER가 있으면 포함)
if not "%DEPLOYER%"=="" (
    set "IMAGE_TAG=%DEPLOYER%/%IMAGE_NAME%"
) else (
    set "IMAGE_TAG=%IMAGE_NAME%"
)

:: Docker 이미지 빌드
echo.
echo ========================================
echo Building Docker image...
echo ========================================
docker build -t !IMAGE_TAG!:!NEW_VERSION! -t !IMAGE_TAG!:latest .
if errorlevel 1 (
    echo Failed to build Docker image
    exit /b 1
)

echo.
echo ========================================
echo Build successful!
echo ========================================
echo.
echo Image tags:
echo   - !IMAGE_TAG!:!NEW_VERSION!
echo   - !IMAGE_TAG!:latest
echo.

:: Docker Hub에 푸시 (설정에서 활성화된 경우)
if /i "%PUSH_TO_REGISTRY%"=="true" (
    echo ========================================
    echo Pushing to Docker Hub...
    echo ========================================
    docker push !IMAGE_TAG!:!NEW_VERSION!
    docker push !IMAGE_TAG!:latest
    if errorlevel 1 (
        echo Warning: Failed to push to registry
    ) else (
        echo Successfully pushed to Docker Hub!
    )
    echo.
)

:: 기존 컨테이너 중지 및 제거
echo Stopping existing containers...
for /f "tokens=*" %%i in ('docker ps -aq --filter "name=%CONTAINER_NAME%"') do (
    echo Stopping container: %%i
    docker stop %%i
    docker rm %%i
)

:: 새 컨테이너 실행
echo.
echo ========================================
echo Starting container...
echo ========================================
docker run -d -p %HOST_PORT%:%CONTAINER_PORT% --name %CONTAINER_NAME% !IMAGE_TAG!:!NEW_VERSION!
if errorlevel 1 (
    echo Failed to start container
    exit /b 1
)

echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo.
echo Deployer    : %DEPLOYER%
echo Version     : v!NEW_VERSION!
echo Image       : !IMAGE_TAG!:!NEW_VERSION!
echo Container   : %CONTAINER_NAME%
echo URL         : http://localhost:%HOST_PORT%
echo.
echo Useful commands:
echo   docker logs %CONTAINER_NAME%          - View logs
echo   docker stop %CONTAINER_NAME%          - Stop container
echo   docker start %CONTAINER_NAME%         - Start container
echo   docker ps                             - List running containers
echo.

endlocal
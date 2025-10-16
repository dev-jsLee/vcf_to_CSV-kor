@echo off
setlocal enabledelayedexpansion

:: 스크립트가 있는 디렉토리로 이동
cd /d "%~dp0"

:: deploy.config 파일 읽기
if exist deploy.config (
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
)

echo ========================================
echo Current Version Information
echo ========================================
echo.

if not exist VERSION (
    echo VERSION file not found
    exit /b 1
)

set /p CURRENT_VERSION=<VERSION
echo Application Version: v%CURRENT_VERSION%
echo.
echo Configuration:
echo ----------------------------------------
echo Deployer       : %DEPLOYER%
echo Image Name     : %IMAGE_NAME%
echo Container Name : %CONTAINER_NAME%
echo Port Mapping   : %HOST_PORT%:%CONTAINER_PORT%

:: 이미지 태그 생성
if not "%DEPLOYER%"=="" (
    set "IMAGE_TAG=%DEPLOYER%/%IMAGE_NAME%"
) else (
    set "IMAGE_TAG=%IMAGE_NAME%"
)

echo.
echo Docker Images:
echo ----------------------------------------
docker images !IMAGE_TAG! --format "table {{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"

endlocal


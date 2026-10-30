
@echo off
setlocal

cd /d "%~dp0.."

if "%~1"=="" (
    echo Usage: deploy.bat v1.0.0
    exit /b 1
)

set "APP_IMAGE=apex-operations-api:%~1"

echo Checking image: %APP_IMAGE%

docker image inspect "%APP_IMAGE%" >nul 2>&1

if errorlevel 1 (
    echo ERROR: Docker image does not exist.
    exit /b 1
)

echo Deploying %APP_IMAGE%...

docker compose up -d --no-build

if errorlevel 1 (
    echo Deployment failed.
    exit /b 1
)

echo Deployment command completed.
docker compose ps

endlocal

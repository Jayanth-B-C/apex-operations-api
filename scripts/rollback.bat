
@echo off

if "%~1"=="" (
    echo Usage: rollback.bat v1.0.0
    exit /b 1
)

echo Rolling back to %~1...

call "%~dp0deploy.bat" %~1

if errorlevel 1 (
    echo Rollback failed.
    exit /b 1
)

echo Rollback deployment completed.

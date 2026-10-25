@echo off
title Tool Chat Go SVIP (1280x720)
cd /d "%~dp0"

if exist "GoSVIPver2.exe" (
    echo Dang khoi chay GoSVIPver2.exe...
    start "" "GoSVIPver2.exe"
    exit
)

echo Dang kiem tra va khoi chay Tool bang Python...
python j4flzchatgo.py
if %errorlevel% neq 0 (
    echo.
    echo ======================================================
    echo Neu thieu thu vien, dang tu dong cai dat thu vien...
    pip install -r requirements.txt
    echo Dang chay lai tool...
    python j4flzchatgo.py
    echo ======================================================
)
pause

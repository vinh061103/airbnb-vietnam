@echo off
title Day Code Len GitHub (Push to GitHub)
echo ===================================================================
echo              DANG DAY TOAN BO DU AN LEN GITHUB
echo ===================================================================
echo Repository: https://github.com/vinh061103/airbnb-vietnam.git
echo.
cd /d "%~dp0"

git branch -M main
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ===================================================================
    echo   CHUC MUNG! CODE DA DUOC DAY LEN GITHUB THANH CONG!
    echo ===================================================================
    echo Bay gio ban co the vao Render.com de ket noi Web Service.
) else (
    echo ===================================================================
    echo LUU Y: Neu GitHub yeu cau xac thuc, trinh duyet se mo ra mot tab
    echo de ban bam "Sign in with your browser" hoac nhap Token cua GitHub.
    echo ===================================================================
)

echo.
pause

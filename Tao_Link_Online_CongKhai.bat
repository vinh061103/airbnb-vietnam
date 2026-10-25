@echo off
title Tao Link Online Cong Khai (Public Live URL)
echo ===================================================================
echo     DANG KHOI TAO DUONG LINK ONLINE CONG KHAI TRUY CAP INTERNET
echo ===================================================================
echo.
cd /d "%~dp0server"

echo Dang ket noi mang de cap duong link HTTPS...
node start_tunnel.js
pause

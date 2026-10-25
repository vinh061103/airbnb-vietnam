@echo off
title Khoi dong Website Dat Phong Airbnb (Fullstack + SQLite Database)
echo ===================================================================
echo     DANG KHOI DONG BACKEND REST API (SQLITE DATABASE) VA FRONTEND
echo ===================================================================
echo.
cd /d "%~dp0"

echo [1/2] Dang khoi dong Backend API & SQLite Database tren cong 5000...
start "Backend SQLite Server (Port 5000)" cmd /k "cd server && node server.js"

timeout /t 2 /nobreak >nul

echo [2/2] Dang khoi dong Frontend React tren http://127.0.0.1:5173/ ...
start http://127.0.0.1:5173/
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
pause

@echo off
title AffetX Voice AI Live Companion
echo Starting AffetX Frontend on Local Server (Microphone Enabled)...
start http://localhost:8000/index.html
python -m http.server 8000 --directory frontend
pause

@echo off
title AffetX - GitHub Uploader
echo ===================================================
echo   Uploading Full Project (including frontend) to GitHub...
echo ===================================================

git init
git add .
git commit -m "Upload AffetX frontend and companion codebase"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/N3Edirisinghe/fyp-demo.git
git push -u origin main --force

echo.
echo ===================================================
echo   Upload complete! You can now deploy on Streamlit.
echo ===================================================
pause

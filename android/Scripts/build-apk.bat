@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-apk.ps1" Debug

if errorlevel 1 (
    echo.
    echo Build failed. If this machine has no Android Gradle environment, use GitHub Actions to build APK.
    pause
    exit /b 1
)

echo.
echo APK generated in dist\MyGames-android-debug.apk
pause

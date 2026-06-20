@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%venv"

where python >nul 2>nul
if errorlevel 1 (
    echo Python introuvable. Installe Python 3.10+ avant de continuer.
    exit /b 1
)

if not exist "%VENV_DIR%" (
    echo Creation du venv...
    python -m venv "%VENV_DIR%"
)

echo Installation des dependances...
"%VENV_DIR%\Scripts\pip.exe" install -q -r "%ROOT_DIR%requirements.txt"
if errorlevel 1 exit /b 1

if not exist "%ROOT_DIR%workspace" mkdir "%ROOT_DIR%workspace"
type nul > "%ROOT_DIR%workspace\.gitkeep"

echo Migrations internes...
"%VENV_DIR%\Scripts\python.exe" "%ROOT_DIR%lab\manage.py" migrate --noinput
if errorlevel 1 exit /b 1

echo.
echo C'est pret — ouvre http://localhost:8000
echo.
"%VENV_DIR%\Scripts\python.exe" "%ROOT_DIR%lab\manage.py" runserver 8000

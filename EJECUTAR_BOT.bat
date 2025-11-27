@echo off
title BOT RPA CLARO
color 0B
cls

:: Verificar que Python esta disponible
set PYTHON_FOUND=0

python --version >nul 2>&1
if %errorlevel% equ 0 set PYTHON_FOUND=1

py --version >nul 2>&1
if %errorlevel% equ 0 set PYTHON_FOUND=1

python3 --version >nul 2>&1
if %errorlevel% equ 0 set PYTHON_FOUND=1

if %PYTHON_FOUND% equ 0 (
    echo ============================================================
    echo    ERROR: Python no instalado
    echo ============================================================
    echo.
    echo [!] Python no esta instalado o no esta en el PATH
    echo [!] Por favor ejecuta "INSTALAR.bat" primero
    echo.
    pause
    exit /b 1
)

:: Activar entorno virtual
if not exist ".venv" (
    echo ============================================================
    echo    ERROR: Entorno no configurado
    echo ============================================================
    echo.
    echo [!] El entorno virtual no existe
    echo [!] Por favor ejecuta "INSTALAR.bat" primero
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\activate.bat" (
    echo ============================================================
    echo    ERROR: Entorno virtual corrupto
    echo ============================================================
    echo.
    echo [!] El entorno virtual esta danado
    echo [!] Por favor ejecuta "INSTALAR.bat" nuevamente
    echo.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

:MENU
cls
echo ============================================================
echo    BOT RPA - DESCARGA AUTOMATICA DE DIAGRAMAS CLARO
echo ============================================================
echo.
echo Selecciona una opcion:
echo.
echo   [1] Interfaz Grafica (Recomendado)
echo   [2] Modo Consola
echo   [3] Salir
echo.
echo ------------------------------------------------------------
set /p opcion="Opcion: "

if "%opcion%"=="1" goto GUI
if "%opcion%"=="2" goto CONSOLA
if "%opcion%"=="3" goto SALIR

echo.
echo Opcion invalida. Intenta de nuevo.
timeout /t 2 >nul
goto MENU

:GUI
cls
echo ============================================================
echo    ABRIENDO INTERFAZ GRAFICA...
echo ============================================================
echo.
python gui.py
goto MENU

:CONSOLA
cls
echo ============================================================
echo    EJECUTANDO BOT EN MODO CONSOLA
echo ============================================================
echo.
python index.py
echo.
echo ============================================================
echo    PROCESO FINALIZADO
echo ============================================================
echo.
pause
goto MENU

:SALIR
cls
echo.
echo Hasta pronto!
timeout /t 1 >nul
exit /b 0

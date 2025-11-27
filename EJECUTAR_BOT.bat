@echo off
title BOT RPA CLARO - INICIO INTELIGENTE
color 0B
cls

:: ===========================================================
:: PASO 1: DETECTAR LA UBICACION DEL BOT
:: ===========================================================

:: Si este .bat esta en el escritorio, buscar la carpeta del bot
set "BOT_DIR=%~dp0"

:: Si hay un archivo de configuracion que indica donde esta el bot, usarlo
if exist "%USERPROFILE%\.bot-rpa-location.txt" (
    set /p BOT_DIR=<"%USERPROFILE%\.bot-rpa-location.txt"
    if exist "!BOT_DIR!\gui.py" (
        cd /d "!BOT_DIR!"
    )
)

:: Verificar si estamos en la carpeta correcta del bot
if not exist "gui.py" (
    if not exist "index.py" (
        echo ============================================================
        echo    ERROR: No se encuentra el bot
        echo ============================================================
        echo.
        echo [!] Este script no puede encontrar los archivos del bot
        echo.
        echo SOLUCIONES:
        echo 1. Ejecuta este archivo desde la carpeta del bot
        echo 2. O ejecuta INSTALAR.bat de nuevo
        echo.
        echo Ruta actual: %CD%
        echo.
        pause
        exit /b 1
    )
)

:: ===========================================================
:: PASO 2: AUTO-VALIDACION Y REPARACION
:: ===========================================================

echo ============================================================
echo    BOT RPA CLARO - VERIFICACION AUTOMATICA
echo ============================================================
echo.
echo [*] Verificando configuracion...
echo.

set NEED_INSTALL=0
set ERROR_MSGS=

:: Verificar Python
set PYTHON_FOUND=0
set PYTHON_CMD=

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=python
)

if %PYTHON_FOUND% equ 0 (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_FOUND=1
        set PYTHON_CMD=py
    )
)

if %PYTHON_FOUND% equ 0 (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_FOUND=1
        set PYTHON_CMD=python3
    )
)

if %PYTHON_FOUND% equ 0 (
    echo [X] Python no encontrado
    set NEED_INSTALL=1
    set ERROR_MSGS=%ERROR_MSGS% Python
) else (
    echo [OK] Python detectado
)

:: Verificar entorno virtual
if not exist ".venv" (
    echo [X] Entorno virtual no existe
    set NEED_INSTALL=1
    set ERROR_MSGS=%ERROR_MSGS% Entorno-Virtual
) else (
    if not exist ".venv\Scripts\activate.bat" (
        echo [X] Entorno virtual corrupto
        set NEED_INSTALL=1
        set ERROR_MSGS=%ERROR_MSGS% Entorno-Corrupto
    ) else (
        echo [OK] Entorno virtual OK
    )
)

:: Verificar archivos principales
if not exist "gui.py" (
    echo [X] Falta gui.py
    set NEED_INSTALL=1
)

if not exist "index.py" (
    echo [X] Falta index.py
    set NEED_INSTALL=1
)

if not exist "requirements.txt" (
    echo [X] Falta requirements.txt
    set NEED_INSTALL=1
)

:: Si hay problemas, ofrecer auto-reparacion
if %NEED_INSTALL% equ 1 (
    echo.
    echo ============================================================
    echo    SE DETECTARON PROBLEMAS
    echo ============================================================
    echo.
    echo Problemas encontrados: %ERROR_MSGS%
    echo.
    echo El bot necesita ser instalado/reparado.
    echo.
    echo [1] Auto-reparar ahora (Recomendado)
    echo [2] Salir y hacerlo manualmente
    echo.
    set /p repair_choice="Selecciona [1/2]: "
    
    if "!repair_choice!"=="1" (
        echo.
        echo [*] Iniciando auto-reparacion...
        echo.
        
        if exist "INSTALAR.bat" (
            call INSTALAR.bat
            
            echo.
            echo [*] Reparacion completada, reiniciando bot...
            timeout /t 3 >nul
            
            :: Reiniciar este script
            start "" "%~f0"
            exit /b 0
        ) else (
            echo [X] No se encuentra INSTALAR.bat
            echo [!] Por favor descarga el bot nuevamente
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo [!] Por favor ejecuta INSTALAR.bat manualmente
        pause
        exit /b 1
    )
)

echo.
echo [OK] Todas las verificaciones pasaron
echo.
timeout /t 2 >nul

:: ===========================================================
:: PASO 3: ACTIVAR ENTORNO Y MOSTRAR MENU
:: ===========================================================

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
%PYTHON_CMD% gui.py
goto MENU

:CONSOLA
cls
echo ============================================================
echo    EJECUTANDO BOT EN MODO CONSOLA
echo ============================================================
echo.
%PYTHON_CMD% index.py
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

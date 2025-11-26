@echo off
title BOT RPA CLARO
color 0B
cls

:: Activar entorno virtual
if not exist ".venv" (
    echo ============================================================
    echo    ERROR: Entorno no configurado
    echo ============================================================
    echo.
    echo [!] Primero debes ejecutar "INSTALAR.bat"
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

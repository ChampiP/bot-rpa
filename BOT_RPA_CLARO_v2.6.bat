@echo off
chcp 65001 >nul
color 0A
title Bot RPA Claro v2.6 - ULTRA RAPIDO

:MENU
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║       BOT RPA CLARO v2.6 - ULTRA RAPIDO AUTOMATICO       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo  [1] 🚀 Ejecutar Bot con Interfaz Gráfica (.exe)
echo  [2] 📋 Ejecutar Bot con Python (desarrollo)
echo  [3] 🔨 Crear nuevo ejecutable (.exe)
echo  [4] 📂 Abrir carpeta de descargas
echo  [5] ⚙️  Abrir configuración (.env)
echo  [6] ❌ Salir
echo.
echo ═══════════════════════════════════════════════════════════
set /p opcion="Selecciona una opción [1-6]: "

if "%opcion%"=="1" goto EJECUTAR_EXE
if "%opcion%"=="2" goto EJECUTAR_PYTHON
if "%opcion%"=="3" goto CREAR_EXE
if "%opcion%"=="4" goto ABRIR_DESCARGAS
if "%opcion%"=="5" goto ABRIR_CONFIG
if "%opcion%"=="6" goto SALIR
goto MENU

:EJECUTAR_EXE
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo  🚀 Ejecutando Bot RPA v2.6 (.exe)
echo ═══════════════════════════════════════════════════════════
echo.
if exist "dist\BotRPA_Claro_v2.6.exe" (
    echo ✅ Ejecutando interfaz gráfica...
    start "" "dist\BotRPA_Claro_v2.6.exe"
    echo.
    echo ✅ Bot iniciado correctamente
    timeout /t 3 >nul
) else (
    echo ❌ ERROR: No se encontró el ejecutable
    echo.
    echo 💡 Usa la opción [3] para crear el .exe primero
    pause
)
goto MENU

:EJECUTAR_PYTHON
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo  🐍 Ejecutando Bot con Python (Desarrollo)
echo ═══════════════════════════════════════════════════════════
echo.
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    python gui.py
) else (
    python gui.py
)
pause
goto MENU

:CREAR_EXE
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo  🔨 Creando ejecutable con PyInstaller
echo ═══════════════════════════════════════════════════════════
echo.
echo ⏳ Este proceso puede tomar 1-3 minutos...
echo.
python -m PyInstaller BotRPA.spec --clean
echo.
if exist "dist\BotRPA_Claro_v2.6.exe" (
    echo ✅ Ejecutable creado exitosamente
    echo 📁 Ubicación: dist\BotRPA_Claro_v2.6.exe
    for %%A in ("dist\BotRPA_Claro_v2.6.exe") do echo 📏 Tamaño: %%~zA bytes
) else (
    echo ❌ ERROR: No se pudo crear el ejecutable
    echo 💡 Verifica que PyInstaller esté instalado: pip install pyinstaller
)
echo.
pause
goto MENU

:ABRIR_DESCARGAS
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo  📂 Abriendo carpeta de descargas
echo ═══════════════════════════════════════════════════════════
echo.
start "" "%USERPROFILE%\Downloads"
timeout /t 2 >nul
goto MENU

:ABRIR_CONFIG
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo  ⚙️  Abriendo archivo de configuración
echo ═══════════════════════════════════════════════════════════
echo.
if exist ".env" (
    notepad .env
) else (
    echo ❌ El archivo .env no existe todavía
    echo 💡 Se creará automáticamente al guardar la configuración en la interfaz
    echo.
    pause
)
goto MENU

:SALIR
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo  ¡Hasta luego! 👋
echo ═══════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul
exit

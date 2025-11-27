@echo off
title BOT RPA CLARO v2.5 - MENU PRINCIPAL
color 0B
setlocal enabledelayedexpansion

:: ============================================================
:: BOT RPA CLARO - TODO EN UNO
:: Version 2.5.0 - Sistema unificado y simplificado
:: ============================================================

:INICIO
cls
echo.
echo ============================================================
echo          BOT RPA CLARO v2.5 - MENU PRINCIPAL
echo ============================================================
echo.
echo  [1] Ejecutar Bot (Interfaz Grafica)
echo  [2] Ejecutar Bot (Modo Consola)
echo  [3] Instalar / Reparar Bot
echo  [4] Verificar Sistema
echo  [5] Salir
echo.
echo ============================================================
set /p opcion="Selecciona una opcion [1-5]: "

if "%opcion%"=="1" goto EJECUTAR_GUI
if "%opcion%"=="2" goto EJECUTAR_CONSOLA
if "%opcion%"=="3" goto INSTALAR
if "%opcion%"=="4" goto VERIFICAR
if "%opcion%"=="5" goto SALIR

echo.
echo [!] Opcion invalida. Intenta de nuevo.
timeout /t 2 >nul
goto INICIO

:: ============================================================
:: EJECUTAR GUI
:: ============================================================
:EJECUTAR_GUI
cls
echo.
echo ============================================================
echo    INICIANDO BOT - INTERFAZ GRAFICA
echo ============================================================
echo.

call :DETECTAR_PYTHON
if %PYTHON_FOUND% equ 0 (
    echo [X] Python no encontrado. Ejecuta la opcion [3] para instalar.
    pause
    goto INICIO
)

call :VERIFICAR_ENTORNO
if %VENV_OK% equ 0 (
    echo [X] Entorno no configurado. Ejecuta la opcion [3] para reparar.
    pause
    goto INICIO
)

echo [*] Activando entorno virtual...
call .venv\Scripts\activate.bat

echo [*] Cerrando Chrome si esta abierto...
taskkill /F /IM chrome.exe /T >nul 2>&1

echo [*] Iniciando interfaz grafica...
echo.
start "Bot RPA GUI" cmd /k "%PYTHON_CMD% gui.py"

echo.
echo [OK] Bot iniciado en nueva ventana
echo.
timeout /t 3 >nul
goto INICIO

:: ============================================================
:: EJECUTAR CONSOLA
:: ============================================================
:EJECUTAR_CONSOLA
cls
echo.
echo ============================================================
echo    INICIANDO BOT - MODO CONSOLA
echo ============================================================
echo.

call :DETECTAR_PYTHON
if %PYTHON_FOUND% equ 0 (
    echo [X] Python no encontrado. Ejecuta la opcion [3] para instalar.
    pause
    goto INICIO
)

call :VERIFICAR_ENTORNO
if %VENV_OK% equ 0 (
    echo [X] Entorno no configurado. Ejecuta la opcion [3] para reparar.
    pause
    goto INICIO
)

echo [*] Activando entorno virtual...
call .venv\Scripts\activate.bat

echo [*] Cerrando Chrome si esta abierto...
taskkill /F /IM chrome.exe /T >nul 2>&1

echo [*] Iniciando bot...
echo.
%PYTHON_CMD% index.py

echo.
echo ============================================================
echo    PROCESO FINALIZADO
echo ============================================================
echo.
pause
goto INICIO

:: ============================================================
:: INSTALAR / REPARAR
:: ============================================================
:INSTALAR
cls
echo.
echo ============================================================
echo    INSTALACION / REPARACION DEL BOT
echo ============================================================
echo.

call :DETECTAR_PYTHON
if %PYTHON_FOUND% equ 0 (
    echo [!] Python NO detectado
    echo.
    echo Opciones:
    echo [1] Intentar instalacion automatica con winget
    echo [2] Instrucciones para instalacion manual
    echo [3] Volver al menu
    echo.
    set /p inst_option="Selecciona [1-3]: "
    
    if "!inst_option!"=="1" goto INSTALAR_PYTHON_AUTO
    if "!inst_option!"=="2" goto INSTALAR_PYTHON_MANUAL
    if "!inst_option!"=="3" goto INICIO
    goto INICIO
)

echo [OK] Python detectado: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: Verificar/crear entorno virtual
echo [PASO 1/3] Configurando entorno virtual...
if exist ".venv" (
    echo [*] Entorno virtual existente detectado
    choice /C SN /M "Deseas recrearlo desde cero? [S=Si, N=No]"
    if errorlevel 2 goto INSTALAR_DEPS
    echo [*] Eliminando entorno anterior...
    rmdir /s /q .venv
)

echo [*] Creando nuevo entorno virtual...
%PYTHON_CMD% -m venv .venv
if %errorlevel% neq 0 (
    echo [!] Error creando entorno. Intentando instalar virtualenv...
    %PYTHON_CMD% -m pip install virtualenv
    %PYTHON_CMD% -m virtualenv .venv
)

if %errorlevel% neq 0 (
    echo [X] No se pudo crear el entorno virtual
    pause
    goto INICIO
)
echo [OK] Entorno virtual creado

:INSTALAR_DEPS
echo.
echo [PASO 2/3] Instalando dependencias...
call .venv\Scripts\activate.bat

pip install --upgrade pip >nul 2>&1
pip install --upgrade -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Error instalando dependencias. Reintentando...
    pip install --upgrade pip setuptools wheel
    pip install --upgrade -r requirements.txt
)

if %errorlevel% neq 0 (
    echo [X] Error instalando dependencias
    pause
    goto INICIO
)
echo [OK] Dependencias instaladas

echo.
echo [PASO 3/3] Configurando estructura...
if not exist "config" mkdir config
if not exist "Diagramas_Claro_Final" mkdir Diagramas_Claro_Final

if not exist "config\terms.json" (
    echo [*] Creando configuracion inicial...
    echo {"lista_busqueda":["Migracion de plan","Guia de cuestionamiento para cobro de recibo","Bloqueo de linea y equipo"]}> config\terms.json
)

if not exist ".env" (
    echo [*] Creando archivo .env de ejemplo...
    (
        echo # Credenciales Bot RPA v2.5
        echo CLARO_USUARIO=
        echo CLARO_CLAVE=
        echo URL_LOGIN=http://portaldeconocimiento.claro.com.pe/web/guest/login
        echo URL_BUSCADOR=http://portaldeconocimiento.claro.com.pe/comunicaciones-internas
        echo ID_BARRA_BUSQUEDA=_3_keywords
        echo DEBUG_MODE=false
        echo PROXY_ENABLED=false
        echo PROXY_HOST=
        echo PROXY_PORT=
        echo TIMING_SHORT_WAIT=0.5
        echo TIMING_MEDIUM_WAIT=2
        echo TIMING_LONG_WAIT=5
        echo TIMING_PAGE_LOAD=180
        echo TIMING_EXPLICIT_WAIT=20
        echo TIMING_DOWNLOAD_TIMEOUT=60
        echo TIMING_RATE_LIMIT=1.5
        echo TIMING_RETRY_DELAY=3
    ) > .env
    echo [!] IMPORTANTE: Configura tus credenciales en el archivo .env
)

echo [OK] Estructura configurada
echo.
echo ============================================================
echo    INSTALACION COMPLETADA
echo ============================================================
echo.
echo [OK] El bot esta listo para usar
echo [*] Usa la opcion [1] para ejecutar la interfaz grafica
echo.
pause
goto INICIO

:INSTALAR_PYTHON_AUTO
cls
echo.
echo [*] Intentando instalar Python con winget...
echo [*] Esto puede tomar varios minutos...
echo.

winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements

if %errorlevel% neq 0 (
    echo.
    echo [!] La instalacion automatica fallo
    goto INSTALAR_PYTHON_MANUAL
)

echo.
echo [OK] Python instalado
echo [*] REINICIA esta ventana y vuelve a ejecutar el bot
echo.
pause
exit /b 0

:INSTALAR_PYTHON_MANUAL
cls
echo.
echo ============================================================
echo    INSTRUCCIONES - INSTALACION MANUAL DE PYTHON
echo ============================================================
echo.
echo 1. Abre tu navegador y ve a:
echo    https://www.python.org/downloads/
echo.
echo 2. Descarga Python 3.11 o superior
echo.
echo 3. Durante la instalacion:
echo    [IMPORTANTE] Marca: "Add Python to PATH"
echo    Click en "Install Now"
echo.
echo 4. Una vez instalado, REINICIA esta ventana
echo    y ejecuta el bot nuevamente
echo.
echo ============================================================
pause
goto INICIO

:: ============================================================
:: VERIFICAR SISTEMA
:: ============================================================
:VERIFICAR
cls
echo.
echo ============================================================
echo    VERIFICACION DEL SISTEMA
echo ============================================================
echo.

call :DETECTAR_PYTHON
echo.
echo [TEST 1] Deteccion de Python
if %PYTHON_FOUND% equ 1 (
    echo [OK] Python encontrado: %PYTHON_CMD%
    %PYTHON_CMD% --version
    %PYTHON_CMD% -c "import sys; print('     Ruta:', sys.executable)"
) else (
    echo [X] Python NO encontrado
)

echo.
echo [TEST 2] Entorno Virtual
call :VERIFICAR_ENTORNO
if %VENV_OK% equ 1 (
    echo [OK] Entorno virtual configurado
    echo     Ruta: %CD%\.venv
) else (
    echo [X] Entorno virtual NO configurado
)

echo.
echo [TEST 3] Archivos principales
set FILES_OK=1
if not exist "index.py" (
    echo [X] Falta: index.py
    set FILES_OK=0
) else (
    echo [OK] index.py
)

if not exist "gui.py" (
    echo [X] Falta: gui.py
    set FILES_OK=0
) else (
    echo [OK] gui.py
)

if not exist "requirements.txt" (
    echo [X] Falta: requirements.txt
    set FILES_OK=0
) else (
    echo [OK] requirements.txt
)

if not exist "config\terms.json" (
    echo [X] Falta: config\terms.json
    set FILES_OK=0
) else (
    echo [OK] config\terms.json
)

if not exist ".env" (
    echo [!] Falta: .env (necesitas configurarlo)
) else (
    echo [OK] .env
)

echo.
echo [TEST 4] Dependencias
if %VENV_OK% equ 1 (
    call .venv\Scripts\activate.bat
    pip list | findstr "selenium"
    pip list | findstr "dotenv"
    pip list | findstr "requests"
) else (
    echo [!] No se puede verificar (entorno no configurado)
)

echo.
echo ============================================================
echo    RESUMEN
echo ============================================================
if %PYTHON_FOUND% equ 1 if %VENV_OK% equ 1 if %FILES_OK% equ 1 (
    echo [OK] Todo configurado correctamente
    echo [*] Puedes ejecutar el bot sin problemas
) else (
    echo [!] Algunos componentes necesitan atencion
    echo [*] Ejecuta la opcion [3] para reparar
)
echo ============================================================
echo.
pause
goto INICIO

:: ============================================================
:: FUNCIONES AUXILIARES
:: ============================================================

:DETECTAR_PYTHON
set PYTHON_FOUND=0
set PYTHON_CMD=

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=python
    goto :eof
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=py
    goto :eof
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=python3
    goto :eof
)

goto :eof

:VERIFICAR_ENTORNO
set VENV_OK=0

if exist ".venv\Scripts\activate.bat" (
    if exist ".venv\Scripts\python.exe" (
        set VENV_OK=1
    )
)

goto :eof

:: ============================================================
:: SALIR
:: ============================================================
:SALIR
cls
echo.
echo Gracias por usar Bot RPA Claro v2.5
echo.
timeout /t 2 >nul
exit /b 0

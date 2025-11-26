@echo off
title INSTALADOR BOT RPA CLARO - DESCARGA DESDE GITHUB
color 0A
cls

echo ============================================================
echo    BOT RPA CLARO - INSTALADOR AUTOMATICO
echo ============================================================
echo.
echo Este instalador descargara el bot desde GitHub e
echo instalara todas las dependencias automaticamente.
echo.
echo Presiona cualquier tecla para comenzar...
pause >nul

cls
echo.
echo [PASO 1/5] Verificando Git...
echo ------------------------------------------------------------

:: Verificar Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Git NO detectado
    echo [*] Descargando e instalando Git...
    
    winget install -e --id Git.Git --silent --accept-package-agreements --accept-source-agreements >nul 2>&1
    
    if %errorlevel% neq 0 (
        echo.
        echo [X] No se pudo instalar Git automaticamente
        echo.
        echo SOLUCION MANUAL:
        echo 1. Descarga Git desde: https://git-scm.com/download/win
        echo 2. Instala Git
        echo 3. Ejecuta este instalador nuevamente
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] Git instalado
    echo [*] Por favor REINICIA este instalador
    pause
    exit /b 0
) else (
    git --version
    echo [OK] Git detectado
)

echo.
echo [PASO 2/5] Verificando Python...
echo ------------------------------------------------------------

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python NO detectado
    echo [*] Instalando Python 3.11...
    
    winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements >nul 2>&1
    
    if %errorlevel% neq 0 (
        echo.
        echo [X] No se pudo instalar Python
        echo.
        echo SOLUCION MANUAL:
        echo 1. Descarga Python desde: https://www.python.org/downloads/
        echo 2. Durante instalacion marca "Add Python to PATH"
        echo 3. Ejecuta este instalador nuevamente
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] Python instalado
    echo [*] Por favor REINICIA este instalador
    pause
    exit /b 0
) else (
    python --version
    echo [OK] Python detectado
)

echo.
echo [PASO 3/5] Descargando bot desde GitHub...
echo ------------------------------------------------------------

:: Crear carpeta temporal si no existe
if not exist "bot_temp" (
    mkdir bot_temp
)

cd bot_temp

:: Clonar repositorio (CAMBIA ESTA URL POR LA TUYA)
echo [*] Clonando repositorio...
git clone https://github.com/TU_USUARIO/bot-rpa-claro.git .

if %errorlevel% neq 0 (
    echo [X] Error descargando el bot
    echo [!] Verifica la URL del repositorio
    pause
    exit /b 1
)

echo [OK] Bot descargado correctamente

echo.
echo [PASO 4/5] Creando entorno virtual...
echo ------------------------------------------------------------

python -m venv .venv
if %errorlevel% neq 0 (
    echo [X] Error creando entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

echo.
echo [PASO 5/5] Instalando dependencias...
echo ------------------------------------------------------------

call .venv\Scripts\activate.bat

pip install --upgrade pip >nul 2>&1
echo [*] Instalando paquetes...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [X] Error instalando dependencias
    echo [*] Intentando reparar...
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
)

echo [OK] Dependencias instaladas

:: Crear carpetas necesarias
if not exist "config" mkdir config
if not exist "Diagramas_Claro_Final" mkdir Diagramas_Claro_Final

:: Crear .env ejemplo si no existe
if not exist ".env" (
    echo # Configuracion del Bot RPA Claro > .env
    echo CLARO_USUARIO=tu_usuario >> .env
    echo CLARO_CLAVE=tu_contraseña >> .env
    echo URL_LOGIN=http://portaldeconocimiento.claro.com.pe/web/guest/login >> .env
    echo URL_BUSCADOR=http://portaldeconocimiento.claro.com.pe/comunicaciones-internas >> .env
    echo ID_BARRA_BUSQUEDA=_3_keywords >> .env
)

echo.
echo ============================================================
echo    INSTALACION COMPLETADA
echo ============================================================
echo.
echo [OK] El bot se descargo e instalo correctamente
echo.
echo PROXIMO PASO:
echo 1. Ejecuta "EJECUTAR_BOT.bat"
echo 2. Configura tus credenciales
echo 3. ¡Usa el bot!
echo.
pause

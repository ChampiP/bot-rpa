@echo off
title INSTALADOR BOT RPA CLARO
color 0A
cls

echo ============================================================
echo    INSTALADOR AUTOMATICO - BOT RPA CLARO
echo ============================================================
echo.
echo Este instalador configurara todo automaticamente.
echo Solo necesitas dar click y esperar.
echo.
echo Presiona cualquier tecla para comenzar...
pause >nul

cls
echo.
echo [PASO 1/4] Verificando Python...
echo ------------------------------------------------------------

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python NO detectado
    echo [*] Descargando Python 3.11...
    
    :: Intentar instalar con winget (Windows 10/11)
    winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements >nul 2>&1
    
    if %errorlevel% neq 0 (
        echo.
        echo [X] No se pudo instalar Python automaticamente
        echo.
        echo SOLUCION MANUAL:
        echo 1. Descarga Python desde: https://www.python.org/downloads/
        echo 2. Durante instalacion, marca "Add Python to PATH"
        echo 3. Ejecuta este instalador nuevamente
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] Python instalado correctamente
    echo [*] Por favor REINICIA este instalador para continuar
    pause
    exit /b 0
) else (
    python --version
    echo [OK] Python detectado correctamente
)

echo.
echo [PASO 2/4] Creando entorno virtual...
echo ------------------------------------------------------------

if exist ".venv" (
    echo [*] Entorno virtual ya existe, eliminando anterior...
    rmdir /s /q .venv
)

python -m venv .venv
if %errorlevel% neq 0 (
    echo [X] Error creando entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

echo.
echo [PASO 3/4] Instalando dependencias...
echo ------------------------------------------------------------

call .venv\Scripts\activate.bat

pip install --upgrade pip >nul 2>&1
echo [*] Instalando paquetes necesarios...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [X] Error instalando dependencias
    echo [*] Intentando reparar...
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo [X] No se pudo completar la instalacion
        pause
        exit /b 1
    )
)

echo [OK] Todas las dependencias instaladas

echo.
echo [PASO 4/4] Configurando archivos...
echo ------------------------------------------------------------

:: Crear carpetas necesarias
if not exist "config" mkdir config
if not exist "Diagramas_Claro_Final" mkdir Diagramas_Claro_Final

:: Verificar que existe terms.json
if not exist "config\terms.json" (
    echo [!] Creando archivo de configuracion inicial...
    echo {"lista_busqueda":["Migracion de plan","Guia de cuestionamiento para cobro de recibo"]} > config\terms.json
)

echo [OK] Configuracion completada

echo.
echo ============================================================
echo    INSTALACION COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo [OK] El bot esta listo para usar
echo.
echo PROXIMO PASO:
echo - Ejecuta "EJECUTAR_BOT.bat" para iniciar el bot
echo - Se abrira una interfaz grafica simple
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul

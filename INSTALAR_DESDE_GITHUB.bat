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
echo [*] Se instalara en: %USERPROFILE%\Desktop\Bot_RPA_Claro
echo.
echo Presiona cualquier tecla para comenzar...
pause >nul

cls
echo.
echo [PASO 1/6] Preparando carpeta de instalacion...
echo ------------------------------------------------------------

:: Definir ruta de instalacion (SIEMPRE en Desktop)
set "INSTALL_DIR=%USERPROFILE%\Desktop\Bot_RPA_Claro"

:: Si ya existe, preguntar
if exist "%INSTALL_DIR%" (
    echo [!] Ya existe una instalacion en Desktop
    echo [?] Deseas reinstalar? Esto borrara la version anterior.
    choice /C SN /M "[S]i reinstalar o [N]o cancelar"
    if errorlevel 2 (
        echo [*] Instalacion cancelada
        pause
        exit /b 0
    )
    echo [*] Eliminando version anterior...
    rmdir /s /q "%INSTALL_DIR%" 2>nul
)

:: Crear carpeta en Desktop
mkdir "%INSTALL_DIR%"
if %errorlevel% neq 0 (
    echo [X] No se pudo crear la carpeta en Desktop
    pause
    exit /b 1
)

echo [OK] Carpeta creada: %INSTALL_DIR%

echo.
echo [PASO 2/6] Verificando Git...
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
echo [PASO 3/6] Verificando Python...
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
echo [PASO 4/6] Descargando bot desde GitHub...
echo ------------------------------------------------------------

:: Cambiar a la carpeta de instalacion
cd /d "%INSTALL_DIR%"

:: Clonar repositorio
echo [*] Clonando repositorio en Desktop...
git clone https://github.com/ChampiP/bot-rpa.git .

if %errorlevel% neq 0 (
    echo [X] Error descargando el bot
    echo [!] Verifica la URL del repositorio
    pause
    exit /b 1
)

echo [OK] Bot descargado correctamente

echo.
echo [PASO 5/6] Creando entorno virtual...
echo ------------------------------------------------------------

python -m venv .venv
if %errorlevel% neq 0 (
    echo [X] Error creando entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

echo.
echo [PASO 6/6] Instalando dependencias...
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
echo [*] Copiando accesos directos al Escritorio...
echo ------------------------------------------------------------

:: Copiar todos los .bat importantes al Desktop para facil acceso
copy /Y "EJECUTAR_BOT.bat" "%USERPROFILE%\Desktop\" >nul 2>&1
copy /Y "INSTALAR.bat" "%USERPROFILE%\Desktop\" >nul 2>&1
copy /Y "VALIDAR_BOT.bat" "%USERPROFILE%\Desktop\" >nul 2>&1
copy /Y "SUBIR_A_GITHUB.bat" "%USERPROFILE%\Desktop\" >nul 2>&1

echo [OK] Accesos directos creados en el Escritorio

echo.
echo ============================================================
echo    INSTALACION COMPLETADA
echo ============================================================
echo.
echo [OK] Bot instalado en: %INSTALL_DIR%
echo [OK] Accesos directos copiados al Escritorio
echo.
echo PROXIMO PASO:
echo 1. Ve a tu Escritorio (Desktop)
echo 2. Ejecuta "EJECUTAR_BOT.bat"
echo 3. Configura tus credenciales
echo 4. ¡Usa el bot!
echo.
echo NOTA: La carpeta completa esta en Desktop\Bot_RPA_Claro
echo.
pause

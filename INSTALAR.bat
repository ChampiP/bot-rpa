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

:: Verificar si Python esta instalado y en el PATH
set PYTHON_FOUND=0
set PYTHON_CMD=

:: Intentar python directamente
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=python
    goto :PYTHON_OK
)

:: Intentar py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=py
    goto :PYTHON_OK
)

:: Intentar python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=python3
    goto :PYTHON_OK
)

:: Python no encontrado - intentar instalacion
:PYTHON_NOT_FOUND
echo [!] Python NO detectado en el sistema
echo.
echo [*] Intentando instalacion automatica...
echo.

:: Verificar si winget esta disponible
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Winget no esta disponible en este sistema
    goto :MANUAL_INSTALL
)

echo [*] Instalando Python 3.11 con winget...
echo [*] Esto puede tomar varios minutos, por favor espera...
echo.

:: Instalar Python con winget
winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements

if %errorlevel% neq 0 (
    echo.
    echo [!] Instalacion con winget fallo, intentando Python 3.12...
    winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    
    if %errorlevel% neq 0 (
        goto :MANUAL_INSTALL
    )
)

echo.
echo [OK] Python instalado correctamente
echo.
echo [*] IMPORTANTE: Se debe reiniciar el sistema o abrir una nueva terminal
echo [*] Para que los cambios surtan efecto.
echo.
echo Opciones:
echo   [1] Reiniciar este instalador ahora (Recomendado)
echo   [2] Continuar de todos modos
echo.
set /p restart_choice="Selecciona [1/2]: "

if "%restart_choice%"=="1" (
    echo.
    echo [*] Reiniciando instalador...
    timeout /t 2 >nul
    start "" "%~f0"
    exit /b 0
)

:: Actualizar PATH en la sesion actual
echo [*] Actualizando PATH en esta sesion...
call :RefreshEnv

:: Verificar nuevamente
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=python
    goto :PYTHON_OK
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_FOUND=1
    set PYTHON_CMD=py
    goto :PYTHON_OK
)

echo [!] Python instalado pero no se puede ejecutar en esta sesion
echo [*] Por favor, cierra esta ventana y ejecuta INSTALAR.bat nuevamente
pause
exit /b 1

:MANUAL_INSTALL
echo.
echo ============================================================
echo [X] NO SE PUDO INSTALAR PYTHON AUTOMATICAMENTE
echo ============================================================
echo.
echo INSTRUCCIONES PARA INSTALACION MANUAL:
echo.
echo 1. Abre tu navegador y ve a:
echo    https://www.python.org/downloads/
echo.
echo 2. Descarga Python 3.11 o superior
echo.
echo 3. Durante la instalacion:
echo    - IMPORTANTE: Marca la casilla "Add Python to PATH"
echo    - Haz click en "Install Now"
echo.
echo 4. Una vez instalado, ejecuta este instalador nuevamente
echo.
echo ============================================================
echo.
pause
exit /b 1

:PYTHON_OK
%PYTHON_CMD% --version
echo [OK] Python detectado correctamente (comando: %PYTHON_CMD%)

echo.
echo [PASO 2/4] Creando entorno virtual...
echo ------------------------------------------------------------

if exist ".venv" (
    echo [*] Entorno virtual ya existe, eliminando anterior...
    rmdir /s /q .venv
)

%PYTHON_CMD% -m venv .venv
if %errorlevel% neq 0 (
    echo [X] Error creando entorno virtual
    echo [*] Intentando instalar modulo venv...
    %PYTHON_CMD% -m pip install virtualenv
    %PYTHON_CMD% -m virtualenv .venv
    
    if %errorlevel% neq 0 (
        echo [X] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
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
echo [*] Copiando accesos directos al Escritorio...
echo ------------------------------------------------------------

:: Copiar .bat al Desktop para facil acceso
copy /Y "EJECUTAR_BOT.bat" "%USERPROFILE%\Desktop\" >nul 2>&1
copy /Y "VALIDAR_BOT.bat" "%USERPROFILE%\Desktop\" >nul 2>&1
copy /Y "SUBIR_A_GITHUB.bat" "%USERPROFILE%\Desktop\" >nul 2>&1

echo [OK] Accesos directos creados en el Escritorio

echo.
echo ============================================================
echo    INSTALACION COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo [OK] El bot esta listo para usar
echo [OK] Accesos directos en el Escritorio (Desktop)
echo.
echo PROXIMO PASO:
echo - Ve a tu Escritorio y ejecuta "EJECUTAR_BOT.bat"
echo - Se abrira una interfaz grafica simple
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
exit /b 0

:: Funcion para actualizar variables de entorno en la sesion actual
:RefreshEnv
echo [*] Actualizando variables de entorno...
:: Leer PATH del registro del sistema
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SystemPath=%%b"
:: Leer PATH del registro del usuario
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"
:: Combinar ambos
set "PATH=%SystemPath%;%UserPath%"
echo [OK] Variables actualizadas
goto :eof

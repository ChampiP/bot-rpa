@echo off
title VERIFICADOR DE PYTHON
color 0E
cls

echo ============================================================
echo    VERIFICADOR DE PYTHON - DIAGNOSTICO COMPLETO
echo ============================================================
echo.
echo Este script te ayudara a identificar problemas con Python.
echo.
pause

echo.
echo [TEST 1/6] Verificando comando 'python'...
echo ------------------------------------------------------------
python --version 2>&1
if %errorlevel% equ 0 (
    echo [OK] Comando 'python' funciona correctamente
    python -c "import sys; print('[INFO] Ruta:', sys.executable)"
    set PYTHON_OK=1
) else (
    echo [X] Comando 'python' no funciona
    set PYTHON_OK=0
)

echo.
echo [TEST 2/6] Verificando comando 'py' (Python Launcher)...
echo ------------------------------------------------------------
py --version 2>&1
if %errorlevel% equ 0 (
    echo [OK] Comando 'py' funciona correctamente
    py -c "import sys; print('[INFO] Ruta:', sys.executable)"
    set PY_OK=1
) else (
    echo [X] Comando 'py' no funciona
    set PY_OK=0
)

echo.
echo [TEST 3/6] Verificando comando 'python3'...
echo ------------------------------------------------------------
python3 --version 2>&1
if %errorlevel% equ 0 (
    echo [OK] Comando 'python3' funciona correctamente
    python3 -c "import sys; print('[INFO] Ruta:', sys.executable)"
    set PYTHON3_OK=1
) else (
    echo [X] Comando 'python3' no funciona
    set PYTHON3_OK=0
)

echo.
echo [TEST 4/6] Verificando winget (gestor de paquetes)...
echo ------------------------------------------------------------
winget --version 2>&1
if %errorlevel% equ 0 (
    echo [OK] Winget esta disponible
    set WINGET_OK=1
) else (
    echo [X] Winget no esta disponible
    echo [INFO] Winget viene con Windows 10/11 actualizados
    set WINGET_OK=0
)

echo.
echo [TEST 5/6] Buscando instalaciones de Python en el sistema...
echo ------------------------------------------------------------
echo [*] Buscando en directorios comunes...

set FOUND_INSTALLS=0

if exist "C:\Python*" (
    echo [ENCONTRADO] C:\Python*
    dir /b C:\Python* 2>nul
    set FOUND_INSTALLS=1
)

if exist "%LOCALAPPDATA%\Programs\Python" (
    echo [ENCONTRADO] %LOCALAPPDATA%\Programs\Python
    dir /b "%LOCALAPPDATA%\Programs\Python" 2>nul
    set FOUND_INSTALLS=1
)

if exist "C:\Program Files\Python*" (
    echo [ENCONTRADO] C:\Program Files\Python*
    dir /b "C:\Program Files\Python*" 2>nul
    set FOUND_INSTALLS=1
)

if %FOUND_INSTALLS% equ 0 (
    echo [INFO] No se encontraron instalaciones en rutas comunes
)

echo.
echo [TEST 6/6] Verificando variable PATH...
echo ------------------------------------------------------------
echo [*] Buscando Python en el PATH...

echo %PATH% | findstr /I "python" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python encontrado en el PATH
    echo [INFO] Rutas encontradas:
    echo %PATH% | findstr /I "python"
) else (
    echo [X] Python NO esta en el PATH
    echo [!] Este es probablemente el problema principal
)

echo.
echo ============================================================
echo    RESUMEN DEL DIAGNOSTICO
echo ============================================================
echo.

set TOTAL_OK=0
if %PYTHON_OK% equ 1 set /a TOTAL_OK+=1
if %PY_OK% equ 1 set /a TOTAL_OK+=1
if %PYTHON3_OK% equ 1 set /a TOTAL_OK+=1

echo Estado de comandos Python:
echo   - 'python'  : %PYTHON_OK%
echo   - 'py'      : %PY_OK%
echo   - 'python3' : %PYTHON3_OK%
echo   - Total OK  : %TOTAL_OK%/3
echo.

if %TOTAL_OK% gtr 0 (
    echo [OK] Python esta instalado y funciona
    echo [OK] Puedes continuar con INSTALAR.bat
) else (
    echo [X] Python no esta correctamente instalado o configurado
    echo.
    echo ============================================================
    echo    RECOMENDACIONES
    echo ============================================================
    echo.
    
    if %WINGET_OK% equ 1 (
        echo [OPCION 1] Instalacion automatica con winget:
        echo    Ejecuta INSTALAR.bat y el instalador lo hara automaticamente
        echo.
    )
    
    echo [OPCION 2] Instalacion manual:
    echo    1. Ve a: https://www.python.org/downloads/
    echo    2. Descarga Python 3.11 o superior
    echo    3. Durante instalacion marca "Add Python to PATH"
    echo    4. Reinicia la computadora
    echo    5. Ejecuta este verificador nuevamente
    echo.
    
    if %FOUND_INSTALLS% equ 1 (
        echo [OPCION 3] Reparar instalacion existente:
        echo    1. Ve a Panel de Control ^> Programas
        echo    2. Busca Python en la lista
        echo    3. Haz click derecho ^> Modificar
        echo    4. Selecciona "Modify" o "Repair"
        echo    5. Asegurate de marcar "Add Python to PATH"
        echo    6. Completa la reparacion
        echo    7. Reinicia la computadora
    )
)

echo.
echo ============================================================
pause
exit /b 0

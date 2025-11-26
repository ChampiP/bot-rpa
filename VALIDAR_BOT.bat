@echo off
title VALIDACION DEL BOT
color 0A
cls

echo ============================================================
echo    VALIDACION COMPLETA DEL BOT RPA CLARO
echo ============================================================
echo.
echo Este script verificara que todo este funcionando correctamente.
echo.
pause

echo.
echo [TEST 1/5] Verificando Python...
echo ------------------------------------------------------------
python --version
if %errorlevel% neq 0 (
    echo [X] FALLO: Python no encontrado
    echo     Ejecuta INSTALAR.bat primero
    goto ERROR
)
echo [OK] Python detectado

echo.
echo [TEST 2/5] Verificando entorno virtual...
echo ------------------------------------------------------------
if not exist ".venv" (
    echo [X] FALLO: Entorno virtual no existe
    echo     Ejecuta INSTALAR.bat primero
    goto ERROR
)
echo [OK] Entorno virtual existe

echo.
echo [TEST 3/5] Verificando archivos principales...
echo ------------------------------------------------------------
set ARCHIVOS_REQUERIDOS=index.py gui.py requirements.txt config\terms.json
set FALLO=0

for %%F in (%ARCHIVOS_REQUERIDOS%) do (
    if not exist "%%F" (
        echo [X] Falta: %%F
        set FALLO=1
    ) else (
        echo [OK] %%F
    )
)

if %FALLO%==1 (
    echo [X] FALLO: Faltan archivos necesarios
    goto ERROR
)

echo.
echo [TEST 4/5] Verificando sintaxis de Python...
echo ------------------------------------------------------------
call .venv\Scripts\activate.bat
python -m py_compile index.py
if %errorlevel% neq 0 (
    echo [X] FALLO: Error de sintaxis en index.py
    goto ERROR
)
echo [OK] index.py sin errores

python -m py_compile gui.py
if %errorlevel% neq 0 (
    echo [X] FALLO: Error de sintaxis en gui.py
    goto ERROR
)
echo [OK] gui.py sin errores

echo.
echo [TEST 5/5] Verificando dependencias...
echo ------------------------------------------------------------
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ADVERTENCIA: Selenium no instalado
    echo     Ejecuta INSTALAR.bat para instalar dependencias
) else (
    echo [OK] Selenium instalado
)

pip show python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ADVERTENCIA: python-dotenv no instalado
    echo     Ejecuta INSTALAR.bat para instalar dependencias
) else (
    echo [OK] python-dotenv instalado
)

echo.
echo ============================================================
echo    VALIDACION COMPLETADA CON EXITO
echo ============================================================
echo.
echo [OK] Todos los tests pasaron
echo [OK] El bot esta listo para usar
echo.
echo Puedes ejecutar: EJECUTAR_BOT.bat
echo.
pause
exit /b 0

:ERROR
echo.
echo ============================================================
echo    VALIDACION FALLIDA
echo ============================================================
echo.
echo [!] Se encontraron problemas
echo [!] Por favor ejecuta: INSTALAR.bat
echo.
pause
exit /b 1

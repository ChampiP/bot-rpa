@echo off
title SUBIR BOT A GITHUB
color 0B
cls

echo ============================================================
echo    SUBIR BOT RPA CLARO A GITHUB
echo ============================================================
echo.
echo Este script te ayudara a subir el bot a GitHub.
echo.
echo REQUISITOS:
echo - Tener una cuenta de GitHub
echo - Tener Git instalado
echo.
echo Presiona cualquier tecla para continuar...
pause >nul

cls
echo.
echo ============================================================
echo    PASO 1: CREAR REPOSITORIO EN GITHUB
echo ============================================================
echo.
echo 1. Ve a: https://github.com/new
echo 2. Nombre del repositorio: bot-rpa-claro
echo 3. Descripcion: Bot RPA para descarga automatica de diagramas Claro
echo 4. Selecciona: Publico o Privado (tu eleccion)
echo 5. NO marques "Add a README file"
echo 6. Click en "Create repository"
echo.
echo Cuando termines, presiona cualquier tecla...
pause >nul

cls
echo.
echo ============================================================
echo    PASO 2: OBTENER URL DEL REPOSITORIO
echo ============================================================
echo.
echo En la pagina de GitHub, copia la URL que aparece en:
echo "Quick setup — if you've done this kind of thing before"
echo.
echo Ejemplo: https://github.com/TU_USUARIO/bot-rpa-claro.git
echo.
set /p REPO_URL="Pega aqui la URL de tu repositorio: "

echo.
echo [*] URL del repositorio: %REPO_URL%
echo.

cls
echo.
echo ============================================================
echo    PASO 3: CONFIGURAR GIT
echo ============================================================
echo.
set /p GIT_USER="Tu nombre de usuario de GitHub: "
set /p GIT_EMAIL="Tu email de GitHub: "

git config user.name "%GIT_USER%"
git config user.email "%GIT_EMAIL%"

echo [OK] Git configurado
echo.

cls
echo.
echo ============================================================
echo    PASO 4: SUBIR ARCHIVOS A GITHUB
echo ============================================================
echo.
echo [*] Conectando con repositorio remoto...
git remote add origin %REPO_URL%

if %errorlevel% neq 0 (
    echo [!] El remoto ya existe, actualizando...
    git remote set-url origin %REPO_URL%
)

echo [OK] Repositorio remoto configurado
echo.
echo [*] Subiendo archivos a GitHub...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [X] Error al subir archivos
    echo.
    echo POSIBLES SOLUCIONES:
    echo 1. Verifica que la URL sea correcta
    echo 2. Verifica tu conexion a internet
    echo 3. Asegurate de tener permisos en el repositorio
    echo 4. Si pide autenticacion, usa tu token de GitHub
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo    ¡EXITO! BOT SUBIDO A GITHUB
echo ============================================================
echo.
echo Tu bot ya esta en GitHub:
echo %REPO_URL%
echo.
echo PROXIMO PASO - COMPARTIR CON COMPANEROS:
echo.
echo 1. Comparte esta URL:
echo    https://github.com/%GIT_USER%/bot-rpa-claro
echo.
echo 2. Tus companeros pueden instalar con UN SOLO COMANDO:
echo.
echo    En PowerShell (Administrador):
echo    irm https://raw.githubusercontent.com/%GIT_USER%/bot-rpa-claro/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
echo.
echo 3. O descargar manualmente:
echo    - Ir a: https://github.com/%GIT_USER%/bot-rpa-claro
echo    - Click en "Code" -^> "Download ZIP"
echo    - Extraer y ejecutar INSTALAR.bat
echo.
pause

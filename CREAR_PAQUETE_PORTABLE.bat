@echo off
title CREAR PAQUETE PORTABLE
color 0E
cls

echo ============================================================
echo    CREADOR DE PAQUETE PORTABLE
echo ============================================================
echo.
echo Este script creara una carpeta lista para compartir
echo con tus companeros.
echo.
pause

set CARPETA_DESTINO=BOT_RPA_CLARO_PORTABLE

echo.
echo [*] Creando carpeta portable...
if exist "%CARPETA_DESTINO%" rmdir /s /q "%CARPETA_DESTINO%"
mkdir "%CARPETA_DESTINO%"
mkdir "%CARPETA_DESTINO%\config"

echo [*] Copiando archivos necesarios...

:: Archivos principales
copy /y "INSTALAR.bat" "%CARPETA_DESTINO%\"
copy /y "EJECUTAR_BOT.bat" "%CARPETA_DESTINO%\"
copy /y "LEEME.txt" "%CARPETA_DESTINO%\"
copy /y "index.py" "%CARPETA_DESTINO%\"
copy /y "gui.py" "%CARPETA_DESTINO%\"
copy /y "requirements.txt" "%CARPETA_DESTINO%\"

:: Archivos de configuracion (sin credenciales)
if exist "config\terms.json" copy /y "config\terms.json" "%CARPETA_DESTINO%\config\"

:: Crear .env de ejemplo (vacio)
echo # Configuracion del bot > "%CARPETA_DESTINO%\.env.ejemplo"
echo # Renombra este archivo a .env y completa los datos >> "%CARPETA_DESTINO%\.env.ejemplo"
echo CLARO_USUARIO=tu_usuario >> "%CARPETA_DESTINO%\.env.ejemplo"
echo CLARO_CLAVE=tu_contraseña >> "%CARPETA_DESTINO%\.env.ejemplo"
echo URL_LOGIN=http://portaldeconocimiento.claro.com.pe/web/guest/login >> "%CARPETA_DESTINO%\.env.ejemplo"
echo URL_BUSCADOR=http://portaldeconocimiento.claro.com.pe/comunicaciones-internas >> "%CARPETA_DESTINO%\.env.ejemplo"
echo ID_BARRA_BUSQUEDA=_3_keywords >> "%CARPETA_DESTINO%\.env.ejemplo"

echo.
echo ============================================================
echo    PAQUETE CREADO EXITOSAMENTE
echo ============================================================
echo.
echo La carpeta "%CARPETA_DESTINO%" esta lista para compartir.
echo.
echo INSTRUCCIONES PARA TUS COMPANEROS:
echo 1. Copia toda la carpeta "%CARPETA_DESTINO%"
echo 2. Abre la carpeta y ejecuta "INSTALAR.bat"
echo 3. Luego usa "EJECUTAR_BOT.bat"
echo.
echo Presiona cualquier tecla para abrir la carpeta...
pause >nul
explorer "%CARPETA_DESTINO%"

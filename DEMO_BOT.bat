@echo off
title DEMO - BOT RPA CLARO
color 0B
cls

echo ============================================================
echo    DEMOSTRACION DEL BOT RPA CLARO
echo ============================================================
echo.
echo Este script te mostrara el bot en accion con 2 busquedas
echo de prueba para que veas como funciona.
echo.
echo NOTA: Necesitas tener configuradas tus credenciales en .env
echo.
echo Presiona cualquier tecla para continuar...
pause >nul

:: Crear archivo temporal con solo 2 terminos para demo
echo {"lista_busqueda":["Migracion de plan","Guia de cuestionamiento para cobro de recibo"]} > config\terms_demo.json

cls
echo.
echo [*] Iniciando demo con 2 busquedas...
echo [*] Esto tomara aproximadamente 2 minutos
echo.

call .venv\Scripts\activate.bat

:: Backup del terms.json original
if exist config\terms.json (
    copy /y config\terms.json config\terms_backup.json >nul
)

:: Usar el archivo de demo
copy /y config\terms_demo.json config\terms.json >nul

:: Ejecutar bot
python index.py

:: Restaurar archivo original
if exist config\terms_backup.json (
    copy /y config\terms_backup.json config\terms.json >nul
    del config\terms_backup.json
)

del config\terms_demo.json

echo.
echo ============================================================
echo    DEMO COMPLETADA
echo ============================================================
echo.
echo Los archivos descargados estan en: %USERPROFILE%\Downloads
echo.
echo Si todo funciono bien, puedes usar el bot con confianza!
echo Para usar el bot completo: ejecuta EJECUTAR_BOT.bat
echo.
pause

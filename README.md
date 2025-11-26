🤖 BOT RPA - DESCARGA AUTOMÁTICA DE DIAGRAMAS CLARO

📋 Descripción

Este bot automatiza la descarga de diagramas y documentos del portal de Claro. El sistema permite configurar los términos de búsqueda y gestiona el proceso de obtención de archivos de manera autónoma.

🔗 Repositorio: https://github.com/ChampiP/bot-rpa

🚀 GUÍA DE INICIO RÁPIDO

📥 DESCARGA E INSTALACIÓN

Opción 1: Instalación Automática desde GitHub (Recomendado)
Ejecutar el siguiente comando en PowerShell (con permisos de Administrador):

irm [https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat](https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat) -outfile install.bat; .\install.bat


Opción 2: Descarga Manual

Ir a: https://github.com/ChampiP/bot-rpa

Hacer clic en "Code" → "Download ZIP".

Extraer los archivos en una carpeta local.

Ejecutar el archivo: INSTALAR.bat.

Esperar la finalización del proceso (aprox. 2-3 minutos).

1️⃣ INSTALACIÓN DE DEPENDENCIAS

Para la configuración inicial del entorno:

Ejecutar el archivo INSTALAR.bat.

Esperar a que la consola indique que el proceso ha finalizado.

2️⃣ CONFIGURACIÓN

Ejecutar el archivo EJECUTAR_BOT.bat.

Opción 1: Interfaz Gráfica.

Ir a la pestaña "Ajustes".

Ingresar las credenciales de acceso al portal (Usuario y Contraseña).

Seleccionar "Guardar".

3️⃣ EJECUCIÓN

Ir a la pestaña "Ejecutar".

Hacer clic en "🚀 INICIAR DESCARGA AUTOMÁTICA".

El bot iniciará el navegador y procesará las descargas automáticamente.

📁 Ubicación de Descargas

Los archivos descargados se almacenarán automáticamente en la ruta predeterminada del sistema:

C:\Users\%USERNAME%\Downloads


⚙️ ESTRUCTURA DE ARCHIVOS

Archivo

Descripción

Acción Requerida

INSTALAR.bat

Script de instalación automática de entorno y dependencias

✅ Ejecutar una vez al inicio

EJECUTAR_BOT.bat

Lanzador principal del bot

✅ Usar para iniciar la aplicación

LEEME.txt

Documentación técnica detallada

📖 Referencia

CREAR_PAQUETE_PORTABLE.bat

Generador de versión portable para distribución

✅ Ejecutar solo para redistribución

index.py

Lógica principal del bot (Python)

❌ No modificar

gui.py

Código de interfaz gráfica (Python)

❌ No modificar

🎯 PERSONALIZACIÓN DE BÚSQUEDAS

Opción 1: Interfaz Gráfica

Abrir EJECUTAR_BOT.bat.

Ir a la pestaña "Términos".

Agregar o eliminar los términos deseados en la lista.

Guardar los cambios.

Opción 2: Edición Manual

Acceder a la carpeta config.

Editar el archivo terms.json con un editor de texto (Notepad, VS Code).

Modificar la lista siguiendo el formato JSON estándar.

Ejemplo de estructura terms.json:

{
  "lista_busqueda": [
    "Migracion de plan",
    "Guia de cuestionamiento",
    "Bloqueo de linea"
  ]
}


🆘 SOLUCIÓN DE PROBLEMAS FRECUENTES

❌ "Python no encontrado"

Causa: Python no está instalado en el sistema o no se agregó a las variables de entorno (PATH).
Solución:

Ir a: https://www.python.org/downloads/

Descargar la versión Python 3.11 o superior.

Durante la instalación, marcar obligatoriamente la casilla "Add Python to PATH".

Ejecutar INSTALAR.bat nuevamente.

❌ "Error al instalar dependencias"

Solución:

Cerrar todas las ventanas de consola o procesos relacionados.

Ejecutar INSTALAR.bat nuevamente.

Si el error persiste, reiniciar el equipo e intentar de nuevo.

❌ "No se pudo acceder al portal"

Solución:

Verificar la conexión a internet.

Validar que las credenciales ingresadas en la pestaña "Ajustes" sean correctas.

Intentar acceder manualmente al portal mediante el navegador para descartar caídas del servicio.

❌ El bot se detiene

Nota: En la versión actual (2.3+), el bot gestiona las esperas automáticamente y no requiere interacción manual (presionar Enter) durante la ejecución normal.

📦 DESPLIEGUE Y DISTRIBUCIÓN

Método 1: Clonación desde GitHub

Compartir el enlace del repositorio público: https://github.com/ChampiP/bot-rpa
Los usuarios deberán descargar el ZIP y ejecutar INSTALAR.bat.

Método 2: Instalación vía Comandos (PowerShell)

Ejecutar el siguiente script en PowerShell con permisos de administrador:

irm [https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat](https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat) -outfile install.bat; .\install.bat


Método 3: Generación de Paquete Portable (Offline)

Ejecutar el script CREAR_PAQUETE_PORTABLE.bat.

Se generará una carpeta llamada BOT_RPA_CLARO_PORTABLE.

Distribuir dicha carpeta a los usuarios finales (vía USB, Red, Drive).

El usuario final solo deberá ejecutar INSTALAR.bat dentro de la carpeta recibida.

⚠️ IMPORTANTE: Al distribuir manualmente, NO incluir la carpeta .venv. El script de instalación generará el entorno virtual específico para el equipo de destino automáticamente.

🔒 SEGURIDAD Y PRIVACIDAD

Acceso: El bot interactúa exclusivamente con el portal de Claro especificado.

Datos: No se realiza envío de telemetría, logs ni datos a servidores externos.

Credenciales: Las contraseñas se almacenan localmente en el equipo del usuario.

Código Abierto: El proyecto es transparente y puede ser auditado.

💡 RECOMENDACIONES DE USO

Antes de ejecutar: Se recomienda cerrar instancias previas de Google Chrome para evitar conflictos con los drivers de Selenium.

Durante ejecución: Mantener abierta la ventana del navegador que inicia el bot (no minimizar si es posible).

Manejo de errores: El bot cuenta con sistemas de recuperación automática ante fallos de carga.

Archivos pesados: La descarga de diagramas extensos puede tomar tiempo adicional; el bot esperará a que finalicen.

Procesamiento: Las búsquedas se realizan de manera secuencial para asegurar la integridad de los datos.

📊 CARACTERÍSTICAS TÉCNICAS

✅ Interfaz gráfica de usuario (GUI) basada en Tkinter/CustomTkinter.

✅ Gestión automática de dependencias y entorno virtual (venv).

✅ Desbloqueo automático de archivos Excel protegidos mediante librería pywin32.

✅ Algoritmo de scoring para determinar la relevancia de resultados de búsqueda.

✅ Sistema de logs detallados para depuración y seguimiento.

✅ Estructura portable y modular.

📞 SOPORTE

En caso de incidencias técnicas:

Consultar el archivo LEEME.txt incluido en el paquete.

Revisar la sección de Solución de Problemas de este documento.

Reintentar la instalación de dependencias ejecutando INSTALAR.bat.

Versión: 2.3

Fecha: Noviembre 2025

# 🤖 BOT RPA – DESCARGA AUTOMÁTICA DE DIAGRAMAS CLARO

## 📋 Descripción General

Este bot permite descargar de forma automática los diagramas y documentos disponibles en el portal de Claro.  
Solo es necesario definir los términos de búsqueda y el sistema realizará el proceso completo.

**Repositorio:** https://github.com/ChampiP/bot-rpa

---

## 🚀 Inicio Rápido

### 📥 Instalación

**Opción 1: Instalación automática desde GitHub (Recomendada)**  
Ejecutar en PowerShell (NO necesita ser Administrador):

```bash
irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
```

✅ Se instala automáticamente en: `Desktop\Bot_RPA_Claro`  
✅ Los archivos .bat se copian al Escritorio para fácil acceso

**Opción 2: Instalación manual**

1. Acceder al repositorio: [https://github.com/ChampiP/bot-rpa](https://github.com/ChampiP/bot-rpa)
2. Seleccionar "Code" → "Download ZIP"
3. Extraer los archivos EN EL ESCRITORIO (Desktop)
4. Ejecutar `INSTALAR.bat`
5. Esperar 2 a 3 minutos hasta completar
6. Los .bat se copiarán automáticamente al Escritorio

---

## 🧩 Configuración

### 1️⃣ Instalación inicial

Ejecutar:

```
INSTALAR.bat
```

### 2️⃣ Configuración del bot

Ejecutar:

```
EJECUTAR_BOT.bat
```

En la interfaz gráfica:

* Abrir la pestaña "Ajustes"
* Registrar credenciales
* Guardar

### 3️⃣ Ejecución

En la pestaña "Ejecutar":

```
INICIAR DESCARGA AUTOMÁTICA 🚀
```

---

## 📁 Ubicación de los archivos descargados

```
C:\Users\NOMBRE_USUARIO\Downloads
```

---

## ⚙️ Archivos del Proyecto

| Archivo                      | Función                  | Modificación     |
| ---------------------------- | ------------------------ | ---------------- |
| `INSTALAR.bat`               | Instalación automática   | Solo ejecutar    |
| `EJECUTAR_BOT.bat`           | Inicia el bot            | Uso diario       |
| `LEEME.txt`                  | Guía completa            | Lectura opcional |
| `CREAR_PAQUETE_PORTABLE.bat` | Genera versión portable  | Opcional         |
| `index.py`                   | Lógica principal del bot | No modificar     |
| `gui.py`                     | Interfaz gráfica         | No modificar     |

---

## 🎯 Personalización de búsqueda

### Método 1: Interfaz gráfica

1. Abrir `EJECUTAR_BOT.bat`
2. Ir a "Términos"
3. Agregar o modificar términos
4. Guardar

### Método 2: Edición directa de archivo

1. Abrir la carpeta `config`
2. Editar `terms.json`

Ejemplo:

```json
{
  "lista_busqueda": [
    "Migracion de plan",
    "Guia de cuestionamiento",
    "Bloqueo de linea"
  ]
}
```

---

## 🆘 Problemas Comunes

### ❌ Python no encontrado

1. El instalador intentará descargarlo automáticamente
2. Si falla:

   * Descargar Python desde [https://www.python.org/downloads/](https://www.python.org/downloads/)
   * Activar "Add Python to PATH"
   * Ejecutar nuevamente `INSTALAR.bat`

### ❌ Error instalando dependencias

1. Cerrar todos los programas
2. Ejecutar otra vez `INSTALAR.bat`
3. Reiniciar el equipo si persiste

### ❌ No se puede acceder al portal

* Revisar conexión a internet
* Verificar credenciales en la pestaña "Ajustes"
* Comprobar acceso manual al portal

### ❌ El bot se detiene

* Esta versión ya corrige las pausas interactivas
* Si ocurre, cerrar todo y volver a ejecutar

---

## 📦 Formas de compartir

### Método 1: Compartir el repositorio

Link directo: [https://github.com/ChampiP/bot-rpa](https://github.com/ChampiP/bot-rpa)

### Método 2: Instalación automática

Ejecutar en PowerShell:

```powershell
irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
```

### Método 3: Paquete portable

1. Ejecutar `CREAR_PAQUETE_PORTABLE.bat`
2. Se generará la carpeta `BOT_RPA_CLARO_PORTABLE`
3. Compartir la carpeta
4. Ejecutar `INSTALAR.bat`

**Nota:** la carpeta `.venv` no debe compartirse.

---

## 🔒 Seguridad

* El bot solo interactúa con el portal de Claro
* No envía datos a servicios externos
* Las credenciales se almacenan localmente
* El código es completamente abierto

---

## 💡 Recomendaciones

* Cerrar completamente Chrome antes de ejecutar
* No cerrar el navegador que abre el bot
* El bot intentará recuperarse ante errores
* Algunos diagramas pueden ser pesados
* El procesamiento se realiza término por término

---

## 📊 Características

* Interfaz gráfica intuitiva
* Instalación automática de dependencias
* Desbloqueo automático de archivos Excel
* Sistema de scoring para mayor precisión
* Manejo automático de errores
* Registros claros
* Totalmente portable

---

## 📝 Versión

**Versión:** 2.3  
**Fecha:** Noviembre 2025

**Mejoras:**

* Salida más limpia y ordenada
* Reducción del tiempo de espera (40%)
* Eliminación de pausas interactivas
* Mejor versión portable
* Interfaz gráfica más clara

---

## 🎉 Gracias por usar este proyecto

Para soporte adicional, revisar:

* `LEEME.txt`
* La sección de Problemas Comunes
* Reinstalar si es necesario



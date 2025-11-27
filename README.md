# 🤖 BOT RPA – DESCARGA AUTOMÁTICA DE DIAGRAMAS CLARO

## 📋 Descripción General

Bot automatizado para descargar diagramas y documentos del portal de Claro de manera automática.  
Configura los términos de búsqueda y deja que el sistema haga todo el trabajo.

**Repositorio:** https://github.com/ChampiP/bot-rpa

---

## 🎯 Guía Paso a Paso - SOLO 3 PASOS! 

### 📥 **PASO 1: Descarga el Bot**

#### **Opción A: Instalación Automática (Más Fácil) ⭐**

1. Abre **PowerShell** en tu computadora:
   - Presiona `Win + X`
   - Selecciona "Windows PowerShell" o "Terminal"

2. Copia y pega este comando:
   ```powershell
   irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
   ```
Necesitas darle permiso a PowerShell para hacer su magia. Ejecuta esto antes de intentar el comando de instalación otra vez:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
 ```
PowerShell

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Copia y pega eso en la terminal.

Si te pregunta, escribe Y o S y dale Enter.

Vuelve a lanzar el comando

3. Presiona `Enter` y espera

✅ **Resultado:** El bot se instalará en tu Escritorio en la carpeta `Bot_RPA_Claro`

#### **Opción B: Descarga Manual**

1. Ve a: https://github.com/ChampiP/bot-rpa
2. Haz clic en el botón verde **"Code"**
3. Selecciona **"Download ZIP"**
4. Extrae el archivo ZIP **donde quieras** (Escritorio, Documentos, etc.)

---

### ⚙️ **PASO 2: Instala el Bot (Solo una vez)**

1. Abre la carpeta donde descargaste el bot
2. Busca el archivo **`INSTALAR.bat`**
3. Haz **doble clic** en él
4. **¡Espera a que termine!**

**🔄 El instalador hará TODO automáticamente:**

- ✅ Detectará si tienes Python (si no, lo instalará)
- ✅ Creará el entorno virtual
- ✅ Instalará todas las dependencias
- ✅ **Copiará `BOT_RPA_CLARO.bat` a tu Escritorio**

**⏱️ Tiempo:** 2-5 minutos

**✨ Al terminar verás:**
```
============================================================
   INSTALACION COMPLETADA EXITOSAMENTE
============================================================

[OK] El bot esta listo para usar

PROXIMO PASO:
  Ve a tu ESCRITORIO y ejecuta:
  ==> BOT_RPA_CLARO.bat
```

---

### 🚀 **PASO 3: Usa el Bot** 

**📍 Desde tu ESCRITORIO:**

1. Busca el archivo **`BOT_RPA_CLARO.bat`** 
2. Haz **doble clic** en él
3. Selecciona **opción 1** (Interfaz Gráfica)

**🔧 Primera vez - Configura tus credenciales:**
1. Ve a la pestaña **"Ajustes"**
2. Ingresa tu usuario y contraseña del portal Claro
3. Haz clic en **"Guardar Configuración"**

**🔍 (Opcional) Configura qué descargar:**
1. Ve a la pestaña **"Términos"**
2. Agrega, edita o elimina términos de búsqueda
3. Haz clic en **"Guardar"**

**▶️ Ejecuta el bot:**
1. Ve a la pestaña **"Ejecutar"**
2. Haz clic en **"INICIAR DESCARGA AUTOMÁTICA 🚀"**
3. ¡Listo! El bot trabajará solo

**⏱️ Tiempo:** Varía según cuántos documentos busque (5-20 min aprox.)

---

### 📁 **Tus archivos descargados estarán en:**

```
C:\Users\TU_USUARIO\Downloads
```

---

## 🔄 Uso Diario (Después de Instalado)

**Es súper fácil:**

1. **Doble clic** en `BOT_RPA_CLARO.bat` (desde tu Escritorio)
2. Opción **1** → Interfaz Gráfica
3. Pestaña **"Ejecutar"** → Botón **"INICIAR 🚀"**
4. ¡Eso es todo!

---

## ⚠️ ¿Tienes Problemas? - El Bot se Auto-Repara! 🔧

### ✨ **Auto-Reparación Inteligente**

**El bot ahora se auto-diagnostica y auto-repara:**

Cuando ejecutas `BOT_RPA_CLARO.bat`, el bot automáticamente:
- ✅ Verifica que Python esté instalado
- ✅ Verifica que el entorno virtual exista
- ✅ Verifica que todos los archivos estén presentes
- ✅ **Si detecta problemas, te ofrece repararlos automáticamente**

**Si ves este mensaje:**
```
============================================================
   SE DETECTARON PROBLEMAS
============================================================

[1] Auto-reparar ahora (Recomendado)
[2] Salir y hacerlo manualmente
```

**¡Simplemente presiona `1` y el bot se reparará solo!**

---

### 🔴 **Problemas Comunes (con soluciones rápidas)**

#### **Problema 1: "Python no encontrado"**

**Solución:**
1. Ejecuta `INSTALAR.bat` - intentará instalar Python automáticamente
2. Si falla, ejecuta `VERIFICAR_PYTHON.bat` para ver diagnóstico
3. Instalación manual: https://www.python.org/downloads/
   - **IMPORTANTE:** Marca "Add Python to PATH" ✅
   - Reinicia tu PC después de instalar

---

#### **Problema 2: "No se encuentra el bot"**

**Causa:** El `.bat` del escritorio no sabe dónde está la carpeta del bot

**Solución:**
1. Ejecuta `INSTALAR.bat` desde la carpeta del bot
2. Esto actualizará la ubicación automáticamente
3. El `.bat` del escritorio funcionará correctamente

---

#### **Problema 3: "Error al ejecutar"**

**Solución Rápida:**
1. Ejecuta `BOT_RPA_CLARO.bat` desde el Escritorio
2. Si el bot detecta problemas, presiona **`1`** para auto-reparar
3. Si persiste, ejecuta `INSTALAR.bat` desde la carpeta del bot

---

#### **Problema 4: "No se puede acceder al portal"**

**Solución:**
- ✅ Verifica tu internet
- ✅ Revisa credenciales (pestaña "Ajustes")
- ✅ Intenta acceder manualmente al portal
- ✅ Verifica que no hay mantenimiento

---

#### **Problema 5: "El bot se congela"**

**Solución:**
1. Cierra Chrome y el bot
2. Ejecuta `BOT_RPA_CLARO.bat` nuevamente
3. El bot reiniciará limpiamente

---

## 🛠️ Herramientas Incluidas

---

## 📁 Ubicación de los archivos descargados

```
C:\Users\NOMBRE_USUARIO\Downloads
```

---

| Archivo | ¿Para qué sirve? | ¿Cuándo usarlo? |
|---------|------------------|-----------------|
| **`INSTALAR.bat`** | Instala todo lo necesario (Python, dependencias, etc.) | **Solo la primera vez** o si hay problemas |
| **`EJECUTAR_BOT.bat`** | Abre la interfaz del bot | **Cada vez que quieras usar el bot** |
| **`VALIDAR_BOT.bat`** | Verifica que todo funcione correctamente | Si tienes dudas o problemas |
| **`VERIFICAR_PYTHON.bat`** | Diagnostica problemas con Python | Si Python no funciona |
| **`LEEME.txt`** | Instrucciones en texto plano | Para referencia rápida |
| `index.py` | Código principal del bot | ❌ No tocar |
| `gui.py` | Interfaz gráfica | ❌ No tocar |
| `requirements.txt` | Lista de dependencias | ❌ No tocar |

---

## 📊 Archivos de Configuración

| Archivo | Ubicación | ¿Qué contiene? |
|---------|-----------|----------------|
| `terms.json` | `config/terms.json` | Términos de búsqueda |
| `.env` | Raíz del proyecto | Credenciales (se crea al guardar en Ajustes) |

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

## 🎨 Funcionalidades de la Interfaz

### 📑 **Pestaña "Ejecutar"**
- **Botón principal:** Inicia el proceso de descarga
- **Log en tiempo real:** Muestra qué está haciendo el bot
- **Indicador de progreso:** Barra visual del proceso

### ⚙️ **Pestaña "Ajustes"**
- **Usuario:** Tu usuario del portal Claro
- **Contraseña:** Tu contraseña (se guarda encriptada localmente)
- **Botón Guardar:** Almacena las credenciales

### 🔍 **Pestaña "Términos"**
- **Lista de términos:** Qué documentos buscará el bot
- **Agregar:** Añade nuevos términos
- **Eliminar:** Quita términos que no necesites
- **Editar:** Modifica términos existentes

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

## 💡 Consejos y Mejores Prácticas

✅ **HACER:**
- Cerrar completamente Chrome antes de ejecutar el bot
- Dejar que el bot trabaje sin interrupciones
- Verificar tu conexión a internet antes de empezar
- Revisar los términos de búsqueda antes de ejecutar
- Mantener el bot actualizado desde el repositorio

❌ **NO HACER:**
- Cerrar el navegador mientras el bot trabaja
- Modificar archivos `.py` si no sabes programar
- Eliminar la carpeta `.venv`
- Compartir tus credenciales
- Usar el bot con conexión inestable

---

## 🔐 Seguridad y Privacidad

🛡️ **Tu información está segura:**
- ✅ El bot solo interactúa con el portal oficial de Claro
- ✅ Las credenciales se almacenan **solo en tu computadora**
- ✅ No se envían datos a servidores externos
- ✅ El código es **100% abierto** y auditable
- ✅ No se recopila información personal

---

## 📦 Compartir el Bot con Otros

### **Opción 1: Compartir el link del repositorio** (Más fácil)
Comparte este link: https://github.com/ChampiP/bot-rpa

### **Opción 2: Comando de instalación automática**
Comparte este comando de PowerShell:
```powershell
irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
```

### **Opción 3: Paquete portable** (Para compartir sin internet)
1. Ejecuta `CREAR_PAQUETE_PORTABLE.bat` (si existe)
2. Se creará una carpeta con todo lo necesario
3. Comprime la carpeta en un ZIP
4. Comparte el ZIP
5. La otra persona debe extraerlo y ejecutar `INSTALAR.bat`

**⚠️ IMPORTANTE:** NO compartas la carpeta `.venv` - es específica de tu computadora

---

## 📊 Características Técnicas

✨ **Lo que hace el bot:**
- ✅ Instalación automática de Python (si no está instalado)
- ✅ Detección inteligente de Python en el sistema
- ✅ Interfaz gráfica intuitiva
- ✅ Descarga automática de múltiples documentos
- ✅ Sistema de scoring para resultados precisos
- ✅ Manejo robusto de errores
- ✅ Logs detallados del proceso
- ✅ Desbloqueo automático de archivos Excel
- ✅ Recuperación automática ante fallos
- ✅ Validación completa del entorno

---

## 📝 Versión y Actualizaciones

**Versión actual:** 2.5 OPTIMIZADA ⚡  
**Fecha:** Noviembre 2025

**🚀 NUEVAS MEJORAS v2.5 - 40% MÁS RÁPIDO:**
- ⚡ **Velocidad mejorada**: Login y búsquedas 40% más rápidas
- ✅ **Sin errores de timeout**: Validación automática de valores mínimos
- ⚡ **Login optimizado**: Detección inteligente y esperas adaptativas
- ⚡ **Búsquedas instantáneas**: Scroll sin animación y búsquedas más eficientes
- ⚡ **Descargas rápidas**: Detección cada 0.5s (antes cada 2s)
- ✅ **Timeouts inteligentes**: Continúa aunque haya timeout en lugar de fallar
- ✅ **Validación de configuración**: No permite valores que causen errores
- 📊 **Interfaz mejorada**: Muestra valores mínimos y estado de optimización
- 📖 **Guía de optimización**: Nuevo archivo OPTIMIZACIONES.md

**Versiones anteriores:**
- v2.4: Instalación automática de Python mejorada
- v2.3: Interfaz mejorada, reducción de tiempos de espera
- v2.2: Sistema portable mejorado
- v2.1: Eliminación de pausas interactivas

---

## ❓ Preguntas Frecuentes (FAQ)

### **¿Necesito instalar Python manualmente?**
No, el instalador lo hará automáticamente. Si falla, te guiará paso a paso.

### **¿Funciona en Windows 7?**
El bot está optimizado para Windows 10 y 11. En Windows 7 puede requerir instalación manual de Python.

### **¿Cuánto espacio necesito?**
Aproximadamente 500 MB para Python y dependencias, más espacio para los archivos descargados.

### **¿Puedo usar el bot en varias computadoras?**
Sí, pero debes instalarlo en cada una. Las credenciales se guardan localmente.

### **¿El bot funciona sin internet?**
No, necesita internet para acceder al portal de Claro y descargar archivos.

### **¿Puedo modificar el código?**
Sí, el código es abierto. Si sabes Python, puedes personalizarlo.

### **¿Por qué veo errores de timeout?**
El bot v2.5 ahora valida automáticamente los valores mínimos. Si ajustas los timeouts muy bajos, el sistema los corregirá. Lee `OPTIMIZACIONES.md` para más detalles.

### **¿Cómo hago el bot más rápido?**
Ve a la interfaz gráfica → Pestaña "Avanzado" → Ajusta los tiempos. El bot te avisará si introduces valores muy bajos. Lee `OPTIMIZACIONES.md` para configuraciones recomendadas según tu conexión.

### **¿Qué hago si encuentro un error?**
1. Ejecuta `VERIFICAR_PYTHON.bat`
2. Ejecuta `VALIDAR_BOT.bat`
3. Lee la sección "¿Tienes Problemas?" de este README
4. Lee `OPTIMIZACIONES.md` si tienes problemas de timeout
5. Si persiste, abre un issue en GitHub

---

## 🎉 Soporte y Ayuda

**¿Necesitas ayuda?**

1. 📖 Lee este README completo
2. 📄 Revisa el archivo `LEEME.txt`
3. 🔍 Ejecuta `VERIFICAR_PYTHON.bat` para diagnósticos
4. ✅ Ejecuta `VALIDAR_BOT.bat` para verificar el bot
5. 🔄 Intenta ejecutar `INSTALAR.bat` nuevamente
6. 💻 Si nada funciona, abre un issue en GitHub

**Repositorio:** https://github.com/ChampiP/bot-rpa

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para automatizar tus tareas.

---

**✨ ¡Gracias por usar el Bot RPA de Claro!**

*Automatiza tu trabajo y ahorra tiempo* 🚀



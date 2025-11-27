# 🤖 BOT RPA – DESCARGA AUTOMÁTICA DE DIAGRAMAS CLARO

## 📋 Descripción General

Bot automatizado para descargar diagramas y documentos del portal de Claro de manera automática.  
Configura los términos de búsqueda y deja que el sistema haga todo el trabajo.

**Repositorio:** https://github.com/ChampiP/bot-rpa

---

## 🎯 Guía Paso a Paso (Para Usuarios)

### 📥 **PASO 1: Descarga el Bot**

#### **Opción A: Instalación Automática (Más Fácil) ⭐**

1. Abre **PowerShell** en tu computadora:
   - Presiona `Win + X`
   - Selecciona "Windows PowerShell" o "Terminal"

2. Copia y pega este comando:
   ```powershell
   irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
   ```

3. Presiona `Enter` y espera

✅ **Resultado:** El bot se instalará en tu Escritorio en la carpeta `Bot_RPA_Claro`

#### **Opción B: Descarga Manual**

1. Ve a: https://github.com/ChampiP/bot-rpa
2. Haz clic en el botón verde **"Code"**
3. Selecciona **"Download ZIP"**
4. Extrae el archivo ZIP **en tu Escritorio**
5. Continúa al Paso 2

---

### ⚙️ **PASO 2: Instala el Bot (Primera Vez Solamente)**

1. Ve a tu **Escritorio (Desktop)**
2. Abre la carpeta `bot-rpa` (o `Bot_RPA_Claro`)
3. Busca el archivo **`INSTALAR.bat`**
4. Haz **doble clic** en él

**🔄 ¿Qué hará el instalador?**

- ✅ Verificará si tienes **Python** instalado
- ✅ Si NO tienes Python, lo instalará automáticamente
- ✅ Creará un entorno virtual
- ✅ Instalará todas las dependencias necesarias
- ✅ Copiará accesos directos a tu Escritorio

**⏱️ Tiempo aproximado:** 2-5 minutos

**⚠️ IMPORTANTE:** 
- Si Python no está instalado, el script lo instalará con **winget**
- Si la instalación automática falla, recibirás instrucciones claras
- Es posible que necesites **reiniciar el instalador** después de instalar Python

---

### 🔧 **PASO 3: Verifica que Todo Funcione (Opcional pero Recomendado)**

1. Ve a tu **Escritorio**
2. Busca el archivo **`VERIFICAR_PYTHON.bat`** (si lo copiaste)
   - O ejecútalo desde la carpeta del bot
3. Haz **doble clic** en él

**📊 Este script te mostrará:**
- ✅ Si Python está instalado correctamente
- ✅ Qué comandos de Python funcionan
- ✅ Si hay problemas con el PATH
- ✅ Recomendaciones específicas para tu caso

**Si todo está OK:** Continúa al Paso 4  
**Si hay problemas:** Sigue las recomendaciones que muestra el script

---

### 🎮 **PASO 4: Configura tus Credenciales**

1. Ve a tu **Escritorio**
2. Busca el archivo **`EJECUTAR_BOT.bat`**
3. Haz **doble clic** en él
4. Se abrirá una **ventana con pestañas**

**📝 En la pestaña "Ajustes":**
1. Ingresa tu **Usuario** del portal Claro
2. Ingresa tu **Contraseña**
3. Haz clic en **"Guardar Configuración"**

✅ **Listo:** Tus credenciales están guardadas (solo en tu computadora)

---

### 🔍 **PASO 5: Configura los Términos de Búsqueda (Opcional)**

**🎯 ¿Qué quieres descargar?**

**Opción 1: Desde la Interfaz Gráfica**
1. En la ventana del bot, ve a la pestaña **"Términos"**
2. Verás una lista de términos de búsqueda
3. Agrega, edita o elimina términos
4. Haz clic en **"Guardar"**

**Opción 2: Editando el Archivo**
1. Ve a la carpeta `config`
2. Abre el archivo `terms.json` con el Bloc de notas
3. Edita los términos siguiendo este formato:
   ```json
   {
     "lista_busqueda": [
       "Migracion de plan",
       "Guia de cuestionamiento",
       "Bloqueo de linea"
     ]
   }
   ```
4. Guarda el archivo

---

### 🚀 **PASO 6: Ejecuta el Bot**

1. En la ventana del bot, ve a la pestaña **"Ejecutar"**
2. Haz clic en **"INICIAR DESCARGA AUTOMÁTICA 🚀"**
3. Se abrirá un navegador Chrome automáticamente
4. **NO CIERRES EL NAVEGADOR** mientras el bot trabaja

**🤖 El bot hará automáticamente:**
- Iniciará sesión con tus credenciales
- Buscará cada término que configuraste
- Descargará los diagramas encontrados
- Cerrará el navegador al terminar

**⏱️ Tiempo:** Depende de cuántos términos y archivos haya (5-20 minutos aprox.)

---

### 📁 **PASO 7: Revisa tus Archivos Descargados**

Los archivos se guardan en:
```
C:\Users\TU_USUARIO\Downloads
```

O simplemente abre tu carpeta de **Descargas**

---

## ⚠️ ¿Tienes Problemas? Soluciones Rápidas

### 🔴 **Problema 1: "Python no encontrado"**

**Solución Automática:**
- El instalador intentará instalar Python automáticamente
- Si falla, verás instrucciones claras en pantalla

**Solución Manual:**
1. Ve a: https://www.python.org/downloads/
2. Descarga **Python 3.11** o superior
3. Durante la instalación, **MARCA LA CASILLA "Add Python to PATH"** ✅
4. Completa la instalación
5. **Reinicia tu computadora**
6. Ejecuta `INSTALAR.bat` nuevamente

**Verificación:**
- Ejecuta `VERIFICAR_PYTHON.bat` para confirmar que Python funciona

---

### 🔴 **Problema 2: "Error instalando dependencias"**

**Solución:**
1. Cierra todas las ventanas del bot
2. Ejecuta `INSTALAR.bat` nuevamente
3. Si persiste, reinicia tu computadora
4. Ejecuta `INSTALAR.bat` una vez más

---

### 🔴 **Problema 3: "No se puede acceder al portal"**

**Solución:**
1. Verifica tu **conexión a internet**
2. Revisa tus **credenciales** en la pestaña "Ajustes"
3. Intenta acceder manualmente al portal desde tu navegador
4. Verifica que no hay mantenimiento en el portal

---

### 🔴 **Problema 4: "El bot se detiene o congela"**

**Solución:**
1. Cierra el navegador Chrome
2. Cierra la ventana del bot
3. Ejecuta `EJECUTAR_BOT.bat` nuevamente
4. Si persiste, reinicia tu computadora

---

### 🔴 **Problema 5: "Entorno virtual no configurado"**

**Solución:**
1. Ejecuta `INSTALAR.bat` nuevamente
2. Espera a que termine completamente
3. Si ves errores, anótalos y ejecuta `VERIFICAR_PYTHON.bat`

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

## 🔄 Uso Diario (Después de Instalado)

**¿Cada vez que quieras usar el bot?**

1. **Doble clic** en `EJECUTAR_BOT.bat` (desde el Escritorio)
2. Selecciona **opción 1** (Interfaz Gráfica)
3. Ve a la pestaña **"Ejecutar"**
4. Haz clic en **"INICIAR DESCARGA AUTOMÁTICA 🚀"**
5. ¡Listo! El bot trabajará solo

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

**Versión actual:** 2.4  
**Fecha:** Noviembre 2025

**🆕 Mejoras en esta versión:**
- ✅ **Instalación automática de Python** mejorada
- ✅ Detección múltiple de Python (python, py, python3)
- ✅ Script de diagnóstico `VERIFICAR_PYTHON.bat`
- ✅ Mejor manejo de errores en la instalación
- ✅ Actualización automática del PATH
- ✅ Instrucciones más claras para usuarios
- ✅ Validaciones robustas en todos los scripts
- ✅ Mejor experiencia de usuario

**Versiones anteriores:**
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

### **¿Qué hago si encuentro un error?**
1. Ejecuta `VERIFICAR_PYTHON.bat`
2. Ejecuta `VALIDAR_BOT.bat`
3. Lee la sección "¿Tienes Problemas?" de este README
4. Si persiste, abre un issue en GitHub

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



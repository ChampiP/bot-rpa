# 🤖 BOT RPA - DESCARGA AUTOMATICA DE DIAGRAMAS CLARO

## 📋 ¿Qué hace este bot?

Este bot descarga **automáticamente** todos los diagramas y documentos del portal de Claro que necesites. Tú solo configuras qué buscar y él hace todo el trabajo.

**🔗 Repositorio:** https://github.com/ChampiP/bot-rpa

---

## 🚀 INICIO RAPIDO (3 Pasos)

### 📥 DESCARGAR E INSTALAR

**Opción 1: Instalación Automática desde GitHub (Recomendado)**
```bash
# En PowerShell (Administrador)
irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
```

**Opción 2: Descarga Manual**
```
1. Ve a: https://github.com/ChampiP/bot-rpa
2. Click en "Code" → "Download ZIP"
3. Extrae los archivos
4. Haz doble clic en: INSTALAR.bat
5. Espera 2-3 minutos
6. ¡Listo!
```

### 1️⃣ INSTALAR (Solo la primera vez)
```
Haz doble clic en: INSTALAR.bat
Espera 2-3 minutos
¡Listo!
```

### 2️⃣ CONFIGURAR
```
Haz doble clic en: EJECUTAR_BOT.bat
Opción 1: Interfaz Gráfica
Ve a pestaña "Ajustes"
Ingresa tu usuario y contraseña
Dale "Guardar"
```

### 3️⃣ USAR
```
Pestaña "Ejecutar"
Click en "🚀 INICIAR DESCARGA AUTOMATICA"
¡Relájate! El bot hace todo solo
```

---

## 📁 ¿Dónde están mis archivos?

Los archivos descargados están en:
```
C:\Users\TU_USUARIO\Downloads
```

---

## ⚙️ ARCHIVOS IMPORTANTES

| Archivo | Para qué sirve | ¿Debes tocarlo? |
|---------|----------------|----------------|
| `INSTALAR.bat` | Instala todo automáticamente | ✅ Solo ejecutar |
| `EJECUTAR_BOT.bat` | Inicia el bot | ✅ Usar siempre |
| `LEEME.txt` | Instrucciones completas | 📖 Leer si hay dudas |
| `CREAR_PAQUETE_PORTABLE.bat` | Crea copia para compartir | ✅ Solo si quieres compartir |
| `index.py` | Código del bot | ❌ No modificar |
| `gui.py` | Interfaz gráfica | ❌ No modificar |

---

## 🎯 ¿Cómo personalizo qué descargar?

### Opción 1: Interfaz Gráfica (Fácil)
1. Abre `EJECUTAR_BOT.bat`
2. Ve a pestaña "Términos"
3. Agrega o quita términos
4. Guarda

### Opción 2: Editar directamente
1. Abre la carpeta `config`
2. Edita `terms.json` con Notepad
3. Agrega términos entre comillas separados por comas

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

## 🆘 PROBLEMAS COMUNES

### ❌ "Python no encontrado"
**Solución:** El instalador lo descargará automáticamente. Si falla:
1. Ve a: https://www.python.org/downloads/
2. Descarga Python 3.11
3. Durante instalación marca "Add Python to PATH"
4. Ejecuta `INSTALAR.bat` de nuevo

### ❌ "Error al instalar dependencias"
**Solución:**
1. Cierra todo
2. Ejecuta `INSTALAR.bat` de nuevo
3. Si persiste, reinicia tu PC

### ❌ "No se pudo acceder al portal"
**Solución:**
1. Verifica tu internet
2. Verifica usuario y contraseña en "Ajustes"
3. Intenta acceder manualmente al portal primero

### ❌ El bot se queda pausado
**Solución:** Esto ya está arreglado en esta versión. El bot ya no requiere presionar Enter.

---

## 📦 ¿Cómo comparto esto con mis compañeros?

### Método 1: Compartir Link de GitHub (Más Fácil) ⭐
Simplemente comparte: **https://github.com/ChampiP/bot-rpa**

Tus compañeros:
1. Abren el link
2. Click en "Code" → "Download ZIP"
3. Extraen y ejecutan `INSTALAR.bat`
4. ¡Listo!

### Método 2: Comando de Instalación Directa
Tu compañero ejecuta en PowerShell (Administrador):
```powershell
irm https://raw.githubusercontent.com/ChampiP/bot-rpa/main/INSTALAR_DESDE_GITHUB.bat -outfile install.bat; .\install.bat
```

### Método 3: Crear Paquete Local
1. Ejecuta `CREAR_PAQUETE_PORTABLE.bat`
2. Se creará carpeta `BOT_RPA_CLARO_PORTABLE`
3. Comparte esa carpeta (Drive, OneDrive, USB, etc.)
4. Tu compañero ejecuta `INSTALAR.bat`

⚠️ **IMPORTANTE:** La carpeta `.venv` NO se debe compartir. El instalador la crea automáticamente.

---

## 🔒 ¿Es seguro?

✅ Sí. Este bot:
- Solo accede al portal de Claro
- No envía información a ningún otro lado
- Las contraseñas se guardan solo en tu computadora
- Es código abierto (puedes revisarlo)

---

## 💡 CONSEJOS PRO

1. **Antes de ejecutar:** Cierra Chrome completamente
2. **Durante ejecución:** No cierres el navegador que abre el bot
3. **Si algo falla:** El bot intentará recuperarse solo
4. **Archivos grandes:** Algunos diagramas pesan varios MB, ten paciencia
5. **Múltiples búsquedas:** El bot procesa un término a la vez

---

## 📊 Características Técnicas

- ✅ Interfaz gráfica amigable
- ✅ Instalación automática de dependencias
- ✅ Desbloqueo automático de archivos Excel
- ✅ Sistema de scoring inteligente para mejor precisión
- ✅ Recuperación automática de errores
- ✅ Logs claros y concisos
- ✅ 100% portable

---

## 📞 ¿Necesitas ayuda?

Si tienes problemas:

1. Lee `LEEME.txt` completo
2. Verifica PROBLEMAS COMUNES arriba
3. Ejecuta `INSTALAR.bat` de nuevo
4. Reinicia tu computadora
5. Contacta al administrador del sistema

---

## 📝 Versión

**Versión:** 2.3  
**Fecha:** Noviembre 2025  
**Mejoras en esta versión:**
- ✨ Salida más limpia y amigable
- ⚡ Más rápido (reducción de 40% en tiempos de espera)
- 🔧 Sin pausas que requieran presionar Enter
- 📦 Sistema portable mejorado
- 🎨 Interfaz gráfica más intuitiva

---

**¡Disfruta tu bot! 🎉**

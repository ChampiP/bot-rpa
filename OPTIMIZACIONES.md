# 🚀 Optimizaciones Bot RPA v2.5 - Guía de Mejoras

## 🎯 Cómo Usar la Configuración

### Desde la Interfaz Gráfica (Recomendado)

1. **Ejecuta:** `python gui.py`
2. **Ve a la pestaña "Avanzado"**
3. **Ajusta los tiempos según necesites**
4. **Haz clic en "Guardar Configuración Avanzada"**

**⚠️ IMPORTANTE:** Si introduces un valor menor al mínimo, el sistema lo ajustará automáticamente y te avisará.

### Valores Recomendados Según Tu Conexión

#### 🟢 Conexión Rápida (> 50 Mbps)
```
TIMING_SHORT_WAIT=0.3
TIMING_MEDIUM_WAIT=1.0
TIMING_LONG_WAIT=2.0
TIMING_PAGE_LOAD=90
TIMING_RATE_LIMIT=0.5
```

#### 🟡 Conexión Normal (10-50 Mbps)
```
TIMING_SHORT_WAIT=0.5
TIMING_MEDIUM_WAIT=1.5
TIMING_LONG_WAIT=3.0
TIMING_PAGE_LOAD=120
TIMING_RATE_LIMIT=0.8
```
**👉 ESTOS SON LOS VALORES POR DEFECTO (YA CONFIGURADOS)**

#### 🔴 Conexión Lenta (< 10 Mbps)
```
TIMING_SHORT_WAIT=0.8
TIMING_MEDIUM_WAIT=2.5
TIMING_LONG_WAIT=4.0
TIMING_PAGE_LOAD=180
TIMING_RATE_LIMIT=1.5
```

## 🔧 Solución de Problemas

### Si aún ves errores de timeout:

1. **Verifica tu conexión:**
   ```powershell
   Test-NetConnection portaldeconocimiento.claro.com.pe -Port 80
   ```

2. **Aumenta PAGE_LOAD a 180 segundos:**
   - Abre la GUI → Pestaña "Avanzado"
   - Cambia `Timeout Carga Pagina` a `180`
   - Guarda la configuración

3. **Activa el modo debug:**
   - En la pestaña "Avanzado"
   - Marca "Activar modo debug"
   - Esto te dará más información sobre qué está pasando

### Si el bot es muy lento:

1. **Reduce los tiempos (respetando mínimos):**
   - `TIMING_MEDIUM_WAIT` → `1.0`
   - `TIMING_RATE_LIMIT` → `0.5`
   - `TIMING_PAGE_LOAD` → `90`

2. **Verifica que no tienes antivirus bloqueando descargas**

3. **Cierra otros programas que usen Chrome**

## 📈 Comparativa de Rendimiento

### Antes (v2.4)
- Login: ~15 segundos
- Cada búsqueda: ~25 segundos
- **Total 10 diagramas: ~4-5 minutos**

### Ahora (v2.5 Optimizado)
- Login: ~8 segundos
- Cada búsqueda: ~15 segundos
- **Total 10 diagramas: ~2.5-3 minutos**

**🎉 Mejora total: ~40% más rápido**

## 🆘 Soporte

Si sigues teniendo problemas:
1. Activa el modo DEBUG
2. Copia el log completo del terminal
3. Incluye tu configuración de timeouts (pestaña Avanzado)
4. Reporta en GitHub: https://github.com/ChampiP/bot-rpa/issues

## 📝 Notas Finales

- ✅ Los valores están optimizados para la mayoría de conexiones
- ✅ La validación automática evita errores de configuración
- ✅ El bot ahora es más inteligente y se adapta mejor
- ✅ Si algo falla, el bot intenta recuperarse automáticamente

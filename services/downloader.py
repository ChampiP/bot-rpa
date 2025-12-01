"""
CoorpiBot - Servicio de Descarga
Gestión de descargas de archivos
"""
import os
import time
from selenium.common.exceptions import ElementClickInterceptedException


class DownloadManager:
    """Gestor de descargas"""
    
    def __init__(self, driver, dirs, unlocker, timings):
        self.driver = driver
        self.dirs = dirs
        self.unlocker = unlocker
        self.timings = timings
    
    def click_download(self, element):
        """Hacer click en elemento para descargar"""
        # Scroll al elemento
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", 
            element
        )
        
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
    
    def wait_for_download(self, snapshot_antes, timeout=None):
        """Esperar a que se complete la descarga"""
        if timeout is None:
            timeout = self.timings.download_timeout
            
        tiempo_inicio = time.time()
        archivo_final = None
        check_interval = 0.5
        
        while (time.time() - tiempo_inicio) < timeout:
            try:
                snapshot_ahora = self.dirs.get_files_snapshot()
                nuevos = set(snapshot_ahora.keys()) - set(snapshot_antes.keys())
                actualizados = []
                
                for filename, mtime in snapshot_ahora.items():
                    if filename in snapshot_antes:
                        if mtime > snapshot_antes[filename] + 0.5:
                            actualizados.append(filename)
                
                candidatos = list(nuevos) + actualizados
                candidato = next(
                    (f for f in candidatos if not f.endswith(('.crdownload', '.tmp', '.partial'))), 
                    None
                )
                
                if candidato:
                    archivo_final = os.path.join(self.dirs.download_dir, candidato)
                    size_prev = -1
                    
                    for i in range(3):
                        try:
                            size_curr = os.path.getsize(archivo_final)
                            if size_curr == size_prev and size_curr > 0:
                                return archivo_final
                            size_prev = size_curr
                            time.sleep(self.timings.short_wait)
                        except OSError:
                            if i == 2:
                                return archivo_final if os.path.exists(archivo_final) else None
                    
                    return archivo_final
            except OSError:
                pass
            
            time.sleep(check_interval)
        
        return archivo_final
    
    def process_download(self, element, info):
        """Procesar descarga completa de un elemento"""
        snapshot_antes = self.dirs.get_files_snapshot()
        
        titulo_corto = info.get('titulo', 'N/A')[:70]
        if len(info.get('titulo', '')) > 70:
            titulo_corto += '...'
        print(f"[>>] Seleccionado: {titulo_corto}")
        
        self.click_download(element)
        
        archivo_final = self.wait_for_download(snapshot_antes)
        
        if archivo_final and os.path.exists(archivo_final):
            self.unlocker.unblock_file(archivo_final)
            archivo_nombre = os.path.basename(archivo_final)
            if len(archivo_nombre) > 60:
                archivo_nombre = archivo_nombre[:57] + '...'
            print(f"[✓] Descargado: {archivo_nombre}\n")
            return True
        else:
            print(f"[!] Error en descarga\n")
            return False

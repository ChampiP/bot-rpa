"""
CoorpiBot - Bot Principal
Orquestador del proceso de descarga automática
"""
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException

from core import ConfigLoader
from services import ChromeConfigurator, SearchEngine, DownloadManager, AuthService
from utils import DirectoryManager, FileUnlocker

VERSION = "2.6.0"
GITHUB_REPO = "ChampiP/bot-rpa"


class UpdateChecker:
    """Verificador de actualizaciones"""
    
    @staticmethod
    def check():
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                latest_version = response.json().get('tag_name', '').lstrip('v')
                current_version = VERSION.lstrip('v')
                if latest_version and latest_version > current_version:
                    print(f"\n[!] Nueva version disponible: v{latest_version} (actual: v{current_version})")
                    print(f"[!] Descarga desde: https://github.com/{GITHUB_REPO}/releases/latest\n")
                    return True
        except (requests.RequestException, KeyError):
            pass
        return False


class BotRPA:
    """Bot principal de descarga automática"""
    
    def __init__(self):
        self.config = ConfigLoader()
        self.dirs = DirectoryManager()
        self.unlocker = FileUnlocker()
        
        chrome_config = ChromeConfigurator(self.dirs.download_dir, self.config)
        self.chrome_options = chrome_config.get_options()
        
        self.driver = None
        self.wait = None
        self.auth = None
        self.search = None
        self.downloader = None
    
    def initialize(self):
        """Inicializar el bot"""
        print("=" * 60)
        print(f"   INICIANDO COORPIBOT v{VERSION}")
        print("=" * 60)
        
        UpdateChecker.check()
        
        print(f"\n[*] Carpeta de descargas: {self.dirs.download_dir}")
        print("[*] Modo ULTRA RAPIDO activado")
        
        if self.config.debug_mode:
            print("[*] Modo DEBUG: ACTIVADO")
        
        print()
        
        # Inicializar driver
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.set_page_load_timeout(self.config.timings.page_load_timeout)
        self.wait = WebDriverWait(self.driver, self.config.timings.explicit_wait)
        
        # Configurar CDP
        try:
            self.driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": self.dirs.download_dir
            })
            print("[OK] Chrome configurado correctamente\n")
        except WebDriverException:
            pass
        
        # Inicializar servicios
        self.auth = AuthService(self.driver, self.wait, self.config)
        self.search = SearchEngine(self.driver, self.wait, self.config)
        self.downloader = DownloadManager(
            self.driver, self.dirs, self.unlocker, self.config.timings
        )
    
    def safe_get(self, url, max_retries=3):
        """Navegar a URL con manejo de errores"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                return True
            except TimeoutException:
                try:
                    self.driver.execute_script("window.stop();")
                except WebDriverException:
                    pass
                return True
            except WebDriverException:
                if attempt == max_retries - 1:
                    return True
        return True
    
    def navigate_to_search(self):
        """Navegar al buscador"""
        self.safe_get(self.config.url_buscador)
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.ID, self.config.id_barra_busqueda)
            ))
        except TimeoutException:
            pass
    
    def process_term(self, idx, termino):
        """Procesar un término de búsqueda"""
        try:
            print(f"\n[{idx}/{len(self.config.lista_busqueda)}] Buscando: '{termino}'")
            
            if self.driver.current_url != self.config.url_buscador:
                self.safe_get(self.config.url_buscador)
            
            self.search.search_term(termino)
            resultados = self.search.find_results(termino)
            
            if not resultados:
                print(f"[X] Sin resultados")
                self.safe_get(self.config.url_buscador)
                return
            
            print(f"[OK] {len(resultados)} resultados encontrados")
            mejor = self.search.select_best_result(resultados, termino)
            
            if not mejor:
                print("   [X] No se pudo seleccionar resultado")
                return
            
            info = self.search.extract_result_info(mejor)
            self.downloader.process_download(mejor, info)
            
            self.safe_get(self.config.url_buscador)
                
        except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
            print(f"   [ERROR] {type(e).__name__}: {e}")
            self._recover()
        except Exception as e:
            print(f"   [ERROR] Excepcion: {e}")
            self._recover()
    
    def _recover(self):
        """Recuperar sesión después de error"""
        print("   -> Recuperando sesion...")
        try:
            self.driver.refresh()
            self.safe_get(self.config.url_buscador)
        except WebDriverException:
            print("   [ERROR CRITICO] No se pudo recuperar")
            raise
    
    def process_all(self):
        """Procesar todos los términos"""
        for idx, termino in enumerate(self.config.lista_busqueda, 1):
            self.process_term(idx, termino)
    
    def cleanup(self):
        """Limpieza final"""
        print("\n" + "=" * 60)
        print("   RESUMEN DEL PROCESO")
        print("=" * 60)
        
        try:
            archivos = [
                f for f in os.listdir(self.dirs.download_dir) 
                if f.endswith('.xlsm') and not f.startswith('~$')
            ]
            print(f"   [OK] Archivos descargados: {len(archivos)}")
            print(f"   Ubicacion: {self.dirs.download_dir}")
        except OSError:
            pass
        
        print("=" * 60)
        print("\n   Cerrando navegador...")
        
        if self.driver:
            self.driver.quit()
        
        print("   [OK] Proceso finalizado")
    
    def run(self):
        """Ejecutar el bot completo"""
        try:
            self.initialize()
            self.auth.login()
            self.navigate_to_search()
            self.process_all()
            self.auth.logout()
        except KeyboardInterrupt:
            print("\n[!] Proceso interrumpido")
        except Exception as e:
            print(f"\n[ERROR GENERAL] {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()


def main():
    """Punto de entrada principal"""
    bot = BotRPA()
    bot.run()


if __name__ == "__main__":
    main()

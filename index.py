import time
import os
import subprocess
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    StaleElementReferenceException,
    WebDriverException,
    ElementClickInterceptedException
)
from dotenv import load_dotenv

VERSION = "2.5.1"
GITHUB_REPO = "ChampiP/bot-rpa"


class UpdateChecker:
    @staticmethod
    def check_for_updates():
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


class TimingConfig:
    def __init__(self):
        load_dotenv()
        # Valores optimizados para conexiones rápidas 80+ Mbps
        # Mantiene mínimos seguros pero con defaults más agresivos
        self.short_wait = max(0.3, float(os.getenv('TIMING_SHORT_WAIT', '0.3')))
        self.medium_wait = max(1.0, float(os.getenv('TIMING_MEDIUM_WAIT', '1.0')))
        self.long_wait = max(2.0, float(os.getenv('TIMING_LONG_WAIT', '2')))
        self.page_load_timeout = max(60, int(os.getenv('TIMING_PAGE_LOAD', '90')))
        self.explicit_wait = max(15, int(os.getenv('TIMING_EXPLICIT_WAIT', '18')))
        self.download_timeout = int(os.getenv('TIMING_DOWNLOAD_TIMEOUT', '35'))
        self.rate_limit_delay = max(0.5, float(os.getenv('TIMING_RATE_LIMIT', '0.5')))
        self.retry_delay = max(2.0, float(os.getenv('TIMING_RETRY_DELAY', '2')))
    
    def apply_rate_limit(self):
        time.sleep(self.rate_limit_delay)


class ConfigLoader:
    def __init__(self):
        load_dotenv()
        self.usuario = os.getenv('CLARO_USUARIO')
        self.clave = os.getenv('CLARO_CLAVE')
        self.url_login = os.getenv('URL_LOGIN')
        self.url_buscador = os.getenv('URL_BUSCADOR')
        self.id_barra_busqueda = os.getenv('ID_BARRA_BUSQUEDA', '_3_keywords')
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.proxy_enabled = os.getenv('PROXY_ENABLED', 'false').lower() == 'true'
        self.proxy_host = os.getenv('PROXY_HOST', '')
        self.proxy_port = os.getenv('PROXY_PORT', '')
        self.lista_busqueda = []
        self.timings = TimingConfig()
        
        self._validate_credentials()
        self._load_search_terms()
    
    def _validate_credentials(self):
        if not self.usuario or not self.clave:
            print("ERROR: No se encontraron las credenciales.")
            print("Asegurate de que el archivo .env existe y contiene CLARO_USUARIO y CLARO_CLAVE")
            exit(1)
    
    def _load_search_terms(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'terms.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.lista_busqueda = config.get('lista_busqueda', [])
                if not self.lista_busqueda:
                    raise ValueError('lista_busqueda vacia en terms.json')
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"[ERROR CRITICO] No se pudo cargar terms.json ({e}).")
            print("El bot no puede continuar sin la lista de busqueda.")
            exit(1)


class DirectoryManager:
    def __init__(self):
        self.download_dir = self._get_download_directory()
        self.final_dir = self._get_final_directory()
        self._create_directories()
    
    def _get_download_directory(self):
        default_downloads = os.path.join(
            os.environ.get('USERPROFILE', os.getcwd()), 
            'Downloads'
        )
        return os.path.abspath(default_downloads)
    
    def _get_final_directory(self):
        return os.path.join(os.path.dirname(__file__), 'Diagramas_Claro_Final')
    
    def _create_directories(self):
        for directory in [self.download_dir, self.final_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def get_files_snapshot(self):
        snapshot = {}
        if not os.path.exists(self.download_dir):
            return snapshot
        
        for filename in os.listdir(self.download_dir):
            path = os.path.join(self.download_dir, filename)
            try:
                if os.path.isfile(path):
                    snapshot[filename] = os.path.getmtime(path)
            except OSError:
                pass
        return snapshot


class FileUnlocker:
    @staticmethod
    def unblock_file(file_path):
        try:
            cmd = [
                'powershell', 
                '-NoProfile', 
                '-ExecutionPolicy', 
                'Bypass', 
                '-Command', 
                f"Unblock-File -LiteralPath '{file_path}'"
            ]
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True, 
                startupinfo=startupinfo,
                timeout=10
            )
            
            print("   -> [OK] Archivo desbloqueado (Macros habilitadas).")
            return True
        except subprocess.TimeoutExpired:
            print(f"   -> [X] Timeout desbloqueando archivo")
            return False
        except subprocess.CalledProcessError as e:
            print(f"   -> [X] Error PowerShell: {e}")
            return False
        except Exception as e:
            print(f"   -> [X] Error inesperado: {e}")
            return False


class ChromeConfigurator:
    def __init__(self, download_directory, config):
        self.download_dir = download_directory
        self.config = config
        self.options = Options()
        self._configure_preferences()
        self._configure_arguments()
        self._configure_proxy()
    
    def _configure_preferences(self):
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "download_restrictions": 0,
            "download.extensions_to_open": "xlsm",
            "profile.default_content_settings.popups": 0,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
        }
        
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    def _configure_arguments(self):
        arguments = [
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--allow-insecure-localhost',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-blink-features=AutomationControlled',
            '--safebrowsing-disable-download-protection',
            '--safebrowsing-disable-extension-blacklist',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        for arg in arguments:
            self.options.add_argument(arg)
    
    def _configure_proxy(self):
        if self.config.proxy_enabled and self.config.proxy_host and self.config.proxy_port:
            proxy_url = f"{self.config.proxy_host}:{self.config.proxy_port}"
            self.options.add_argument(f'--proxy-server={proxy_url}')
            print(f"[*] Proxy configurado: {proxy_url}")
    
    def get_options(self):
        return self.options


class SearchEngine:
    def __init__(self, driver, wait, config, dirs):
        self.driver = driver
        self.wait = wait
        self.config = config
        self.dirs = dirs
        self.debug_mode = config.debug_mode
        self.timings = config.timings
    
    def print_page_structure(self):
        if not self.debug_mode:
            return
        
        try:
            print("\n   [DEBUG] Estructura de la pagina:")
            containers = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".search-results, .asset-entry, .document-entry, [class*='result']"
            )
            print(f"   Contenedores encontrados: {len(containers)}")
            for i, container in enumerate(containers[:3]):
                print(f"\n   Contenedor {i+1}:")
                print(f"   HTML: {container.get_attribute('outerHTML')[:200]}...")
        except (NoSuchElementException, WebDriverException) as e:
            print(f"   [DEBUG] Error: {e}")
    
    def find_search_box(self):
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.ID, self.config.id_barra_busqueda))
            )
        except TimeoutException:
            try:
                return self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='text'][name*='keywords']")
                    )
                )
            except TimeoutException:
                return self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    
    def search_term(self, termino):
        search_box = self.find_search_box()
        search_box.clear()
        time.sleep(self.timings.short_wait)
        search_box.send_keys(termino)
        search_box.send_keys(Keys.RETURN)
        # Espera optimizada para resultados
        time.sleep(self.timings.medium_wait)
    
    def extract_result_info(self, element):
        info = {
            'texto': '',
            'titulo': '',
            'descripcion': '',
            'href': '',
            'highlights_count': 0
        }
        
        try:
            title_element = None
            if hasattr(element, 'title_element'):
                title_element = element.title_element
            else:
                try:
                    title_element = element.find_element(By.XPATH, "./ancestor::span[@class='asset-entry-title']")
                except NoSuchElementException:
                    try:
                        title_element = element.find_element(By.XPATH, "./parent::span[@class='asset-entry-title']")
                    except NoSuchElementException:
                        pass
            
            if title_element:
                info['titulo'] = title_element.text.strip()
                try:
                    highlights = title_element.find_elements(By.CSS_SELECTOR, "span.highlight")
                    info['highlights_count'] = len(highlights)
                except NoSuchElementException:
                    pass
            else:
                info['titulo'] = element.text.strip()
            
            info['texto'] = info['titulo']
            
            try:
                parent = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'asset-entry')]")
                desc_elem = parent.find_element(By.CSS_SELECTOR, ".asset-entry-content, .description")
                info['descripcion'] = desc_elem.text.strip()[:100]
            except NoSuchElementException:
                pass
            
            try:
                info['href'] = element.get_attribute('href')
            except:
                pass
                
        except Exception as e:
            print(f"   -> Error extrayendo info: {e}")
        
        return info
    
    def find_results(self, termino):
        resultados = []
        
        self.print_page_structure()
        
        try:
            title_elements = self.driver.find_elements(By.CSS_SELECTOR, "span.asset-entry-title")
            
            if title_elements:
                for title_element in title_elements:
                    try:
                        link = title_element.find_element(By.TAG_NAME, "a")
                        if link:
                            link.title_element = title_element
                            resultados.append(link)
                    except NoSuchElementException:
                        try:
                            if title_element.get_attribute("href"):
                                resultados.append(title_element)
                        except:
                            pass
                
        except NoSuchElementException:
            pass
        
        if not resultados:
            resultados = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Diagrama")
        
        if not resultados:
            resultados = self.driver.find_elements(By.CSS_SELECTOR, "a[href$='.xlsm']")
        
        if not resultados:
            try:
                doc_links = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".search-results a, .document-container a, .asset-entry a"
                )
                if doc_links:
                    resultados = doc_links
            except NoSuchElementException:
                pass
        
        if not resultados:
            palabras_clave = termino.split()
            if len(palabras_clave) > 0:
                keyword = next((w for w in palabras_clave if len(w) > 3), palabras_clave[0])
                resultados = self.driver.find_elements(By.PARTIAL_LINK_TEXT, keyword)
        
        return resultados
    
    def select_best_result(self, resultados, termino):
        if not resultados:
            return None
        
        termino_lower = termino.lower()
        palabras_termino = [p for p in termino_lower.split() if len(p) > 2]
        
        mejor_score = -1
        mejor_resultado = resultados[0]
        mejor_titulo_completo = ""
        
        for resultado in resultados:
            try:
                title_element = None
                if hasattr(resultado, 'title_element'):
                    title_element = resultado.title_element
                else:
                    try:
                        title_element = resultado.find_element(By.XPATH, "./ancestor::span[@class='asset-entry-title']")
                    except NoSuchElementException:
                        try:
                            title_element = resultado.find_element(By.XPATH, "./parent::span[@class='asset-entry-title']")
                        except NoSuchElementException:
                            pass
                
                if title_element:
                    texto_resultado = title_element.text.strip()
                else:
                    texto_resultado = resultado.text.strip()
                
                if not texto_resultado:
                    continue
                
                texto_lower = texto_resultado.lower()
                score = 0
                
                num_highlights = 0
                if title_element:
                    try:
                        highlights = title_element.find_elements(By.CSS_SELECTOR, "span.highlight")
                        num_highlights = len(highlights)
                        score += num_highlights * 500
                    except NoSuchElementException:
                        pass
                
                if termino_lower in texto_lower:
                    score += 2000
                
                palabras_encontradas = 0
                for palabra in palabras_termino:
                    if palabra in texto_lower:
                        score += 100
                        palabras_encontradas += 1
                
                porcentaje_coincidencia = palabras_encontradas / len(palabras_termino) if palabras_termino else 0
                if porcentaje_coincidencia > 0.8:
                    score += 300
                
                for palabra in palabras_termino:
                    if texto_lower.startswith(palabra):
                        score += 50
                        break
                
                if "guia" in texto_lower or "diagrama" in texto_lower:
                    score += 25
                
                len_diff = abs(len(texto_lower) - len(termino_lower))
                if len_diff > 100:
                    score -= 20
                
                if score > mejor_score:
                    mejor_score = score
                    mejor_resultado = resultado
                    mejor_titulo_completo = texto_resultado
                    
            except StaleElementReferenceException:
                print(f"   -> Elemento obsoleto, continuando...")
                continue
            except Exception as e:
                print(f"   -> Error evaluando resultado: {e}")
                continue
        
        return mejor_resultado
    
    def wait_for_download(self, snapshot_antes, timeout=None):
        if timeout is None:
            timeout = self.timings.download_timeout
            
        tiempo_inicio = time.time()
        archivo_final = None
        check_interval = 0.5  # Verificar cada 0.5 segundos para ser más rápido
        
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
                    
                    # Verificar que el archivo se haya descargado completamente
                    for i in range(3):
                        try:
                            size_curr = os.path.getsize(archivo_final)
                            if size_curr == size_prev and size_curr > 0:
                                return archivo_final
                            size_prev = size_curr
                            time.sleep(self.timings.short_wait)
                        except OSError:
                            if i == 2:  # Último intento
                                return archivo_final if os.path.exists(archivo_final) else None
                    
                    return archivo_final
            except OSError:
                pass
            
            time.sleep(check_interval)
        
        return archivo_final


class BotRPA:
    def __init__(self, config, dirs, unlocker, chrome_options):
        self.config = config
        self.dirs = dirs
        self.unlocker = unlocker
        self.driver = None
        self.wait = None
        self.chrome_options = chrome_options
        self.search_engine = None
        
    def initialize_driver(self):
        print("=" * 60)
        print(f"   INICIANDO BOT RPA v{VERSION} - MODO DESCARGA AUTOMATICA")
        print("=" * 60)
        
        UpdateChecker.check_for_updates()
        
        print("\n[*] Configurando Chrome con permisos extendidos...")
        print(f"[*] Carpeta de descargas: {self.dirs.download_dir}")
        print("[*] Safe Browsing: DESACTIVADO")
        print("[*] Proteccion de descargas: DESACTIVADA")
        
        if self.config.debug_mode:
            print("[*] Modo DEBUG: ACTIVADO")
        
        if self.config.proxy_enabled:
            print(f"[*] Proxy: {self.config.proxy_host}:{self.config.proxy_port}")
        
        print()
        
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.set_page_load_timeout(self.config.timings.page_load_timeout)
        self.wait = WebDriverWait(self.driver, self.config.timings.explicit_wait)
        self.search_engine = SearchEngine(self.driver, self.wait, self.config, self.dirs)
        
        self._configure_cdp()
    
    def _configure_cdp(self):
        try:
            self.driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": self.dirs.download_dir
            })
            print("[OK] Chrome DevTools Protocol: Descargas automaticas habilitadas\n")
        except WebDriverException as e:
            print(f"[!] Advertencia CDP: {e}\n")
    
    def safe_get(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                # Espera reducida para mejorar velocidad
                time.sleep(self.config.timings.short_wait)
                return True
            except TimeoutException:
                if attempt < max_retries - 1:
                    print(f"   [!] Timeout navegando a {url} (Intento {attempt + 1}/{max_retries})")
                    # Detener carga de página
                    try:
                        self.driver.execute_script("window.stop();")
                    except WebDriverException:
                        pass
                    time.sleep(self.config.timings.short_wait)
                else:
                    print(f"   [!] Timeout final en {url}, continuando de todos modos...")
                    try:
                        self.driver.execute_script("window.stop();")
                        return True  # Continuar aunque haya timeout
                    except WebDriverException:
                        return False
            except WebDriverException as e:
                print(f"   [!] Error WebDriver: {e} (Intento {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(self.config.timings.retry_delay)
        return False
    
    def login(self):
        print(f"Accediendo al login: {self.config.url_login}")
        if not self.safe_get(self.config.url_login):
            raise WebDriverException("No se pudo acceder a la pagina de login tras varios intentos.")
        
        try:
            # Espera optimizada para campos de login
            campo_user = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[id*='login']"))
            )
            campo_pass = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            
            print(f"Logueando como {self.config.usuario}...")
            campo_user.clear()
            time.sleep(self.timings.short_wait)
            campo_user.send_keys(self.config.usuario)
            
            campo_pass.clear()
            time.sleep(self.timings.short_wait)
            campo_pass.send_keys(self.config.clave)
            campo_pass.send_keys(Keys.RETURN)
            
            # Esperar a que la página cargue después del login
            time.sleep(self.config.timings.medium_wait)
            
            # Verificar si el login fue exitoso
            try:
                self.wait.until(lambda d: d.current_url != self.config.url_login)
                print("[OK] Login exitoso")
            except TimeoutException:
                print("[OK] Login completado (verificación de URL timeout)")
                
        except TimeoutException as e:
            print(f"[!] Timeout en login automatico. Error: {e}")
            print("[*] Esperando 15 segundos para login manual si es necesario...")
            time.sleep(15)
        except NoSuchElementException as e:
            print(f"[!] No se encontraron campos de login. Error: {e}")
            print("[*] Esperando 15 segundos para login manual si es necesario...")
            time.sleep(15)
    
    def navigate_to_search(self):
        if not self.safe_get(self.config.url_buscador):
            print("   [!] Advertencia: Fallo carga inicial del buscador. Reintentando...")
        time.sleep(self.config.timings.medium_wait)
    
    def process_single_download(self, idx, termino):
        try:
            print(f"\n[{idx}/{len(self.config.lista_busqueda)}] Buscando: '{termino}'")
            
            if self.driver.current_url != self.config.url_buscador:
                self.safe_get(self.config.url_buscador)
                time.sleep(self.config.timings.short_wait)
            
            self.search_engine.search_term(termino)
            resultados = self.search_engine.find_results(termino)
            
            if not resultados:
                print(f"[X] Sin resultados")
                self.safe_get(self.config.url_buscador)
                return
            
            print(f"[OK] {len(resultados)} resultados encontrados")
            mejor_resultado = self.search_engine.select_best_result(resultados, termino)
            
            if not mejor_resultado:
                print("   [X] No se pudo seleccionar un resultado valido")
                return
            
            info = self.search_engine.extract_result_info(mejor_resultado)
            titulo_corto = info.get('titulo', 'N/A')[:70] + '...' if len(info.get('titulo', '')) > 70 else info.get('titulo', 'N/A')
            print(f"[>>] Seleccionado: {titulo_corto}")
            
            snapshot_antes = self.dirs.get_files_snapshot()
            
            # Scroll más rápido sin animación
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", 
                mejor_resultado
            )
            time.sleep(0.3)  # Espera mínima
            
            try:
                mejor_resultado.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", mejor_resultado)
            
            archivo_final = self.search_engine.wait_for_download(snapshot_antes)
            
            if archivo_final and os.path.exists(archivo_final):
                self.unlocker.unblock_file(archivo_final)
                archivo_nombre = os.path.basename(archivo_final)
                if len(archivo_nombre) > 60:
                    archivo_nombre = archivo_nombre[:57] + '...'
                print(f"[✓] Descargado: {archivo_nombre}\n")
            else:
                print(f"[!] Error en descarga\n")
            
            # Volver al buscador más rápido
            self.safe_get(self.config.url_buscador)
            time.sleep(self.config.timings.short_wait)
                
        except TimeoutException as e:
            print(f"   [ERROR] Timeout en '{termino}': {e}")
            self._recover_session()
        except StaleElementReferenceException as e:
            print(f"   [ERROR] Elemento obsoleto en '{termino}': {e}")
            self._recover_session()
        except WebDriverException as e:
            print(f"   [ERROR] WebDriver en '{termino}': {e}")
            self._recover_session()
        except Exception as e:
            print(f"   [ERROR] Excepcion inesperada en '{termino}': {e}")
            self._recover_session()
    
    def _recover_session(self):
        print("   -> Intentando recuperar sesion...")
        try:
            self.driver.refresh()
            time.sleep(self.config.timings.medium_wait)
            self.safe_get(self.config.url_buscador)
            time.sleep(self.config.timings.medium_wait)
        except WebDriverException:
            print("   [ERROR CRITICO] No se pudo recuperar la sesion")
            raise
    
    def process_downloads(self):
        for idx, termino in enumerate(self.config.lista_busqueda, 1):
            self.process_single_download(idx, termino)
    
    def logout(self):
        print("\n" + "=" * 60)
        print("   CERRANDO SESION")
        print("=" * 60)
        
        try:
            logout_found = False
            logout_texts = ["Cerrar sesion", "Cerrar Sesion", "Logout", "Salir", "Sign Out"]
            
            for text in logout_texts:
                try:
                    links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, text)
                    if links:
                        print(f"   -> Click en '{text}'...")
                        links[0].click()
                        logout_found = True
                        time.sleep(self.config.timings.medium_wait)
                        break
                except NoSuchElementException:
                    continue
            
            if not logout_found:
                print("   -> Boton no encontrado, forzando logout por URL...")
                self.safe_get("http://portaldeconocimiento.claro.com.pe/c/portal/logout")
                time.sleep(self.config.timings.medium_wait)
            
            print("   -> [OK] Sesion finalizada.")
        except Exception as e:
            print(f"   [!] Error al cerrar sesion: {e}")
    
    def cleanup(self):
        print("\n" + "=" * 60)
        print("   RESUMEN DEL PROCESO")
        print("=" * 60)
        
        try:
            archivos = [
                f for f in os.listdir(self.dirs.download_dir) 
                if f.endswith('.xlsm') and not f.startswith('~$')
            ]
            print(f"   [OK] Archivos en carpeta Descargas: {len(archivos)}")
            print(f"   Ubicacion: {self.dirs.download_dir}")
        except OSError:
            pass
        
        print("=" * 60)
        print("\n   Cerrando navegador en 3 segundos...")
        time.sleep(3)
        
        if self.driver:
            self.driver.quit()
        
        print("   [OK] Proceso finalizado correctamente")
    
    def run(self):
        try:
            self.initialize_driver()
            self.login()
            self.navigate_to_search()
            self.process_downloads()
            self.logout()
        except KeyboardInterrupt:
            print("\n[!] Proceso interrumpido por el usuario")
        except Exception as e:
            print(f"\n[ERROR GENERAL] {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()


def main():
    config = ConfigLoader()
    dirs = DirectoryManager()
    unlocker = FileUnlocker()
    chrome_config = ChromeConfigurator(dirs.download_dir, config)
    
    bot = BotRPA(config, dirs, unlocker, chrome_config.get_options())
    bot.run()


if __name__ == "__main__":
    main()

# Bot RPA para automatizacion de descargas desde el portal de Claro

import time
import os
import subprocess
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


class ConfigLoader:
    # Carga y valida la configuracion del bot
    
    def __init__(self):
        load_dotenv()
        self.usuario = os.getenv('CLARO_USUARIO')
        self.clave = os.getenv('CLARO_CLAVE')
        self.url_login = os.getenv('URL_LOGIN')
        self.url_buscador = os.getenv('URL_BUSCADOR')
        self.id_barra_busqueda = os.getenv('ID_BARRA_BUSQUEDA', '_3_keywords')
        self.lista_busqueda = []
        
        self._validate_credentials()
        self._load_search_terms()
    
    def _validate_credentials(self):
        # Valida que las credenciales esten configuradas
        if not self.usuario or not self.clave:
            print("ERROR: No se encontraron las credenciales.")
            print("Asegurate de que el archivo .env existe y contiene CLARO_USUARIO y CLARO_CLAVE")
            exit(1)
    
    def _load_search_terms(self):
        # Carga los terminos de busqueda desde config/terms.json
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'terms.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.lista_busqueda = config.get('lista_busqueda', [])
                if not self.lista_busqueda:
                    raise ValueError('lista_busqueda vacia en terms.json')
        except Exception as e:
            print(f"[ERROR CRITICO] No se pudo cargar terms.json ({e}).")
            print("El bot no puede continuar sin la lista de busqueda.")
            exit(1)


class DirectoryManager:
    # Gestiona los directorios de descarga
    
    def __init__(self):
        self.download_dir = self._get_download_directory()
        self.final_dir = self._get_final_directory()
        self._create_directories()
    
    def _get_download_directory(self):
        # Obtiene el directorio de descargas del usuario
        default_downloads = os.path.join(
            os.environ.get('USERPROFILE', os.getcwd()), 
            'Downloads'
        )
        return os.path.abspath(default_downloads)
    
    def _get_final_directory(self):
        # Obtiene el directorio final de almacenamiento
        return os.path.join(os.path.dirname(__file__), 'Diagramas_Claro_Final')
    
    def _create_directories(self):
        # Crea los directorios si no existen
        for directory in [self.download_dir, self.final_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def get_files_snapshot(self):
        # Obtiene un snapshot de los archivos en el directorio de descargas
        snapshot = {}
        if not os.path.exists(self.download_dir):
            return snapshot
        
        for filename in os.listdir(self.download_dir):
            path = os.path.join(self.download_dir, filename)
            try:
                if os.path.isfile(path):
                    snapshot[filename] = os.path.getmtime(path)
            except:
                pass
        return snapshot


class FileUnlocker:
    # Desbloquea archivos descargados de Windows
    
    @staticmethod
    def unblock_file(file_path):
        # Desbloquea un archivo usando PowerShell
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
                startupinfo=startupinfo
            )
            
            print("   -> [OK] Archivo desbloqueado (Macros habilitadas).")
            return True
        except Exception as e:
            print(f"   -> [X] No se pudo desbloquear: {e}")
            return False


class ChromeConfigurator:
    # Configura las opciones de Chrome para el bot
    
    def __init__(self, download_directory):
        self.download_dir = download_directory
        self.options = Options()
        self._configure_preferences()
        self._configure_arguments()
    
    def _configure_preferences(self):
        # Configura las preferencias de Chrome
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
        # Configura los argumentos de linea de comandos de Chrome
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
    
    def get_options(self):
        # Retorna las opciones configuradas
        return self.options


class SearchEngine:
    # Maneja la logica de busqueda y descarga
    
    def __init__(self, driver, wait, config, dirs):
        self.driver = driver
        self.wait = wait
        self.config = config
        self.dirs = dirs
        self.debug_mode = False  # Activar para ver mas detalles
    
    def print_page_structure(self):
        # Imprime la estructura de la pagina para debugging
        if not self.debug_mode:
            return
        
        try:
            print("\n   [DEBUG] Estructura de la pagina:")
            
            # Buscar contenedores de resultados
            containers = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".search-results, .asset-entry, .document-entry, [class*='result']"
            )
            
            print(f"   Contenedores encontrados: {len(containers)}")
            
            for i, container in enumerate(containers[:3]):  # Solo primeros 3
                print(f"\n   Contenedor {i+1}:")
                print(f"   HTML: {container.get_attribute('outerHTML')[:200]}...")
                
        except Exception as e:
            print(f"   [DEBUG] Error: {e}")
    
    def find_search_box(self):
        # Encuentra la barra de busqueda en la pagina
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.ID, self.config.id_barra_busqueda))
            )
        except:
            try:
                return self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='text'][name*='keywords']")
                    )
                )
            except:
                return self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    
    def search_term(self, termino):
        # Realiza la busqueda de un termino
        search_box = self.find_search_box()
        search_box.clear()
        time.sleep(0.3)
        search_box.send_keys(termino)
        time.sleep(0.3)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
    
    def extract_result_info(self, element):
        # Extrae informacion detallada de un elemento resultado
        info = {
            'texto': '',
            'titulo': '',
            'descripcion': '',
            'href': '',
            'highlights_count': 0
        }
        
        try:
            # Buscar el span.asset-entry-title asociado
            title_element = None
            if hasattr(element, 'title_element'):
                title_element = element.title_element
            else:
                try:
                    title_element = element.find_element(By.XPATH, "./ancestor::span[@class='asset-entry-title']")
                except:
                    try:
                        title_element = element.find_element(By.XPATH, "./parent::span[@class='asset-entry-title']")
                    except:
                        pass
            
            # Obtener titulo completo
            if title_element:
                info['titulo'] = title_element.text.strip()
                
                # Contar highlights en el titulo
                try:
                    highlights = title_element.find_elements(By.CSS_SELECTOR, "span.highlight")
                    info['highlights_count'] = len(highlights)
                except:
                    pass
            else:
                info['titulo'] = element.text.strip()
            
            info['texto'] = info['titulo']
            
            # Intentar obtener la descripcion (fuera del titulo)
            try:
                # Buscar el contenedor padre que tiene la descripcion
                parent = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'asset-entry')]")
                desc_elem = parent.find_element(By.CSS_SELECTOR, ".asset-entry-content, .description")
                info['descripcion'] = desc_elem.text.strip()[:100]
            except:
                pass
            
            # Obtener el href
            try:
                info['href'] = element.get_attribute('href')
            except:
                pass
                
        except Exception as e:
            print(f"   -> Error extrayendo info: {e}")
        
        return info
    
    def find_results(self, termino):
        # Encuentra los resultados de busqueda usando estructura HTML del portal
        resultados = []
        
        # Debug opcional
        self.print_page_structure()
        
        # Estrategia PRINCIPAL: Buscar por span.asset-entry-title y extraer enlaces
        try:
            # Buscar TODOS los elementos con clase asset-entry-title
            title_elements = self.driver.find_elements(By.CSS_SELECTOR, "span.asset-entry-title")
            
            if title_elements:
                for title_element in title_elements:
                    try:
                        # Buscar el enlace <a> DENTRO del span.asset-entry-title
                        link = title_element.find_element(By.TAG_NAME, "a")
                        if link:
                            # Guardar tanto el link como el elemento del titulo para analisis
                            link.title_element = title_element  # Adjuntar referencia al titulo
                            resultados.append(link)
                    except:
                        try:
                            # Fallback: buscar si el title_element mismo es clickeable
                            if title_element.get_attribute("href"):
                                resultados.append(title_element)
                        except:
                            pass
                
        except Exception as e:
            pass
        
        # Estrategia 2: Buscar enlaces que contengan "Diagrama" o sean .xlsm
        if not resultados:
            resultados = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Diagrama")
        
        if not resultados:
            resultados = self.driver.find_elements(By.CSS_SELECTOR, "a[href$='.xlsm']")
        
        # Estrategia 3: Buscar en la lista de documentos (estructura table-based)
        if not resultados:
            try:
                doc_links = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".search-results a, .document-container a, .asset-entry a"
                )
                if doc_links:
                    resultados = doc_links
            except:
                pass
        
        # Estrategia 4: Busqueda por palabras clave del termino
        if not resultados:
            palabras_clave = termino.split()
            if len(palabras_clave) > 0:
                keyword = next((w for w in palabras_clave if len(w) > 3), palabras_clave[0])
                resultados = self.driver.find_elements(By.PARTIAL_LINK_TEXT, keyword)
        
        return resultados
    
    def select_best_result(self, resultados, termino):
        # Selecciona el mejor resultado usando coincidencia inteligente basada en highlights
        if not resultados:
            return None
        
        termino_lower = termino.lower()
        palabras_termino = [p for p in termino_lower.split() if len(p) > 2]
        
        mejor_score = -1
        mejor_resultado = resultados[0]
        mejor_titulo_completo = ""
        
        for resultado in resultados:
            try:
                # CLAVE: Obtener el elemento title asociado al enlace
                title_element = None
                if hasattr(resultado, 'title_element'):
                    title_element = resultado.title_element
                else:
                    # Intentar encontrar el span.asset-entry-title que contiene este enlace
                    try:
                        title_element = resultado.find_element(By.XPATH, "./ancestor::span[@class='asset-entry-title']")
                    except:
                        try:
                            title_element = resultado.find_element(By.XPATH, "./parent::span[@class='asset-entry-title']")
                        except:
                            pass
                
                # Obtener el texto completo del titulo (SIN recortar)
                if title_element:
                    texto_resultado = title_element.text.strip()
                else:
                    texto_resultado = resultado.text.strip()
                
                if not texto_resultado:
                    continue
                
                texto_lower = texto_resultado.lower()
                
                # Inicializar score
                score = 0
                
                # ===== SCORING PRINCIPAL =====
                
                # 1. CONTAR HIGHLIGHTS DENTRO DEL TITULO (MAXIMA PRIORIDAD)
                num_highlights = 0
                if title_element:
                    try:
                        highlights = title_element.find_elements(By.CSS_SELECTOR, "span.highlight")
                        num_highlights = len(highlights)
                        score += num_highlights * 500  # 500 puntos por cada highlight
                    except:
                        pass
                
                # 2. Coincidencia exacta del termino completo
                if termino_lower in texto_lower:
                    score += 2000
                
                # 3. Contar palabras que coinciden
                palabras_encontradas = 0
                for palabra in palabras_termino:
                    if palabra in texto_lower:
                        score += 100
                        palabras_encontradas += 1
                
                # 4. Bonus si casi todas las palabras coinciden
                porcentaje_coincidencia = palabras_encontradas / len(palabras_termino) if palabras_termino else 0
                if porcentaje_coincidencia > 0.8:  # Mas del 80% de palabras coinciden
                    score += 300
                
                # 5. Bonus si el texto empieza con alguna palabra del termino
                for palabra in palabras_termino:
                    if texto_lower.startswith(palabra):
                        score += 50
                        break
                
                # 6. Bonus moderado si contiene "guia" o "diagrama"
                if "guia" in texto_lower or "diagrama" in texto_lower:
                    score += 25
                
                # 7. Penalizar diferencias muy grandes de longitud
                len_diff = abs(len(texto_lower) - len(termino_lower))
                if len_diff > 100:
                    score -= 20
                
                # Actualizar mejor resultado (sin mostrar cada evaluacion)
                if score > mejor_score:
                    mejor_score = score
                    mejor_resultado = resultado
                    mejor_titulo_completo = texto_resultado
                    
            except Exception as e:
                print(f"   -> Error evaluando resultado: {e}")
                continue
        
        return mejor_resultado
    
    def wait_for_download(self, snapshot_antes, timeout=45):
        # Espera a que se complete la descarga
        tiempo_inicio = time.time()
        archivo_final = None
        
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
                    for _ in range(5):
                        try:
                            size_curr = os.path.getsize(archivo_final)
                            if size_curr == size_prev and size_curr > 0:
                                break
                            size_prev = size_curr
                            time.sleep(0.5)
                        except:
                            pass
                    
                    return archivo_final
            except Exception:
                pass
            
            time.sleep(2)
        
        return archivo_final


class BotRPA:
    # Clase principal que ejecuta el bot de automatizacion
    
    def __init__(self, config, dirs, unlocker, chrome_options):
        self.config = config
        self.dirs = dirs
        self.unlocker = unlocker
        self.driver = None
        self.wait = None
        self.chrome_options = chrome_options
        self.search_engine = None
        
    def initialize_driver(self):
        # Inicializa el navegador Chrome
        print("=" * 60)
        print("   INICIANDO BOT RPA - MODO DESCARGA AUTOMATICA")
        print("=" * 60)
        print("\n[*] Configurando Chrome con permisos extendidos...")
        print(f"[*] Carpeta de descargas: {self.dirs.download_dir}")
        print("[*] Safe Browsing: DESACTIVADO")
        print("[*] Proteccion de descargas: DESACTIVADA\n")
        
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.set_page_load_timeout(180)
        self.wait = WebDriverWait(self.driver, 20)
        self.search_engine = SearchEngine(self.driver, self.wait, self.config, self.dirs)
        
        self._configure_cdp()
    
    def _configure_cdp(self):
        # Configura Chrome DevTools Protocol para descargas automaticas
        try:
            self.driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": self.dirs.download_dir
            })
            print("[OK] Chrome DevTools Protocol: Descargas automaticas habilitadas\n")
        except Exception as e:
            print(f"[!] Advertencia CDP: {e}\n")
    
    def safe_get(self, url, max_retries=3):
        # Navega a una URL con reintentos
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                return True
            except Exception as e:
                print(f"   [!] Error navegando a {url} (Intento {attempt + 1}/{max_retries}): {e}")
                time.sleep(5)
                try:
                    self.driver.execute_script("window.stop();")
                except:
                    pass
        return False
    
    def login(self):
        # Realiza el proceso de login
        print(f"Accediendo al login: {self.config.url_login}")
        if not self.safe_get(self.config.url_login):
            raise Exception("No se pudo acceder a la pagina de login tras varios intentos.")
        
        try:
            campo_user = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id*='login']"))
            )
            campo_pass = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            print(f"Logueando como {self.config.usuario}...")
            campo_user.clear()
            campo_user.send_keys(self.config.usuario)
            campo_pass.clear()
            campo_pass.send_keys(self.config.clave)
            campo_pass.send_keys(Keys.RETURN)
            
            time.sleep(5)
            print("[OK] Login exitoso")
        except Exception as e:
            print(f"Alerta! Fallo el login automatico. Hazlo manual rapido. Error: {e}")
            time.sleep(20)
    
    def navigate_to_search(self):
        # Navega al sitio de busqueda
        if not self.safe_get(self.config.url_buscador):
            print("   [!] Advertencia: Fallo carga inicial del buscador. Reintentando...")
        time.sleep(3)
    
    def process_single_download(self, idx, termino):
        # Procesa la descarga de un termino individual
        try:
            print(f"\n[{idx}/{len(self.config.lista_busqueda)}] Buscando: '{termino}'")
            
            if self.driver.current_url != self.config.url_buscador:
                self.safe_get(self.config.url_buscador)
                time.sleep(2)
            
            # Realizar busqueda
            self.search_engine.search_term(termino)
            
            # Encontrar resultados
            resultados = self.search_engine.find_results(termino)
            
            if not resultados:
                print(f"[X] Sin resultados")
                self.safe_get(self.config.url_buscador)
                time.sleep(1)
                return
            
            print(f"[OK] {len(resultados)} resultados encontrados")
            
            # Seleccionar mejor resultado
            mejor_resultado = self.search_engine.select_best_result(resultados, termino)
            
            if not mejor_resultado:
                print("   [X] No se pudo seleccionar un resultado valido")
                return
            
            # Extraer informacion del resultado
            info = self.search_engine.extract_result_info(mejor_resultado)
            
            titulo_corto = info.get('titulo', 'N/A')[:70] + '...' if len(info.get('titulo', '')) > 70 else info.get('titulo', 'N/A')
            print(f"[>>] Seleccionado: {titulo_corto}")
            
            # Preparar descarga
            snapshot_antes = self.dirs.get_files_snapshot()
            
            # Scroll y click
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                mejor_resultado
            )
            time.sleep(0.5)
            
            try:
                mejor_resultado.click()
            except:
                self.driver.execute_script("arguments[0].click();", mejor_resultado)
            
            # Esperar descarga
            archivo_final = self.search_engine.wait_for_download(snapshot_antes)
            
            if archivo_final and os.path.exists(archivo_final):
                self.unlocker.unblock_file(archivo_final)
                archivo_nombre = os.path.basename(archivo_final)
                if len(archivo_nombre) > 60:
                    archivo_nombre = archivo_nombre[:57] + '...'
                print(f"[✓] Descargado: {archivo_nombre}\n")
            else:
                print(f"[!] Error en descarga\n")
            
            self.safe_get(self.config.url_buscador)
            time.sleep(2)
                
        except Exception as e:
            print(f"   [ERROR] Excepcion en '{termino}': {e}")
            print("   -> Intentando recuperar sesion...")
            try:
                self.driver.refresh()
                time.sleep(3)
                self.safe_get(self.config.url_buscador)
                time.sleep(3)
            except:
                print("   [ERROR CRITICO] No se pudo recuperar la sesion")
                raise
    
    def process_downloads(self):
        # Procesa todas las descargas de la lista de busqueda
        for idx, termino in enumerate(self.config.lista_busqueda, 1):
            self.process_single_download(idx, termino)
    
    def logout(self):
        # Cierra la sesion
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
                        time.sleep(3)
                        break
                except:
                    continue
            
            if not logout_found:
                print("   -> Boton no encontrado, forzando logout por URL...")
                self.safe_get("http://portaldeconocimiento.claro.com.pe/c/portal/logout")
                time.sleep(2)
            
            print("   -> [OK] Sesion finalizada.")
        except Exception as e:
            print(f"   [!] Error al cerrar sesion: {e}")
    
    def cleanup(self):
        # Limpia y cierra el navegador
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
        except:
            pass
        
        print("=" * 60)
        print("\n   Cerrando navegador en 3 segundos...")
        time.sleep(3)
        
        if self.driver:
            self.driver.quit()
        
        print("   [OK] Proceso finalizado correctamente")
    
    def run(self):
        # Ejecuta el proceso completo del bot
        try:
            self.initialize_driver()
            self.login()
            self.navigate_to_search()
            self.process_downloads()
            self.logout()
        except Exception as e:
            print(f"\n[ERROR GENERAL] {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()


def main():
    # Funcion principal del script
    config = ConfigLoader()
    dirs = DirectoryManager()
    unlocker = FileUnlocker()
    chrome_config = ChromeConfigurator(dirs.download_dir)
    
    bot = BotRPA(config, dirs, unlocker, chrome_config.get_options())
    bot.run()


if __name__ == "__main__":
    main()

"""
CoorpiBot - Servicio de Autenticación
Login y logout en el portal
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config
    
    def login(self):
        """Realizar login en el portal"""
        print(f"Accediendo al login: {self.config.url_login}")
        self.driver.get(self.config.url_login)
        
        try:
            campo_user = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[id*='login']"))
            )
            campo_pass = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            
            print(f"Logueando como {self.config.usuario}...")
            campo_user.clear()
            campo_user.send_keys(self.config.usuario)
            campo_pass.clear()
            campo_pass.send_keys(self.config.clave)
            campo_pass.send_keys(Keys.RETURN)
            
            try:
                self.wait.until(lambda d: d.current_url != self.config.url_login)
                print("[OK] Login exitoso")
            except TimeoutException:
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                    print("[OK] Login exitoso")
                except:
                    print("[!] Verificación de login timeout - continuando...")
                
        except TimeoutException:
            print(f"[!] Timeout en login - continuando...")
            time.sleep(5)
        except NoSuchElementException:
            print(f"[!] Campos de login no encontrados - continuando...")
            time.sleep(5)
    
    def logout(self):
        """Cerrar sesión"""
        print("\n" + "=" * 60)
        print("   CERRANDO SESION")
        print("=" * 60)
        
        try:
            logout_texts = ["Cerrar sesion", "Cerrar Sesion", "Logout", "Salir", "Sign Out"]
            logout_found = False
            
            for text in logout_texts:
                try:
                    links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, text)
                    if links:
                        print(f"   -> Click en '{text}'...")
                        links[0].click()
                        logout_found = True
                        break
                except NoSuchElementException:
                    continue
            
            if not logout_found:
                print("   -> Forzando logout por URL...")
                self.driver.get("http://portaldeconocimiento.claro.com.pe/c/portal/logout")
            
            print("   -> [OK] Sesion finalizada.")
        except Exception as e:
            print(f"   [!] Error al cerrar sesion: {e}")

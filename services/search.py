"""
CoorpiBot - Servicio de Búsqueda
Motor de búsqueda y selección de resultados
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    StaleElementReferenceException
)


class SearchEngine:
    """Motor de búsqueda"""
    
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config
        self.timings = config.timings
    
    def _get_title_element(self, element):
        """Obtener elemento título de un resultado (helper para evitar duplicación)"""
        title_element = getattr(element, 'title_element', None)
        if title_element:
            return title_element
        
        for xpath in ["./ancestor::span[@class='asset-entry-title']", 
                      "./parent::span[@class='asset-entry-title']"]:
            try:
                return element.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                continue
        return None
    
    def find_search_box(self):
        """Encontrar la barra de búsqueda"""
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
        """Buscar un término"""
        search_box = self.find_search_box()
        search_box.clear()
        search_box.send_keys(termino)
        search_box.send_keys(Keys.RETURN)
        
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.asset-entry-title, a[href*='xlsm'], .search-results")
            ))
        except TimeoutException:
            time.sleep(self.timings.short_wait)
    
    def find_results(self, termino):
        """Encontrar resultados de búsqueda"""
        resultados = []
        
        # Buscar por títulos de assets
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
        
        # Fallbacks
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
            if palabras_clave:
                keyword = next((w for w in palabras_clave if len(w) > 3), palabras_clave[0])
                resultados = self.driver.find_elements(By.PARTIAL_LINK_TEXT, keyword)
        
        return resultados
    
    def extract_result_info(self, element):
        """Extraer información de un resultado"""
        info = {'titulo': '', 'href': ''}
        
        try:
            title_element = self._get_title_element(element)
            info['titulo'] = title_element.text.strip() if title_element else element.text.strip()
            
            try:
                info['href'] = element.get_attribute('href')
            except:
                pass
                
        except Exception as e:
            print(f"   -> Error extrayendo info: {e}")
        
        return info
    
    def select_best_result(self, resultados, termino):
        """Seleccionar el mejor resultado basado en coincidencia"""
        if not resultados:
            return None
        
        termino_lower = termino.lower()
        palabras_termino = [p for p in termino_lower.split() if len(p) > 2]
        
        mejor_score = -1
        mejor_resultado = resultados[0]
        
        for resultado in resultados:
            try:
                title_element = self._get_title_element(resultado)
                texto = title_element.text.strip() if title_element else resultado.text.strip()
                
                if not texto:
                    continue
                
                texto_lower = texto.lower()
                score = 0
                
                # Bonus por highlights
                if title_element:
                    try:
                        score += len(title_element.find_elements(By.CSS_SELECTOR, "span.highlight")) * 500
                    except NoSuchElementException:
                        pass
                
                # Coincidencia exacta
                if termino_lower in texto_lower:
                    score += 2000
                
                # Palabras encontradas
                palabras_encontradas = sum(1 for p in palabras_termino if p in texto_lower)
                score += palabras_encontradas * 100
                
                if palabras_termino and palabras_encontradas / len(palabras_termino) > 0.8:
                    score += 300
                
                if score > mejor_score:
                    mejor_score = score
                    mejor_resultado = resultado
                    
            except StaleElementReferenceException:
                continue
            except Exception:
                continue
        
        return mejor_resultado

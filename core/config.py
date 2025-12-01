"""
CoorpiBot - Configuración
Carga de configuración y tiempos
"""
from . import database as db


class TimingConfig:
    """Configuración de tiempos de espera"""
    
    def __init__(self):
        config = db.get_all_config()
        
        self.short_wait = max(0.3, float(config.get('TIMING_SHORT_WAIT', '0.3')))
        self.medium_wait = max(1.0, float(config.get('TIMING_MEDIUM_WAIT', '1.0')))
        self.long_wait = max(2.0, float(config.get('TIMING_LONG_WAIT', '2')))
        self.page_load_timeout = max(60, int(float(config.get('TIMING_PAGE_LOAD', '90'))))
        self.explicit_wait = max(15, int(float(config.get('TIMING_EXPLICIT_WAIT', '18'))))
        self.download_timeout = int(float(config.get('TIMING_DOWNLOAD_TIMEOUT', '35')))


class ConfigLoader:
    """Cargador de configuración principal"""
    
    def __init__(self):
        config = db.get_all_config()
        creds = db.get_credentials()
        
        self.usuario = creds.get('usuario', '')
        self.clave = creds.get('clave', '')
        self.url_login = config.get('URL_LOGIN', '')
        self.url_buscador = config.get('URL_BUSCADOR', '')
        self.id_barra_busqueda = config.get('ID_BARRA_BUSQUEDA', '_3_keywords')
        self.debug_mode = config.get('DEBUG_MODE', 'false').lower() == 'true'
        self.proxy_enabled = config.get('PROXY_ENABLED', 'false').lower() == 'true'
        self.proxy_host = config.get('PROXY_HOST', '')
        self.proxy_port = config.get('PROXY_PORT', '')
        self.lista_busqueda = []
        self.timings = TimingConfig()
        
        self._validate_credentials()
        self._load_search_terms()
    
    def _validate_credentials(self):
        if not self.usuario or not self.clave:
            print("ERROR: No se encontraron las credenciales.")
            print("Configura las credenciales en CoorpiBot (pestaña Ajustes)")
            exit(1)
    
    def _load_search_terms(self):
        self.lista_busqueda = db.get_terms()
        if not self.lista_busqueda:
            print("[ERROR CRITICO] No se encontraron términos de búsqueda.")
            exit(1)

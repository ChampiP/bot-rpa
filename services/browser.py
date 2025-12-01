"""
CoorpiBot - Servicio de Navegador
Configuración de Chrome
"""
from selenium.webdriver.chrome.options import Options


class ChromeConfigurator:
    """Configurador de opciones de Chrome"""
    
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

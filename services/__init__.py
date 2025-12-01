"""
CoorpiBot - Services Module
Servicios del bot
"""
from .browser import ChromeConfigurator
from .search import SearchEngine
from .downloader import DownloadManager
from .auth import AuthService

__all__ = ['ChromeConfigurator', 'SearchEngine', 'DownloadManager', 'AuthService']

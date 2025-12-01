"""
CoorpiBot - Módulo de Base de Datos SQLite
Almacena credenciales, términos de búsqueda y configuración
"""
import sqlite3
import os
import sys
from typing import List, Dict

# Detectar si se ejecuta como .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    DB_DIR = os.path.join(os.path.expanduser('~'), '.coorpibot')
else:
    DB_DIR = os.path.dirname(os.path.dirname(__file__))

os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'coorpibot.db')

# Términos por defecto
DEFAULT_TERMS = [
    "Oferta Comercial Postpago y Colaborador Resumen Nota de Producto",
    "Bloqueo de Línea y Equipo Diagrama",
    "Migración de Plan Móvil Prepago y Postpago Diagrama",
    "Guía de Atención para Cuestionamientos de Cobros en Recibos Móvil Masivo",
    "Descartes AT Móvil Canal Telefónico Primer Nivel Postpago",
    "Problemas de Pago Diagrama",
    "Contención de Bajas Diagrama",
    "Guía de Recomendación Comercial y Ventas",
    "Reclamos Móvil Diagrama",
    "Resumen de Agregadores",
    "Ajustes de NC ND DCAJ y OCC Diagrama",
    "Solución Anticipada de Reclamos SAR Diagrama",
    "Gestión de Cobranza Diagrama",
    "Gestión de Cobranza Equipos con Deuda Diagrama",
    "Horarios y Responsables de los Centros de Atención"
]

# Configuración por defecto
DEFAULT_CONFIG = {
    "URL_LOGIN": "http://portaldeconocimiento.claro.com.pe/web/guest/login",
    "URL_BUSCADOR": "http://portaldeconocimiento.claro.com.pe/comunicaciones-internas",
    "ID_BARRA_BUSQUEDA": "_3_keywords",
    "DEBUG_MODE": "false",
    "PROXY_ENABLED": "false",
    "PROXY_HOST": "",
    "PROXY_PORT": "",
    "TIMING_SHORT_WAIT": "0.3",
    "TIMING_MEDIUM_WAIT": "1.0",
    "TIMING_LONG_WAIT": "2",
    "TIMING_PAGE_LOAD": "90",
    "TIMING_EXPLICIT_WAIT": "18",
    "TIMING_DOWNLOAD_TIMEOUT": "35",
    "TIMING_RATE_LIMIT": "0.5",
    "TIMING_RETRY_DELAY": "2"
}


class Database:
    """Clase Singleton para manejar la base de datos SQLite"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL DEFAULT '',
                clave TEXT NOT NULL DEFAULT ''
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL,
                position INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('SELECT COUNT(*) FROM credentials')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO credentials (id, usuario, clave) VALUES (1, "", "")')
        
        for key, value in DEFAULT_CONFIG.items():
            cursor.execute('INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)', (key, value))
        
        cursor.execute('SELECT COUNT(*) FROM terms')
        if cursor.fetchone()[0] == 0:
            for i, term in enumerate(DEFAULT_TERMS):
                cursor.execute('INSERT INTO terms (term, position) VALUES (?, ?)', (term, i))
        
        conn.commit()
        conn.close()
    
    # Credenciales
    def get_credentials(self) -> Dict[str, str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT usuario, clave FROM credentials WHERE id = 1')
        row = cursor.fetchone()
        conn.close()
        return {'usuario': row['usuario'], 'clave': row['clave']} if row else {'usuario': '', 'clave': ''}
    
    def save_credentials(self, usuario: str, clave: str) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE credentials SET usuario = ?, clave = ? WHERE id = 1', (usuario, clave))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
    
    # Configuración
    def get_config(self, key: str, default: str = '') -> str:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM config WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        return row['value'] if row else default
    
    def get_all_config(self) -> Dict[str, str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM config')
        rows = cursor.fetchall()
        conn.close()
        
        config = {row['key']: row['value'] for row in rows}
        creds = self.get_credentials()
        config['CLARO_USUARIO'] = creds['usuario']
        config['CLARO_CLAVE'] = creds['clave']
        return config
    
    def save_config(self, key: str, value: str) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, value))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
    
    def save_all_config(self, config: Dict[str, str]) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            for key, value in config.items():
                if key not in ('CLARO_USUARIO', 'CLARO_CLAVE'):
                    cursor.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, value))
            
            if 'CLARO_USUARIO' in config or 'CLARO_CLAVE' in config:
                creds = self.get_credentials()
                cursor.execute(
                    'UPDATE credentials SET usuario = ?, clave = ? WHERE id = 1',
                    (config.get('CLARO_USUARIO', creds['usuario']), config.get('CLARO_CLAVE', creds['clave']))
                )
            
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
    
    # Términos
    def get_terms(self) -> List[str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT term FROM terms ORDER BY position')
        rows = cursor.fetchall()
        conn.close()
        return [row['term'] for row in rows]
    
    def save_terms(self, terms: List[str]) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM terms')
            for i, term in enumerate(terms):
                cursor.execute('INSERT INTO terms (term, position) VALUES (?, ?)', (term, i))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False


# Instancia global
db = Database()

# Funciones de acceso rápido
def get_credentials() -> Dict[str, str]:
    return db.get_credentials()

def save_credentials(usuario: str, clave: str) -> bool:
    return db.save_credentials(usuario, clave)

def get_config(key: str, default: str = '') -> str:
    return db.get_config(key, default)

def get_all_config() -> Dict[str, str]:
    return db.get_all_config()

def save_config(key: str, value: str) -> bool:
    return db.save_config(key, value)

def save_all_config(config: Dict[str, str]) -> bool:
    return db.save_all_config(config)

def get_terms() -> List[str]:
    return db.get_terms()

def save_terms(terms: List[str]) -> bool:
    return db.save_terms(terms)

def get_db_path() -> str:
    return DB_PATH

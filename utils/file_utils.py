"""
CoorpiBot - Utilidades de Archivos
Gestión de directorios y desbloqueo de archivos
"""
import os
import subprocess


class DirectoryManager:
    """Gestión de directorios de descarga"""
    
    def __init__(self):
        self.download_dir = self._get_download_directory()
    
    def _get_download_directory(self):
        default_downloads = os.path.join(
            os.environ.get('USERPROFILE', os.getcwd()), 
            'Downloads'
        )
        return os.path.abspath(default_downloads)
    
    def get_files_snapshot(self):
        """Obtener snapshot de archivos actuales"""
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
    """Desbloqueo de archivos descargados de Internet"""
    
    @staticmethod
    def unblock_file(file_path):
        """Desbloquear archivo para habilitar macros"""
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

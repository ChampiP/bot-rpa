"""Interfaz grafica de usuario para el Bot RPA Claro"""

import os
import json
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk


CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
TERMS_FILE = os.path.join(CONFIG_DIR, 'terms.json')
ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')

DEFAULT_TERMS = [
    "Migracion de plan",
    "Guia de cuestionamiento para cobro de recibo",
    "Bloqueo de linea y equipo",
    "Gestion de cobranza",
    "Guia de recomendacion comercial y ventas",
    "Descartes at",
    "contencion de bajas"
]

class BotGUI(tk.Tk):
    """Interfaz grafica principal del bot"""
    
    def __init__(self):
        super().__init__()
        self.title("Bot RPA Claro - Configuracion y Ejecucion")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Inicializar variables antes de crear la UI
        self.form_entries = {}
        self.search_terms = []
        self.env_config = {}
        
        # Cargar configuracion
        self.load_configuration()
        
        # Configurar interfaz
        self.setup_ui()
    
    def load_configuration(self):
        """Carga la configuracion inicial"""
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.search_terms = self.load_terms()
        self.env_config = self.load_env()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.tabs = ttk.Notebook(self)
        self.tab_terms = ttk.Frame(self.tabs)
        self.tab_settings = ttk.Frame(self.tabs)
        self.tab_run = ttk.Frame(self.tabs)
        
        self.tabs.add(self.tab_terms, text="Terminos")
        self.tabs.add(self.tab_settings, text="Ajustes")
        self.tabs.add(self.tab_run, text="Ejecutar")
        self.tabs.pack(fill=tk.BOTH, expand=True)
        
        self.build_terms_tab()
        self.build_settings_tab()
        self.build_run_tab()

    def load_terms(self):
        """Carga los terminos de busqueda desde el archivo JSON"""
        try:
            with open(TERMS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('lista_busqueda', DEFAULT_TERMS)
        except Exception:
            return DEFAULT_TERMS.copy()

    def save_terms(self):
        """Guarda los terminos de busqueda en el archivo JSON"""
        try:
            with open(TERMS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"lista_busqueda": self.search_terms}, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Guardado", "Terminos guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def load_env(self):
        """Carga las variables de entorno desde el archivo .env"""
        env = {
            "CLARO_USUARIO": "",
            "CLARO_CLAVE": "",
            "URL_LOGIN": "http://portaldeconocimiento.claro.com.pe/web/guest/login",
            "URL_BUSCADOR": "http://portaldeconocimiento.claro.com.pe/comunicaciones-internas",
            "ID_BARRA_BUSQUEDA": "_3_keywords"
        }
        try:
            if os.path.exists(ENV_FILE):
                with open(ENV_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env[key] = value
        except Exception:
            pass
        return env

    def save_env(self):
        """Guarda las variables de entorno en el archivo .env"""
        try:
            with open(ENV_FILE, 'w', encoding='utf-8') as f:
                f.write("# Credenciales y ajustes del Bot RPA\n")
                env_keys = ["CLARO_USUARIO", "CLARO_CLAVE", "URL_LOGIN", 
                           "URL_BUSCADOR", "ID_BARRA_BUSQUEDA"]
                for key in env_keys:
                    f.write(f"{key}={self.env_config.get(key, '')}\n")
            messagebox.showinfo("Guardado", ".env actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar .env: {e}")

    def build_terms_tab(self):
        """Construye la pestana de terminos de busqueda"""
        frame = self.tab_terms

        label = ttk.Label(frame, text="Lista de terminos a buscar (uno por linea):")
        label.pack(anchor=tk.W, padx=10, pady=10)

        self.listbox = tk.Listbox(frame, height=15)
        self.listbox.pack(fill=tk.X, padx=10)
        for term in self.search_terms:
            self.listbox.insert(tk.END, term)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        buttons = [
            ("Agregar", self.add_term),
            ("Editar", self.edit_term),
            ("Eliminar", self.delete_term),
            ("Subir", lambda: self.move_term(-1)),
            ("Bajar", lambda: self.move_term(1))
        ]
        
        for text, command in buttons:
            ttk.Button(btn_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Guardar", command=self.save_terms).pack(side=tk.RIGHT, padx=5)

    def add_term(self):
        """Agrega un nuevo termino de busqueda"""
        term = simpledialog.askstring("Agregar termino", "Nuevo termino de busqueda:")
        if term:
            self.search_terms.append(term)
            self.listbox.insert(tk.END, term)

    def edit_term(self):
        """Edita un termino de busqueda existente"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selecciona", "Seleccione un termino para editar.")
            return
        
        index = selection[0]
        current = self.search_terms[index]
        term = simpledialog.askstring("Editar termino", "Nuevo valor:", initialvalue=current)
        
        if term is not None:
            self.search_terms[index] = term
            self.listbox.delete(index)
            self.listbox.insert(index, term)

    def delete_term(self):
        """Elimina un termino de busqueda"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        self.listbox.delete(index)
        del self.search_terms[index]

    def move_term(self, direction):
        """Mueve un termino arriba o abajo en la lista"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        current_index = selection[0]
        new_index = current_index + direction
        
        if 0 <= new_index < len(self.search_terms):
            self.search_terms[current_index], self.search_terms[new_index] = \
                self.search_terms[new_index], self.search_terms[current_index]
            
            self.listbox.delete(current_index)
            self.listbox.insert(current_index, self.search_terms[current_index])
            self.listbox.delete(new_index)
            self.listbox.insert(new_index, self.search_terms[new_index])
            
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(new_index)

    def build_settings_tab(self):
        """Construye la pestana de ajustes"""
        frame = self.tab_settings
        
        # Titulo y descripcion
        title_label = ttk.Label(
            frame, 
            text="Configuracion de Credenciales y URLs", 
            font=("Arial", 12, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W)
        
        info_label = ttk.Label(
            frame, 
            text="Modifica las credenciales y configuraciones del bot:",
            font=("Arial", 9)
        )
        info_label.grid(row=1, column=0, columnspan=2, pady=(0, 15), padx=10, sticky=tk.W)

        fields = [
            ("Usuario", "CLARO_USUARIO", False),
            ("Contrasena", "CLARO_CLAVE", True),
            ("URL Login", "URL_LOGIN", False),
            ("URL Buscador", "URL_BUSCADOR", False),
            ("ID Barra Busqueda", "ID_BARRA_BUSQUEDA", False),
        ]

        for index, (label, key, is_password) in enumerate(fields):
            row = index + 2  # +2 porque hay titulo y descripcion
            
            ttk.Label(frame, text=f"{label}:", font=("Arial", 9, "bold")).grid(
                row=row, column=0, sticky=tk.W, padx=10, pady=8
            )
            
            if is_password:
                entry = ttk.Entry(frame, width=60, show="*")
            else:
                entry = ttk.Entry(frame, width=60)
            
            entry.grid(row=row, column=1, padx=10, pady=8)
            entry.insert(0, self.env_config.get(key, ''))
            self.form_entries[key] = entry
        
        # Frame para botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields) + 2, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame, 
            text="Guardar Configuracion", 
            command=self.on_save_env,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Mostrar/Ocultar Contrasena",
            command=self.toggle_password,
            width=25
        ).pack(side=tk.LEFT, padx=5)
        
        # Nota informativa
        note_label = ttk.Label(
            frame,
            text="Nota: Los cambios se guardaran en el archivo .env",
            font=("Arial", 8, "italic"),
            foreground="gray"
        )
        note_label.grid(row=len(fields) + 3, column=0, columnspan=2, pady=5)

    def on_save_env(self):
        """Guarda las configuraciones del formulario"""
        # Validar que usuario y contrasena no esten vacios
        usuario = self.form_entries["CLARO_USUARIO"].get().strip()
        clave = self.form_entries["CLARO_CLAVE"].get().strip()
        
        if not usuario or not clave:
            messagebox.showwarning(
                "Campos Incompletos",
                "Usuario y Contrasena son obligatorios."
            )
            return
        
        for key, entry in self.form_entries.items():
            self.env_config[key] = entry.get()
        self.save_env()
    
    def toggle_password(self):
        """Muestra u oculta la contrasena"""
        password_entry = self.form_entries["CLARO_CLAVE"]
        current_show = password_entry.cget("show")
        
        if current_show == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    def build_run_tab(self):
        """Construye la pestana de ejecucion"""
        frame = self.tab_run
        
        # Titulo
        title_label = ttk.Label(
            frame,
            text="Ejecutar Bot RPA",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=20)
        
        # Instrucciones
        instructions = ttk.Label(
            frame,
            text="Presiona el boton para iniciar el proceso de descarga automatica.\n"
                 "El bot cerrara Chrome automaticamente si esta abierto.",
            font=("Arial", 10),
            justify=tk.CENTER
        )
        instructions.pack(pady=10)
        
        # Boton principal de ejecucion
        run_button = ttk.Button(
            frame,
            text="▶ EJECUTAR BOT",
            command=self.run_bot,
            width=30
        )
        run_button.pack(pady=20)
        
        # Frame de informacion
        info_frame = ttk.LabelFrame(frame, text="Informacion", padding=10)
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        info_items = [
            ("📥 Ubicacion de descargas:", f"{os.environ.get('USERPROFILE', '')}\\Downloads"),
            ("🔧 Configuracion:", "config/terms.json y .env"),
            ("⚙️ Modo:", "Descarga automatica sin intervención")
        ]
        
        for label, value in info_items:
            item_frame = ttk.Frame(info_frame)
            item_frame.pack(fill=tk.X, pady=3)
            ttk.Label(item_frame, text=label, font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            ttk.Label(item_frame, text=value, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        # Nota de advertencia
        warning_label = ttk.Label(
            frame,
            text="⚠️ Asegurate de haber configurado correctamente las credenciales en la pestana 'Ajustes'",
            font=("Arial", 8, "italic"),
            foreground="orange"
        )
        warning_label.pack(pady=10)

    def run_bot(self):
        """Ejecuta el bot en un hilo separado"""
        # Verificar que existan credenciales antes de ejecutar
        if not self.env_config.get("CLARO_USUARIO") or not self.env_config.get("CLARO_CLAVE"):
            response = messagebox.askyesno(
                "Credenciales no configuradas",
                "No se encontraron credenciales configuradas.\n"
                "¿Deseas ir a la pestana de Ajustes para configurarlas?"
            )
            if response:
                self.tabs.select(1)  # Seleccionar pestana de Ajustes
            return
        
        # Confirmar ejecucion
        response = messagebox.askyesno(
            "Confirmar Ejecucion",
            "¿Estas seguro de que deseas ejecutar el bot?\n"
            "Chrome se cerrara automaticamente si esta abierto."
        )
        
        if not response:
            return
        
        def execute_bot():
            try:
                # Cerrar Chrome
                subprocess.run(
                    ["taskkill", "/F", "/IM", "chrome.exe", "/T"], 
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                # Ejecutar el bot
                index_path = os.path.join(os.path.dirname(__file__), "index.py")
                
                # Crear una nueva ventana de terminal para ver el progreso
                if os.name == 'nt':  # Windows
                    subprocess.Popen(
                        ["cmd", "/c", "start", "cmd", "/k", "python", index_path],
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    subprocess.Popen(["python", index_path])
                
                messagebox.showinfo(
                    "Bot Iniciado",
                    "El bot se esta ejecutando en una ventana de terminal.\n"
                    "Puedes cerrar esta ventana sin afectar el proceso."
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo ejecutar el bot: {e}")
        
        threading.Thread(target=execute_bot, daemon=True).start()

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()

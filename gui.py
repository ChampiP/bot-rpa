import os
import sys
import threading
import subprocess
import webbrowser
import requests
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from core import database as db

VERSION = "2.6.0"
GITHUB_REPO = "ChampiP/bot-rpa"


class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🤖 CoorpiBot")
        
        # Configurar colores modernos
        self.configure(bg='#f5f5f5')
        
        # Estilo moderno
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('TNotebook', background='#f5f5f5', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[15, 8], font=('Segoe UI', 9, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#2196F3')], foreground=[('selected', 'white')])
        style.configure('TFrame', background='#ffffff')
        style.configure('TLabel', background='#ffffff', font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9, 'bold'), padding=8)
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Interfaz más compacta
        min_width = 650
        min_height = 480
        default_width = 720
        default_height = 540
        
        # Centrar ventana en la pantalla
        x = (screen_width - default_width) // 2
        y = (screen_height - default_height) // 2
        
        self.geometry(f"{default_width}x{default_height}+{x}+{y}")
        self.minsize(min_width, min_height)
        self.resizable(True, True)
        
        self.form_entries = {}
        self.search_terms = []
        self.env_config = {}
        
        self.load_configuration()
        self.setup_ui()
    
    def load_configuration(self):
        # Cargar configuración desde SQLite
        self.search_terms = db.get_terms()
        self.env_config = db.get_all_config()
    
    def setup_ui(self):
        self.tabs = ttk.Notebook(self)
        self.tab_terms = ttk.Frame(self.tabs)
        self.tab_settings = ttk.Frame(self.tabs)
        self.tab_run = ttk.Frame(self.tabs)
        self.tab_instructions = ttk.Frame(self.tabs)
        
        self.tabs.add(self.tab_terms, text="📋 Términos")
        self.tabs.add(self.tab_settings, text="⚙️ Ajustes")
        self.tabs.add(self.tab_run, text="🚀 Ejecutar")
        self.tabs.add(self.tab_instructions, text="📖 Instrucciones")
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.build_terms_tab()
        self.build_settings_tab()
        self.build_run_tab()
        self.build_instructions_tab()

    def save_terms(self):
        """Guarda términos en SQLite"""
        if db.save_terms(self.search_terms):
            messagebox.showinfo("✅ Guardado", "Términos guardados correctamente.", icon='info')
        else:
            messagebox.showerror("Error", "No se pudieron guardar los términos.")

    def save_env(self):
        """Guarda configuración en SQLite"""
        try:
            # Guardar credenciales
            db.save_credentials(
                self.env_config.get("CLARO_USUARIO", ""),
                self.env_config.get("CLARO_CLAVE", "")
            )
            # Guardar resto de configuración
            db.save_all_config(self.env_config)
            messagebox.showinfo("Guardado", "Configuración actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {e}")

    def build_terms_tab(self):
        frame = self.tab_terms
        frame.configure(style='TFrame')
        
        # Header más compacto
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill=tk.X, padx=15, pady=(10, 8))
        
        label = tk.Label(header_frame, text="📋 Términos a buscar:", font=("Segoe UI", 10, "bold"), bg='#ffffff', fg='#2196F3')
        label.pack(anchor=tk.W)
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set, 
            font=("Segoe UI", 9),
            bg='#ffffff',
            fg='#333333',
            selectbackground='#2196F3',
            selectforeground='white',
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightcolor='#2196F3',
            highlightbackground='#ddd'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        for term in self.search_terms:
            self.listbox.insert(tk.END, term)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Botones de edición
        edit_frame = ttk.Frame(btn_frame)
        edit_frame.pack(side=tk.LEFT)
        
        buttons = [
            ("➕ Agregar", self.add_term),
            ("✏️ Editar", self.edit_term),
            ("🗑️ Eliminar", self.delete_term),
            ("⬆️ Subir", lambda: self.move_term(-1)),
            ("⬇️ Bajar", lambda: self.move_term(1))
        ]
        
        for text, command in buttons:
            btn = ttk.Button(edit_frame, text=text, command=command, width=10)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Botón guardar destacado
        save_btn = ttk.Button(btn_frame, text="💾 Guardar", command=self.save_terms, width=12)
        save_btn.pack(side=tk.RIGHT, padx=3)

    def add_term(self):
        term = simpledialog.askstring("Agregar termino", "Nuevo termino de busqueda:")
        if term:
            self.search_terms.append(term)
            self.listbox.insert(tk.END, term)

    def edit_term(self):
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
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        self.listbox.delete(index)
        del self.search_terms[index]

    def move_term(self, direction):
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
        frame = self.tab_settings
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        title_label = ttk.Label(
            scrollable_frame, 
            text="Configuracion de Credenciales y URLs", 
            font=("Segoe UI", 10, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=8, padx=10, sticky=tk.W)
        
        fields = [
            ("Usuario", "CLARO_USUARIO", False),
            ("Contrasena", "CLARO_CLAVE", True),
            ("URL Login", "URL_LOGIN", False),
            ("URL Buscador", "URL_BUSCADOR", False),
            ("ID Barra Busqueda", "ID_BARRA_BUSQUEDA", False),
        ]

        for index, (label, key, is_password) in enumerate(fields):
            row = index + 1
            
            ttk.Label(scrollable_frame, text=f"{label}:", font=("Segoe UI", 9, "bold")).grid(
                row=row, column=0, sticky=tk.W, padx=10, pady=5
            )
            
            if is_password:
                entry = ttk.Entry(scrollable_frame, width=50, show="*")
            else:
                entry = ttk.Entry(scrollable_frame, width=50)
            
            entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.EW)
            entry.insert(0, self.env_config.get(key, ''))
            self.form_entries[key] = entry
        
        scrollable_frame.columnconfigure(1, weight=1)
        
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=12)
        
        ttk.Button(
            btn_frame, 
            text="💾 Guardar Configuracion", 
            command=self.on_save_env,
            width=22
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="👁️ Mostrar/Ocultar Contrasena",
            command=self.toggle_password,
            width=26
        ).pack(side=tk.LEFT, padx=5)
        
        note_label = ttk.Label(
            scrollable_frame,
            text="Nota: Los cambios se guardaran en la base de datos local (SQLite)",
            font=("Segoe UI", 8, "italic"),
            foreground="gray"
        )
        note_label.grid(row=len(fields) + 2, column=0, columnspan=2, pady=8)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



    def on_save_env(self):
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
        
        # Aplicar valores ultra rápidos automáticos
        self.env_config["DEBUG_MODE"] = "false"
        self.env_config["PROXY_ENABLED"] = "false"
        self.env_config["PROXY_HOST"] = ""
        self.env_config["PROXY_PORT"] = ""
        self.env_config["TIMING_SHORT_WAIT"] = "0.3"
        self.env_config["TIMING_MEDIUM_WAIT"] = "1.0"
        self.env_config["TIMING_LONG_WAIT"] = "2"
        self.env_config["TIMING_PAGE_LOAD"] = "90"
        self.env_config["TIMING_EXPLICIT_WAIT"] = "18"
        self.env_config["TIMING_DOWNLOAD_TIMEOUT"] = "35"
        self.env_config["TIMING_RATE_LIMIT"] = "0.5"
        self.env_config["TIMING_RETRY_DELAY"] = "2"
        
        self.save_env()
    
    def toggle_password(self):
        password_entry = self.form_entries["CLARO_CLAVE"]
        current_show = password_entry.cget("show")
        
        if current_show == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    def build_run_tab(self):
        frame = self.tab_run
        frame.configure(style='TFrame')
        
        # Header azul
        header_frame = tk.Frame(frame, bg='#2196F3', height=50)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🤖 CoorpiBot",
            font=("Segoe UI", 14, "bold"),
            bg='#2196F3',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Contenedor principal centrado
        main_container = tk.Frame(frame, bg='#ffffff')
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Sección de Créditos
        credits_frame = tk.Frame(main_container, bg='#f8f8f8', relief=tk.RIDGE, borderwidth=1)
        credits_frame.pack(pady=15, padx=40, fill=tk.X)
        
        copyright_title = tk.Label(
            credits_frame,
            text="© Copyright & Créditos",
            font=("Segoe UI", 11, "bold"),
            bg='#f8f8f8',
            fg='#00bcd4',
            pady=10
        )
        copyright_title.pack()
        
        author_label = tk.Label(
            credits_frame,
            text="👤 Autor: ChampiP",
            font=("Segoe UI", 9, "bold"),
            bg='#f8f8f8',
            fg='#333333',
            pady=3
        )
        author_label.pack()
        
        github_label = tk.Label(
            credits_frame,
            text="🔗 GitHub: https://github.com/ChampiP",
            font=("Segoe UI", 9),
            bg='#f8f8f8',
            fg='#1976D2',
            cursor='hand2',
            pady=3
        )
        github_label.pack()
        
        def open_github(e):
            webbrowser.open('https://github.com/ChampiP')
        
        github_label.bind('<Button-1>', open_github)
        
        whatsapp_label = tk.Label(
            credits_frame,
            text="📞 Contacto WhatsApp: +51 946 674 643",
            font=("Segoe UI", 9, "bold"),
            bg='#f8f8f8',
            fg='#25D366',
            cursor='hand2',
            pady=3
        )

        def open_whatsapp(event=None):
            webbrowser.open('https://wa.me/51946674643?text=Hola%20tengo%20una%20consulta%20sobre%20CoorpiBot')

        whatsapp_label.bind("<Button-1>", open_whatsapp)
        whatsapp_label.pack()
        
        version_label = tk.Label(
            credits_frame,
            text="🔰 CoorpiBot v2.6",
            font=("Segoe UI", 8),
            bg='#f8f8f8',
            fg='#666666',
            pady=5
        )
        version_label.pack()
        
        copyright_label = tk.Label(
            credits_frame,
            text="© 2025 ChampiP. Todos los derechos reservados.",
            font=("Segoe UI", 8, "italic"),
            bg='#f8f8f8',
            fg='#999999',
            pady=8
        )
        copyright_label.pack()
        
        # Botón de ejecución
        button_frame = tk.Frame(main_container, bg='#ffffff')
        button_frame.pack(pady=20)
        
        run_button = tk.Button(
            button_frame,
            text="▶  EJECUTAR BOT",
            command=self.run_bot,
            font=("Segoe UI", 11, "bold"),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.FLAT,
            padx=50,
            pady=14,
            cursor='hand2',
            borderwidth=0
        )
        run_button.pack()
        
        def on_enter(e):
            run_button['bg'] = '#45a049'
        def on_leave(e):
            run_button['bg'] = '#4CAF50'
        
        run_button.bind('<Enter>', on_enter)
        run_button.bind('<Leave>', on_leave)
        
        # Información al final
        info_frame = ttk.LabelFrame(main_container, text="Información", padding=8)
        info_frame.pack(pady=10, padx=40, fill=tk.X)
        
        info_items = [
            ("📥 Descargas:", f"C:\\Users\\tu usuario\\Downloads"),
            ("🔧 Config:", f"Base de datos SQLite ({db.get_db_path()})")
        ]
        
        for label, value in info_items:
            item_frame = ttk.Frame(info_frame)
            item_frame.pack(fill=tk.X, pady=2)
            ttk.Label(item_frame, text=label, font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT)
            ttk.Label(item_frame, text=value, font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=5)
        
        warning_label = ttk.Label(
            main_container,
            text="⚠️ Configura las credenciales en 'Ajustes'",
            font=("Segoe UI", 8, "italic"),
            foreground="orange"
        )
        warning_label.pack(pady=5)

    def run_bot(self):
        if not self.env_config.get("CLARO_USUARIO") or not self.env_config.get("CLARO_CLAVE"):
            response = messagebox.askyesno(
                "Credenciales no configuradas",
                "No se encontraron credenciales configuradas.\n"
                "¿Deseas ir a la pestana de Ajustes para configurarlas?"
            )
            if response:
                self.tabs.select(1)
            return
        
        response = messagebox.askyesno(
            "Confirmar Ejecucion",
            "¿Estas seguro de que deseas ejecutar el bot?\n"
            "Chrome se cerrara automaticamente si esta abierto."
        )
        
        if not response:
            return
        
        def execute_bot():
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "chrome.exe", "/T"], 
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                # Si está ejecutándose como .exe, importar y ejecutar directamente
                if getattr(sys, 'frozen', False):
                    def run_bot_module():
                        try:
                            from bot import main
                            main()
                        except Exception as e:
                            messagebox.showerror("Error", f"Error al ejecutar el bot: {e}")
                    
                    threading.Thread(target=run_bot_module, daemon=False).start()
                    
                    messagebox.showinfo(
                        "Bot Iniciado",
                        "El bot se esta ejecutando en segundo plano.\n"
                        "Revisa la carpeta Downloads para ver los archivos descargados."
                    )
                else:
                    # Modo desarrollo: ejecutar bot.py con Python
                    bot_path = os.path.join(os.path.dirname(__file__), "bot.py")
                    
                    if os.name == 'nt':
                        subprocess.Popen(
                            ["cmd", "/c", "start", "cmd", "/k", "python", bot_path],
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
                    else:
                        subprocess.Popen(["python", bot_path])
                    
                    messagebox.showinfo(
                        "Bot Iniciado",
                        "El bot se esta ejecutando en una ventana de terminal.\n"
                        "Puedes cerrar esta ventana sin afectar el proceso."
                    )
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo ejecutar el bot: {e}")
        
        threading.Thread(target=execute_bot, daemon=True).start()
    
    def build_instructions_tab(self):
        frame = self.tab_instructions
        frame.configure(style='TFrame')
        
        # Contenedor con scroll
        canvas = tk.Canvas(frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header = tk.Label(
            scrollable_frame,
            text="📖 Instrucciones de Uso",
            font=("Segoe UI", 12, "bold"),
            bg='#ffffff',
            fg='#2196F3',
            pady=10
        )
        header.pack(pady=(10, 5))
        
        # Instrucciones
        instructions_text = """1️⃣ Configurar Credenciales:
   Ve a la pestaña "Ajustes" e ingresa tu usuario y contraseña.

2️⃣ Gestionar Términos:
   En "Términos" puedes agregar, editar o eliminar términos de búsqueda.

3️⃣ Ejecutar el Bot:
   En "Ejecutar", presiona el botón verde para iniciar.
   El bot buscará y descargará automáticamente los archivos.

4️⃣ Revisar Descargas:
   Los archivos se guardan en tu carpeta de Descargas.

⚠️ Importante:
   • Chrome se cerrará automáticamente al ejecutar el bot
   • Asegúrate de tener una conexión estable a Internet
   • No cierres el bot mientras está en ejecución"""
        
        instructions_label = tk.Label(
            scrollable_frame,
            text=instructions_text,
            font=("Segoe UI", 9),
            bg='#ffffff',
            fg='#333333',
            justify=tk.LEFT,
            padx=20,
            pady=10
        )
        instructions_label.pack(pady=5)
        
        # Separador
        separator = ttk.Separator(scrollable_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=20, pady=15)
        
        # Sección de Actualizaciones
        update_frame = tk.Frame(scrollable_frame, bg='#e3f2fd', relief=tk.RIDGE, borderwidth=1)
        update_frame.pack(fill=tk.X, padx=20, pady=10)
        
        update_title = tk.Label(
            update_frame,
            text="🔄 Actualizaciones",
            font=("Segoe UI", 10, "bold"),
            bg='#e3f2fd',
            fg='#1976D2',
            pady=8
        )
        update_title.pack()
        
        version_label = tk.Label(
            update_frame,
            text=f"Versión actual: v{VERSION}",
            font=("Segoe UI", 9),
            bg='#e3f2fd',
            fg='#555555'
        )
        version_label.pack()
        
        update_btn = tk.Button(
            update_frame,
            text="🔍 Buscar Actualizaciones",
            command=self.check_for_updates,
            font=("Segoe UI", 9, "bold"),
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        update_btn.pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def check_for_updates(self):
        """Verificar si hay actualizaciones disponibles en GitHub"""
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('tag_name', '').lstrip('v')
                current_version = VERSION.lstrip('v')
                
                if latest_version and latest_version > current_version:
                    result = messagebox.askyesno(
                        "🎉 Nueva Versión Disponible",
                        f"¡Hay una nueva versión disponible!\n\n"
                        f"Tu versión: v{current_version}\n"
                        f"Nueva versión: v{latest_version}\n\n"
                        f"¿Deseas ir a la página de descarga?"
                    )
                    if result:
                        webbrowser.open(f"https://github.com/{GITHUB_REPO}/releases/latest")
                else:
                    messagebox.showinfo(
                        "✅ Actualizado",
                        f"¡Tienes la última versión!\n\nVersión actual: v{current_version}"
                    )
            elif response.status_code == 404:
                messagebox.showinfo(
                    "Sin Releases",
                    "Aún no hay versiones publicadas en GitHub.\n"
                    "Visita el repositorio para más información."
                )
            else:
                raise Exception(f"Error HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Tiempo de espera agotado.\nVerifica tu conexión a Internet.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se pudo conectar a Internet.\nVerifica tu conexión.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo verificar actualizaciones:\n{e}")


if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()

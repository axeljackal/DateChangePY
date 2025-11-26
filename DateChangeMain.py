import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import platform
from datetime import datetime
from pathlib import Path

class DateChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cambiador de Fechas de Archivos")
        self.root.geometry("700x600")
        self.files = []
        
        # Formato de fecha por defecto: Argentino
        self.date_format = tk.StringVar(value="Argentino")
        self.format_patterns = {
            "Argentino": "%d-%m-%Y %H:%M:%S",
            "Internacional": "%Y-%m-%d %H:%M:%S"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="📅 Modificador de Fechas de Archivos", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Área de drop de archivos
        drop_frame = ttk.LabelFrame(main_frame, text="Archivos seleccionados", padding="5")
        drop_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        drop_frame.columnconfigure(0, weight=1)
        
        self.listbox = tk.Listbox(drop_frame, height=10, selectmode=tk.EXTENDED)
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar drag & drop
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_files)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(drop_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botones de archivos
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_frame, text="📁 Agregar Archivos", command=self.add_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Agregar Carpeta", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar Lista", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Quitar Seleccionados", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        
        # Frame de fechas
        date_frame = ttk.LabelFrame(main_frame, text="Configurar Fechas", padding="10")
        date_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Selector de formato de fecha
        format_frame = ttk.Frame(date_frame)
        format_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(format_frame, text="🌐 Formato de Fecha:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="🇦🇷 Argentino (DD-MM-AAAA)", 
                       variable=self.date_format, value="Argentino", 
                       command=self.on_format_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="🌍 Internacional (AAAA-MM-DD)", 
                       variable=self.date_format, value="Internacional",
                       command=self.on_format_change).pack(side=tk.LEFT, padx=5)
        
        # Fecha de creación
        ttk.Label(date_frame, text="📅 Fecha de Creación:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        creation_entry_frame = ttk.Frame(date_frame)
        creation_entry_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.creation_date = tk.StringVar(value=datetime.now().strftime(self.get_current_format()))
        ttk.Entry(creation_entry_frame, textvariable=self.creation_date, width=25).pack(side=tk.LEFT)
        ttk.Button(creation_entry_frame, text="Ahora", command=lambda: self.set_now('creation')).pack(side=tk.LEFT, padx=5)
        
        # Fecha de modificación
        ttk.Label(date_frame, text="📝 Fecha de Modificación:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        modified_entry_frame = ttk.Frame(date_frame)
        modified_entry_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.modified_date = tk.StringVar(value=datetime.now().strftime(self.get_current_format()))
        ttk.Entry(modified_entry_frame, textvariable=self.modified_date, width=25).pack(side=tk.LEFT)
        ttk.Button(modified_entry_frame, text="Ahora", command=lambda: self.set_now('modified')).pack(side=tk.LEFT, padx=5)
        
        # Checkbox para mantener fecha de acceso
        self.keep_access = tk.BooleanVar(value=True)
        ttk.Checkbutton(date_frame, text="Mantener fecha de último acceso", 
                       variable=self.keep_access).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Instrucciones de formato
        self.format_label = ttk.Label(date_frame, text=self.get_format_instruction(), 
                 font=('Arial', 8), foreground='gray')
        self.format_label.grid(row=4, column=0, columnspan=2, pady=(0, 5))
        
        # Botón aplicar cambios
        apply_button = ttk.Button(main_frame, text="✅ Aplicar Cambios a Todos los Archivos", 
                                 command=self.apply_changes)
        apply_button.grid(row=4, column=0, columnspan=3, pady=10, ipadx=20, ipady=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Label de estado
        self.status_label = ttk.Label(main_frame, text="🎯 Arrastra archivos aquí o usa 'Agregar Archivos'", 
                                     font=('Arial', 9))
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
    
    def get_current_format(self):
        """Obtiene el patrón de formato actual"""
        return self.format_patterns[self.date_format.get()]
    
    def get_format_instruction(self):
        """Obtiene las instrucciones de formato según el formato seleccionado"""
        if self.date_format.get() == "Argentino":
            return "Formato: DD-MM-AAAA HH:MM:SS (Ejemplo: 26-11-2025 15:30:00)"
        else:
            return "Formato: AAAA-MM-DD HH:MM:SS (Ejemplo: 2025-11-26 15:30:00)"
    
    def on_format_change(self):
        """Actualiza las fechas cuando cambia el formato"""
        try:
            # Intentar parsear las fechas actuales con el formato anterior
            old_format = self.format_patterns["Internacional"] if self.date_format.get() == "Argentino" else self.format_patterns["Argentino"]
            new_format = self.get_current_format()
            
            # Convertir fecha de creación
            try:
                creation_dt = datetime.strptime(self.creation_date.get(), old_format)
                self.creation_date.set(creation_dt.strftime(new_format))
            except ValueError:
                # Si falla, poner fecha actual
                self.creation_date.set(datetime.now().strftime(new_format))
            
            # Convertir fecha de modificación
            try:
                modified_dt = datetime.strptime(self.modified_date.get(), old_format)
                self.modified_date.set(modified_dt.strftime(new_format))
            except ValueError:
                # Si falla, poner fecha actual
                self.modified_date.set(datetime.now().strftime(new_format))
            
            # Actualizar label de formato
            self.format_label.config(text=self.get_format_instruction())
            
        except Exception:
            # En caso de error, resetear a fecha actual
            now = datetime.now().strftime(self.get_current_format())
            self.creation_date.set(now)
            self.modified_date.set(now)
            self.format_label.config(text=self.get_format_instruction())
    
    def set_now(self, date_type):
        """Establece la fecha actual"""
        now = datetime.now().strftime(self.get_current_format())
        if date_type == 'creation':
            self.creation_date.set(now)
        else:
            self.modified_date.set(now)
    
    def drop_files(self, event):
        """Maneja el evento de arrastrar y soltar archivos"""
        files = self.root.tk.splitlist(event.data)
        added_count = 0
        
        for file in files:
            # Limpiar el path (remover llaves si existen)
            file = file.strip('{}')
            
            if os.path.isfile(file):
                if file not in self.files:
                    self.files.append(file)
                    self.listbox.insert(tk.END, file)
                    added_count += 1
            elif os.path.isdir(file):
                # Si es una carpeta, agregar todos los archivos
                for root, dirs, filenames in os.walk(file):
                    for filename in filenames:
                        filepath = os.path.join(root, filename)
                        if filepath not in self.files:
                            self.files.append(filepath)
                            self.listbox.insert(tk.END, filepath)
                            added_count += 1
        
        self.status_label.config(text=f"✅ {len(self.files)} archivo(s) en total - {added_count} agregado(s)")
    
    def add_files(self):
        """Agregar archivos mediante diálogo"""
        files = filedialog.askopenfilenames(title="Seleccionar archivos")
        added_count = 0
        
        for file in files:
            if file not in self.files:
                self.files.append(file)
                self.listbox.insert(tk.END, file)
                added_count += 1
        
        self.status_label.config(text=f"✅ {len(self.files)} archivo(s) en total - {added_count} agregado(s)")
    
    def add_folder(self):
        """Agregar todos los archivos de una carpeta"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta")
        if not folder:
            return
        
        added_count = 0
        for root, dirs, filenames in os.walk(folder):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if filepath not in self.files:
                    self.files.append(filepath)
                    self.listbox.insert(tk.END, filepath)
                    added_count += 1
        
        self.status_label.config(text=f"✅ {len(self.files)} archivo(s) en total - {added_count} agregado(s)")
    
    def remove_selected(self):
        """Quitar archivos seleccionados de la lista"""
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Información", "No hay archivos seleccionados para quitar")
            return
        
        # Eliminar en orden inverso para no afectar los índices
        for index in reversed(selected_indices):
            del self.files[index]
            self.listbox.delete(index)
        
        self.status_label.config(text=f"✅ {len(self.files)} archivo(s) restantes")
    
    def clear_files(self):
        """Limpiar toda la lista"""
        self.files.clear()
        self.listbox.delete(0, tk.END)
        self.status_label.config(text="🗑️ Lista limpiada")
        self.progress['value'] = 0
    
    def apply_changes(self):
        """Aplicar cambios de fecha a todos los archivos"""
        if not self.files:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados")
            return
        
        # Validar formatos de fecha con el formato actual
        current_format = self.get_current_format()
        try:
            creation_dt = datetime.strptime(self.creation_date.get(), current_format)
            modified_dt = datetime.strptime(self.modified_date.get(), current_format)
        except ValueError:
            messagebox.showerror("Error", f"Formato de fecha inválido.\n\n{self.get_format_instruction()}")
            return
        
        # Confirmación
        result = messagebox.askyesno(
            "Confirmar cambios",
            f"¿Está seguro de modificar las fechas de {len(self.files)} archivo(s)?\n\n"
            f"Fecha de creación: {self.creation_date.get()}\n"
            f"Fecha de modificación: {self.modified_date.get()}\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if not result:
            return
        
        self.progress['maximum'] = len(self.files)
        success_count = 0
        errors = []
        
        for idx, file_path in enumerate(self.files):
            try:
                self.change_file_dates(file_path, creation_dt, modified_dt)
                success_count += 1
                self.status_label.config(text=f"⏳ Procesando: {os.path.basename(file_path)}")
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
            
            self.progress['value'] = idx + 1
            self.root.update_idletasks()
        
        # Mostrar resultados
        if errors:
            error_msg = f"✅ {success_count} de {len(self.files)} archivos modificados\n\n"
            error_msg += "❌ Errores:\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... y {len(errors) - 10} errores más"
            messagebox.showwarning("Completado con errores", error_msg)
        else:
            messagebox.showinfo("Completado", f"✅ Todos los {success_count} archivos fueron modificados exitosamente")
        
        self.status_label.config(text=f"✅ Proceso completado: {success_count}/{len(self.files)} exitosos")
        self.progress['value'] = 0
    
    def change_file_dates(self, file_path, creation_date, modified_date):
        """Cambia las fechas de creación y modificación de un archivo"""
        # Obtener timestamp de modificación
        mod_timestamp = modified_date.timestamp()
        
        # Obtener fecha de acceso actual si queremos mantenerla
        if self.keep_access.get():
            access_timestamp = os.path.getatime(file_path)
        else:
            access_timestamp = mod_timestamp
        
        # Cambiar fecha de modificación y acceso
        os.utime(file_path, (access_timestamp, mod_timestamp))
        
        # Cambiar fecha de creación (específico de Windows)
        if platform.system() == 'Windows':
            try:
                import win32file
                import pywintypes
                
                # Convertir a formato Windows FILETIME
                wintime = pywintypes.Time(creation_date)
                
                # Abrir archivo
                winfile = win32file.CreateFile(
                    file_path, 
                    win32file.GENERIC_WRITE,
                    win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE | win32file.FILE_SHARE_DELETE,
                    None, 
                    win32file.OPEN_EXISTING,
                    win32file.FILE_ATTRIBUTE_NORMAL, 
                    None
                )
                
                # Establecer fecha de creación
                win32file.SetFileTime(winfile, wintime, None, None)
                winfile.close()
                
            except ImportError:
                # Si no está disponible pywin32, notificar
                raise Exception("pywin32 no está instalado. Solo se modificó la fecha de modificación.")

def main():
    """Función principal para ejecutar la aplicación"""
    root = TkinterDnD.Tk()
    app = DateChangerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

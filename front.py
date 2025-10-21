import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import re
from datetime import datetime
from models import Usuario, Paciente, Enfermedad, Diagnostico, Sintoma, Signo
from database import db

# ======== Pantalla de Login ========
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Motor Diagnóstico Médico")
        self.geometry("400x300")
        self.config(bg="white")

        title = tk.Label(self, text="Motor Diagnóstico Médico",
                         font=("Arial", 16, "bold"), bg="white", fg="#1e40af")
        title.pack(pady=30)

        tk.Label(self, text="Usuario:", bg="white").pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack(pady=5)

        tk.Label(self, text="Contraseña:", bg="white").pack()
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack(pady=5)

        tk.Button(self, text="Iniciar sesión", bg="#1e40af", fg="white",
                  width=20, command=self.login).pack(pady=20)

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        
        if username.strip() == "" or password.strip() == "":
            messagebox.showwarning("Aviso", "Ingresa usuario y contraseña para continuar")
            return
            
        # Autenticar con la base de datos
        user_data = db.authenticate_user(username, password)
        if user_data:
            self.destroy()
            DashboardWindow(user_data[1], user_data[2])  # nombre, rol
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# ======== Pantalla principal ========
class DashboardWindow(tk.Tk):
    def __init__(self, username, rol):
        super().__init__()
        self.title("Motor Diagnóstico Médico")
        self.geometry("1000x600")
        self.config(bg="white")
        self.username = username
        self.rol = rol

        # Marco lateral
        sidebar = tk.Frame(self, bg="#1e40af", width=200)
        sidebar.pack(side="left", fill="y")

        # Botones menú según rol
        self.create_menu_buttons(sidebar)
        
        # Botón de cerrar sesión
        tk.Button(sidebar, text="Cerrar Sesión", bg="#dc2626", fg="white",
                      font=("Arial", 11, "bold"), relief="flat",
                  activebackground="#ef4444",
                  command=self.logout, anchor="w", padx=20, height=2).pack(side="bottom", fill="x", pady=(20, 0))

        # Contenedor principal
        self.content = tk.Frame(self, bg="white")
        self.content.pack(side="right", expand=True, fill="both")

        self.show_welcome(username)
        self.mainloop()

    # ====== Pantalla de bienvenida ======
    def show_welcome(self, username):
        for w in self.content.winfo_children():
            w.destroy()
        tk.Label(self.content, text=f"Bienvenido, {username}",
                 font=("Arial", 18, "bold"), bg="white", fg="#1e40af").pack(pady=60)
        tk.Label(self.content, text="Selecciona una opción del menú lateral",
                 font=("Arial", 12), bg="white").pack()
    
    # ====== Cerrar sesión ======
    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que quieres cerrar sesión?"):
            self.destroy()
            LoginWindow()
    
    # ====== Crear menú según rol ======
    def create_menu_buttons(self, sidebar):
        """Crear botones del menú según el rol del usuario."""
        if self.rol == "admin":
            # Admin puede ver usuarios y gestionar el sistema
            menu_items = [
                ("Usuarios", self.show_usuarios),
                ("Pacientes", self.show_pacientes),
                ("Enfermedades", self.show_enfermedades),
                ("Historial", self.show_historial)
            ]
        elif self.rol == "medico":
            # Médico puede ver pacientes, diagnosticar y ver historial
            menu_items = [
                ("Pacientes", self.show_pacientes),
                ("Diagnósticos", self.show_diagnosticos),
                ("Enfermedades", self.show_enfermedades),
                ("Historial", self.show_historial)
            ]
        elif self.rol == "auxiliar":
            # Auxiliar puede ver pacientes y historial (solo lectura)
            menu_items = [
                ("Pacientes", self.show_pacientes),
                ("Historial", self.show_historial)
            ]
        else:
            # Rol desconocido - acceso mínimo
            menu_items = [
                ("Pacientes", self.show_pacientes)
            ]
        
        for text, cmd in menu_items:
            tk.Button(sidebar, text=text, bg="#1e40af", fg="white",
                      font=("Arial", 11, "bold"), relief="flat",
                      activebackground="#2563eb",
                      command=cmd, anchor="w", padx=20, height=2).pack(fill="x")
    
    # ====== Utilidades ======
    def calculate_age(self, fecha_nacimiento):
        """Calcular edad a partir de fecha de nacimiento."""
        if not fecha_nacimiento:
            return 0
        try:
            from datetime import datetime
            birth_date = datetime.fromisoformat(fecha_nacimiento)
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except (ValueError, TypeError):
            return 0
    
    def validate_email(self, email):
        """Validar formato de email."""
        if not email:
            return True  # Email opcional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validar formato de teléfono."""
        if not phone:
            return True  # Teléfono opcional
        # Permitir números con o sin guiones, espacios, paréntesis
        pattern = r'^[\d\s\-\(\)\+]+$'
        return re.match(pattern, phone) is not None and len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')) >= 7
    
    def validate_date(self, date_str):
        """Validar formato de fecha."""
        if not date_str:
            return True  # Fecha opcional
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # ====== Usuarios ======
    def show_usuarios(self):
        self.clear_content("Usuarios del Sistema")

        columns = ("ID", "Nombre", "Usuario", "Rol", "Correo")
        table = self.create_table(columns)
        
        # Obtener usuarios de la base de datos
        usuarios_data = db.select('usuarios', 'id, nombre, usuario, rol, correo')
        if usuarios_data:
            self.insert_data(table, usuarios_data)
        
        self.create_crud_buttons(table, "usuarios")

    # ====== Pacientes ======
    def show_pacientes(self):
        self.clear_content("Pacientes")

        columns = ("ID", "Nombre", "Apellido", "Edad", "Género", "Teléfono")
        table = self.create_table(columns)
        
        # Obtener pacientes de la base de datos
        pacientes_data = db.select('pacientes', 'id, nombre, apellido, fecha_nacimiento, genero, telefono')
        if pacientes_data:
            # Calcular edad y formatear datos
            formatted_data = []
            for paciente in pacientes_data:
                edad = self.calculate_age(paciente[3]) if paciente[3] else 0
                formatted_data.append((paciente[0], paciente[1], paciente[2], edad, paciente[4] or "", paciente[5] or ""))
            self.insert_data(table, formatted_data)
        
        self.create_crud_buttons(table, "pacientes")

    # ====== Diagnósticos ======
    def show_diagnosticos(self):
        self.clear_content("Diagnósticos")

        columns = ("ID", "Paciente", "Médico", "Fecha", "Notas")
        table = self.create_table(columns)
        
        # Obtener diagnósticos de la base de datos con información de paciente y médico
        query = """
        SELECT d.id, p.nombre || ' ' || p.apellido as paciente_nombre, 
               u.nombre as medico_nombre, d.fecha_diagnostico, d.notas
        FROM diagnosticos d
        JOIN pacientes p ON d.paciente_id = p.id
        JOIN usuarios u ON d.usuario_id = u.id
        ORDER BY d.fecha_diagnostico DESC
        """
        diagnosticos_data = db.select(query)
        if diagnosticos_data:
            self.insert_data(table, diagnosticos_data)
        
        self.create_crud_buttons(table, "diagnosticos")

    # ====== Enfermedades ======
    def show_enfermedades(self):
        self.clear_content("Enfermedades")

        columns = ("ID", "Nombre", "Descripción", "Tratamiento Base")
        table = self.create_table(columns)
        
        # Obtener enfermedades de la base de datos
        enfermedades_data = db.select('enfermedades', 'id, nombre, descripcion, tratamiento_base')
        if enfermedades_data:
            self.insert_data(table, enfermedades_data)
        
        self.create_crud_buttons(table, "enfermedades")

    # ====== Historial médico ======
    def show_historial(self):
        self.clear_content("Historial Médico")

        columns = ("ID", "Paciente", "Diagnóstico", "Fecha", "Médico")
        table = self.create_table(columns)
        
        # Obtener historial de diagnósticos de la base de datos
        query = """
        SELECT d.id, p.nombre || ' ' || p.apellido as paciente_nombre, 
               GROUP_CONCAT(e.nombre, ', ') as enfermedades,
               d.fecha_diagnostico, u.nombre as medico_nombre
        FROM diagnosticos d
        JOIN pacientes p ON d.paciente_id = p.id
        JOIN usuarios u ON d.usuario_id = u.id
        LEFT JOIN diagnostico_enfermedad de ON d.id = de.diagnostico_id
        LEFT JOIN enfermedades e ON de.enfermedad_id = e.id
        GROUP BY d.id
        ORDER BY d.fecha_diagnostico DESC
        """
        historial_data = db.select(query)
        if historial_data:
            self.insert_data(table, historial_data)
        
        self.create_crud_buttons(table, "historial")

    # ====== Utilidades ======
    def clear_content(self, title):
        for w in self.content.winfo_children():
            w.destroy()
        tk.Label(self.content, text=title, font=("Arial", 18, "bold"),
                 bg="white", fg="#1e40af").pack(pady=15)

    def create_table(self, columns):
        frame = tk.Frame(self.content, bg="white")
        frame.pack(pady=10)
        table = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=180 if col != "ID" else 60, anchor="center")
        table.pack()
        return table

    def insert_data(self, table, data):
        for item in data:
            table.insert("", "end", values=item)

    def create_crud_buttons(self, table, section):
        btn_frame = tk.Frame(self.content, bg="white")
        btn_frame.pack(pady=15)
        style = {"bg": "#2563eb", "fg": "white", "relief": "flat", "font": ("Arial", 11, "bold")}
        
        # Determinar qué botones mostrar según el rol y la sección
        buttons_to_show = self.get_allowed_buttons(section)
        
        # Botones CRUD con funcionalidad
        if "agregar" in buttons_to_show:
            tk.Button(btn_frame, text="Agregar", width=12, 
                     command=lambda: self.add_record(section), **style).pack(side="left", padx=15)
        if "editar" in buttons_to_show:
            tk.Button(btn_frame, text="Editar", width=12, 
                     command=lambda: self.edit_record(table, section), **style).pack(side="left", padx=15)
        if "eliminar" in buttons_to_show:
            tk.Button(btn_frame, text="Eliminar", width=12, 
                     command=lambda: self.delete_record(table, section), **style).pack(side="left", padx=15)
        if "buscar" in buttons_to_show:
            tk.Button(btn_frame, text="Buscar", width=12, 
                     command=lambda: self.search_records(table, section), **style).pack(side="left", padx=15)
        if "refrescar" in buttons_to_show:
            tk.Button(btn_frame, text="Refrescar", width=12, 
                     command=lambda: self.refresh_section(section), **style).pack(side="left", padx=15)

    def get_allowed_buttons(self, section):
        """Determinar qué botones CRUD puede usar el usuario según su rol."""
        if self.rol == "admin":
            if section == "usuarios":
                return ["agregar", "editar", "eliminar", "buscar", "refrescar"]
            elif section in ["pacientes", "enfermedades"]:
                return ["agregar", "editar", "eliminar", "buscar", "refrescar"]
            elif section in ["diagnosticos", "historial"]:
                return ["buscar", "refrescar"]  # Solo lectura para admin
        elif self.rol == "medico":
            if section == "usuarios":
                return []  # Médicos no pueden gestionar usuarios
            elif section in ["pacientes", "enfermedades"]:
                return ["agregar", "editar", "eliminar", "buscar", "refrescar"]
            elif section in ["diagnosticos", "historial"]:
                return ["agregar", "editar", "eliminar", "buscar", "refrescar"]
        elif self.rol == "auxiliar":
            # Auxiliares solo pueden ver y buscar
            return ["buscar", "refrescar"]
        else:
            # Rol desconocido - acceso mínimo
            return ["buscar", "refrescar"]
        
        return ["buscar", "refrescar"]  # Por defecto, al menos buscar y refrescar

    def has_permission(self, action, section):
        """Verificar si el usuario tiene permisos para realizar una acción."""
        allowed_buttons = self.get_allowed_buttons(section)
        return action in allowed_buttons

    # ====== Métodos CRUD ======
    def add_record(self, section):
        """Agregar un nuevo registro."""
        # Verificar permisos
        if not self.has_permission("agregar", section):
            messagebox.showwarning("Sin Permisos", f"No tienes permisos para agregar {section}")
            return
            
        if section == "usuarios":
            self.show_usuario_form()
        elif section == "pacientes":
            self.show_paciente_form()
        elif section == "enfermedades":
            self.show_enfermedad_form()
        elif section == "diagnosticos":
            self.show_diagnostico_form()
        else:
            messagebox.showinfo("Info", f"Funcionalidad de agregar {section} en desarrollo")

    def edit_record(self, table, section):
        """Editar un registro seleccionado."""
        # Verificar permisos
        if not self.has_permission("editar", section):
            messagebox.showwarning("Sin Permisos", f"No tienes permisos para editar {section}")
            return
            
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un registro para editar")
            return
        
        item = table.item(selected[0])
        record_id = item['values'][0]
        
        if section == "usuarios":
            self.show_usuario_form(record_id)
        elif section == "pacientes":
            self.show_paciente_form(record_id)
        elif section == "enfermedades":
            self.show_enfermedad_form(record_id)
        elif section == "diagnosticos":
            self.show_diagnostico_form(record_id)
        else:
            messagebox.showinfo("Info", f"Funcionalidad de editar {section} en desarrollo")

    def delete_record(self, table, section):
        """Eliminar un registro seleccionado."""
        # Verificar permisos
        if not self.has_permission("eliminar", section):
            messagebox.showwarning("Sin Permisos", f"No tienes permisos para eliminar {section}")
            return
            
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un registro para eliminar")
            return
        
        item = table.item(selected[0])
        record_id = item['values'][0]
        record_name = item['values'][1] if len(item['values']) > 1 else f"ID {record_id}"
        
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar {record_name}?"):
            if db.delete(section, record_id):
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                # Refrescar la tabla
                if section == "usuarios":
                    self.show_usuarios()
                elif section == "pacientes":
                    self.show_pacientes()
                elif section == "enfermedades":
                    self.show_enfermedades()
                elif section == "diagnosticos":
                    self.show_diagnosticos()
                elif section == "historial":
                    self.show_historial()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro")

    def search_records(self, table, section):
        """Buscar registros."""
        search_term = simpledialog.askstring("Buscar", f"Ingresa el término de búsqueda para {section}:")
        if search_term:
            self.perform_search(table, section, search_term)

    def perform_search(self, table, section, search_term):
        """Realizar búsqueda en la base de datos."""
        # Limpiar tabla actual
        for item in table.get_children():
            table.delete(item)
        
        try:
            if section == "usuarios":
                query = """
                SELECT id, nombre, usuario, rol, correo 
                FROM usuarios 
                WHERE nombre LIKE ? OR usuario LIKE ? OR correo LIKE ?
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                results = db.select(query, params=params)
                
            elif section == "pacientes":
                query = """
                SELECT id, nombre, apellido, fecha_nacimiento, genero, telefono 
                FROM pacientes 
                WHERE nombre LIKE ? OR apellido LIKE ? OR telefono LIKE ? OR correo LIKE ?
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                results = db.select(query, params=params)
                
                # Formatear datos para mostrar edad
                if results:
                    formatted_results = []
                    for paciente in results:
                        edad = self.calculate_age(paciente[3]) if paciente[3] else 0
                        formatted_results.append((paciente[0], paciente[1], paciente[2], edad, paciente[4] or "", paciente[5] or ""))
                    results = formatted_results
                    
            elif section == "enfermedades":
                query = """
                SELECT id, nombre, descripcion, tratamiento_base 
                FROM enfermedades 
                WHERE nombre LIKE ? OR descripcion LIKE ? OR tratamiento_base LIKE ?
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                results = db.select(query, params=params)
                
            elif section == "diagnosticos":
                query = """
                SELECT d.id, p.nombre || ' ' || p.apellido as paciente_nombre, 
                       u.nombre as medico_nombre, d.fecha_diagnostico, d.notas
                FROM diagnosticos d
                JOIN pacientes p ON d.paciente_id = p.id
                JOIN usuarios u ON d.usuario_id = u.id
                WHERE p.nombre LIKE ? OR p.apellido LIKE ? OR u.nombre LIKE ? OR d.notas LIKE ?
                ORDER BY d.fecha_diagnostico DESC
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                results = db.select(query, params=params)
                
            elif section == "historial":
                query = """
                SELECT d.id, p.nombre || ' ' || p.apellido as paciente_nombre, 
                       GROUP_CONCAT(e.nombre, ', ') as enfermedades,
                       d.fecha_diagnostico, u.nombre as medico_nombre
                FROM diagnosticos d
                JOIN pacientes p ON d.paciente_id = p.id
                JOIN usuarios u ON d.usuario_id = u.id
                LEFT JOIN diagnostico_enfermedad de ON d.id = de.diagnostico_id
                LEFT JOIN enfermedades e ON de.enfermedad_id = e.id
                WHERE p.nombre LIKE ? OR p.apellido LIKE ? OR u.nombre LIKE ? OR e.nombre LIKE ?
                GROUP BY d.id
                ORDER BY d.fecha_diagnostico DESC
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                results = db.select(query, params=params)
            
            else:
                messagebox.showinfo("Info", f"Búsqueda no implementada para {section}")
                return
            
            if results:
                self.insert_data(table, results)
                messagebox.showinfo("Búsqueda", f"Se encontraron {len(results)} resultados para '{search_term}'")
            else:
                messagebox.showinfo("Búsqueda", f"No se encontraron resultados para '{search_term}'")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")

    def refresh_section(self, section):
        """Refrescar la sección actual."""
        if section == "usuarios":
            self.show_usuarios()
        elif section == "pacientes":
            self.show_pacientes()
        elif section == "enfermedades":
            self.show_enfermedades()
        elif section == "diagnosticos":
            self.show_diagnosticos()
        elif section == "historial":
            self.show_historial()

    # ====== Formularios ======
    def show_usuario_form(self, user_id=None):
        """Mostrar formulario de usuario."""
        form_window = tk.Toplevel(self)
        form_window.title("Agregar Usuario" if not user_id else "Editar Usuario")
        form_window.geometry("400x500")
        form_window.config(bg="white")
        
        # Campos del formulario
        tk.Label(form_window, text="Nombre:", bg="white").pack(pady=5)
        nombre_entry = tk.Entry(form_window, width=40)
        nombre_entry.pack(pady=5)
        
        tk.Label(form_window, text="Usuario:", bg="white").pack(pady=5)
        usuario_entry = tk.Entry(form_window, width=40)
        usuario_entry.pack(pady=5)
        
        tk.Label(form_window, text="Contraseña:", bg="white").pack(pady=5)
        password_entry = tk.Entry(form_window, width=40, show="*")
        password_entry.pack(pady=5)
        
        tk.Label(form_window, text="Rol:", bg="white").pack(pady=5)
        rol_var = tk.StringVar(value="medico")
        
        # Solo admin puede crear otros admins
        if self.rol == "admin":
            rol_values = ["admin", "medico", "auxiliar"]
        else:
            rol_values = ["medico", "auxiliar"]  # Médicos solo pueden crear médicos y auxiliares
            
        rol_combo = ttk.Combobox(form_window, textvariable=rol_var, 
                                values=rol_values, state="readonly")
        rol_combo.pack(pady=5)
        
        tk.Label(form_window, text="Correo:", bg="white").pack(pady=5)
        correo_entry = tk.Entry(form_window, width=40)
        correo_entry.pack(pady=5)
        
        tk.Label(form_window, text="Teléfono:", bg="white").pack(pady=5)
        telefono_entry = tk.Entry(form_window, width=40)
        telefono_entry.pack(pady=5)
        
        # Cargar datos si es edición
        if user_id:
            user_data = db.select('usuarios', where="id = ?", params=(user_id,), fetch_one=True)
            if user_data:
                nombre_entry.insert(0, user_data[1])
                usuario_entry.insert(0, user_data[2])
                rol_var.set(user_data[4])
                correo_entry.insert(0, user_data[5] or "")
                telefono_entry.insert(0, user_data[6] or "")
        
        def save_user():
            data = {
                'nombre': nombre_entry.get().strip(),
                'usuario': usuario_entry.get().strip(),
                'password': password_entry.get(),
                'rol': rol_var.get(),
                'correo': correo_entry.get().strip(),
                'telefono': telefono_entry.get().strip()
            }
            
            # Validaciones
            if not all([data['nombre'], data['usuario'], data['password'], data['rol']]):
                messagebox.showerror("Error", "Completa todos los campos obligatorios")
                return
            
            if not self.validate_email(data['correo']):
                messagebox.showerror("Error", "Formato de correo electrónico inválido")
                return
            
            if not self.validate_phone(data['telefono']):
                messagebox.showerror("Error", "Formato de teléfono inválido")
                return
            
            # Verificar permisos para crear usuarios admin
            if data['rol'] == "admin" and self.rol != "admin":
                messagebox.showerror("Error", "Solo los administradores pueden crear usuarios con rol admin")
                return
            
            # Verificar si el usuario ya existe (solo para nuevos usuarios)
            if not user_id:
                existing_user = db.select('usuarios', where="usuario = ?", params=(data['usuario'],), fetch_one=True)
                if existing_user:
                    messagebox.showerror("Error", "El nombre de usuario ya existe")
                    return
            
            try:
                if user_id:
                    # Actualizar
                    if db.update('usuarios', user_id, data):
                        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                        form_window.destroy()
                        self.show_usuarios()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el usuario")
                else:
                    # Crear nuevo
                    if db.insert('usuarios', data):
                        messagebox.showinfo("Éxito", "Usuario creado correctamente")
                        form_window.destroy()
                        self.show_usuarios()
                    else:
                        messagebox.showerror("Error", "No se pudo crear el usuario")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar usuario: {str(e)}")
        
        tk.Button(form_window, text="Guardar", bg="#2563eb", fg="white",
                 command=save_user).pack(pady=20)

    def show_paciente_form(self, paciente_id=None):
        """Mostrar formulario de paciente."""
        form_window = tk.Toplevel(self)
        form_window.title("Agregar Paciente" if not paciente_id else "Editar Paciente")
        form_window.geometry("400x600")
        form_window.config(bg="white")
        
        # Campos del formulario
        tk.Label(form_window, text="Nombre:", bg="white").pack(pady=5)
        nombre_entry = tk.Entry(form_window, width=40)
        nombre_entry.pack(pady=5)
        
        tk.Label(form_window, text="Apellido:", bg="white").pack(pady=5)
        apellido_entry = tk.Entry(form_window, width=40)
        apellido_entry.pack(pady=5)
        
        tk.Label(form_window, text="Fecha de Nacimiento (YYYY-MM-DD):", bg="white").pack(pady=5)
        fecha_entry = tk.Entry(form_window, width=40)
        fecha_entry.pack(pady=5)
        
        tk.Label(form_window, text="Género:", bg="white").pack(pady=5)
        genero_var = tk.StringVar(value="Masculino")
        genero_combo = ttk.Combobox(form_window, textvariable=genero_var,
                                   values=["Masculino", "Femenino", "Otro"], state="readonly")
        genero_combo.pack(pady=5)
        
        tk.Label(form_window, text="Dirección:", bg="white").pack(pady=5)
        direccion_entry = tk.Entry(form_window, width=40)
        direccion_entry.pack(pady=5)
        
        tk.Label(form_window, text="Teléfono:", bg="white").pack(pady=5)
        telefono_entry = tk.Entry(form_window, width=40)
        telefono_entry.pack(pady=5)
        
        tk.Label(form_window, text="Correo:", bg="white").pack(pady=5)
        correo_entry = tk.Entry(form_window, width=40)
        correo_entry.pack(pady=5)
        
        # Cargar datos si es edición
        if paciente_id:
            paciente_data = db.select('pacientes', where="id = ?", params=(paciente_id,), fetch_one=True)
            if paciente_data:
                nombre_entry.insert(0, paciente_data[1])
                apellido_entry.insert(0, paciente_data[2])
                fecha_entry.insert(0, paciente_data[3] or "")
                genero_var.set(paciente_data[4] or "Masculino")
                direccion_entry.insert(0, paciente_data[5] or "")
                telefono_entry.insert(0, paciente_data[6] or "")
                correo_entry.insert(0, paciente_data[7] or "")
        
        def save_paciente():
            data = {
                'nombre': nombre_entry.get().strip(),
                'apellido': apellido_entry.get().strip(),
                'fecha_nacimiento': fecha_entry.get().strip(),
                'genero': genero_var.get(),
                'direccion': direccion_entry.get().strip(),
                'telefono': telefono_entry.get().strip(),
                'correo': correo_entry.get().strip()
            }
            
            # Validaciones
            if not all([data['nombre'], data['apellido']]):
                messagebox.showerror("Error", "Completa nombre y apellido")
                return
            
            if data['fecha_nacimiento'] and not self.validate_date(data['fecha_nacimiento']):
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return
            
            if not self.validate_email(data['correo']):
                messagebox.showerror("Error", "Formato de correo electrónico inválido")
                return
            
            if not self.validate_phone(data['telefono']):
                messagebox.showerror("Error", "Formato de teléfono inválido")
                return
            
            try:
                if paciente_id:
                    # Actualizar
                    if db.update('pacientes', paciente_id, data):
                        messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
                        form_window.destroy()
                        self.show_pacientes()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el paciente")
                else:
                    # Crear nuevo
                    if db.insert('pacientes', data):
                        messagebox.showinfo("Éxito", "Paciente creado correctamente")
                        form_window.destroy()
                        self.show_pacientes()
                    else:
                        messagebox.showerror("Error", "No se pudo crear el paciente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar paciente: {str(e)}")
        
        tk.Button(form_window, text="Guardar", bg="#2563eb", fg="white",
                 command=save_paciente).pack(pady=20)

    def show_enfermedad_form(self, enfermedad_id=None):
        """Mostrar formulario de enfermedad."""
        form_window = tk.Toplevel(self)
        form_window.title("Agregar Enfermedad" if not enfermedad_id else "Editar Enfermedad")
        form_window.geometry("500x400")
        form_window.config(bg="white")
        
        # Campos del formulario
        tk.Label(form_window, text="Nombre:", bg="white").pack(pady=5)
        nombre_entry = tk.Entry(form_window, width=50)
        nombre_entry.pack(pady=5)
        
        tk.Label(form_window, text="Descripción:", bg="white").pack(pady=5)
        descripcion_text = tk.Text(form_window, width=50, height=4)
        descripcion_text.pack(pady=5)
        
        tk.Label(form_window, text="Tratamiento Base:", bg="white").pack(pady=5)
        tratamiento_text = tk.Text(form_window, width=50, height=4)
        tratamiento_text.pack(pady=5)
        
        # Cargar datos si es edición
        if enfermedad_id:
            enfermedad_data = db.select('enfermedades', where="id = ?", params=(enfermedad_id,), fetch_one=True)
            if enfermedad_data:
                nombre_entry.insert(0, enfermedad_data[1])
                descripcion_text.insert("1.0", enfermedad_data[2] or "")
                tratamiento_text.insert("1.0", enfermedad_data[3] or "")
        
        def save_enfermedad():
            data = {
                'nombre': nombre_entry.get().strip(),
                'descripcion': descripcion_text.get("1.0", tk.END).strip(),
                'tratamiento_base': tratamiento_text.get("1.0", tk.END).strip()
            }
            
            # Validaciones
            if not data['nombre']:
                messagebox.showerror("Error", "Completa el nombre de la enfermedad")
                return
            
            # Verificar si la enfermedad ya existe (solo para nuevas enfermedades)
            if not enfermedad_id:
                existing_enfermedad = db.select('enfermedades', where="nombre = ?", params=(data['nombre'],), fetch_one=True)
                if existing_enfermedad:
                    messagebox.showerror("Error", "Ya existe una enfermedad con ese nombre")
                    return
            
            try:
                if enfermedad_id:
                    # Actualizar
                    if db.update('enfermedades', enfermedad_id, data):
                        messagebox.showinfo("Éxito", "Enfermedad actualizada correctamente")
                        form_window.destroy()
                        self.show_enfermedades()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la enfermedad")
                else:
                    # Crear nuevo
                    if db.insert('enfermedades', data):
                        messagebox.showinfo("Éxito", "Enfermedad creada correctamente")
                        form_window.destroy()
                        self.show_enfermedades()
                    else:
                        messagebox.showerror("Error", "No se pudo crear la enfermedad")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar enfermedad: {str(e)}")
        
        tk.Button(form_window, text="Guardar", bg="#2563eb", fg="white",
                 command=save_enfermedad).pack(pady=20)

    def show_diagnostico_form(self, diagnostico_id=None):
        """Mostrar formulario de diagnóstico."""
        messagebox.showinfo("Info", "Formulario de diagnóstico en desarrollo")


# ======== Ejecutar la app ========
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

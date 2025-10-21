import tkinter as tk
from tkinter import ttk, messagebox

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
        user = self.user_entry.get()
        if user.strip() == "":
            messagebox.showwarning("Aviso", "Ingresa un usuario para continuar")
        else:
            self.destroy()
            DashboardWindow(user)


# ======== Pantalla principal ========
class DashboardWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Motor Diagnóstico Médico")
        self.geometry("1000x600")
        self.config(bg="white")

        # Marco lateral
        sidebar = tk.Frame(self, bg="#1e40af", width=200)
        sidebar.pack(side="left", fill="y")

        # Botones menú
        menu_items = [
            ("Usuarios", self.show_usuarios),
            ("Pacientes", self.show_pacientes),
            ("Diagnósticos", self.show_diagnosticos),
            ("Enfermedades", self.show_enfermedades),
            ("Historial", self.show_historial)
        ]
        for text, cmd in menu_items:
            tk.Button(sidebar, text=text, bg="#1e40af", fg="white",
                      font=("Arial", 11, "bold"), relief="flat",
                      activebackground="#2563eb",
                      command=cmd, anchor="w", padx=20, height=2).pack(fill="x")

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

    # ====== Usuarios ======
    def show_usuarios(self):
        self.clear_content("Usuarios del Sistema")

        columns = ("ID", "Nombre", "Usuario", "Rol", "Correo")
        table = self.create_table(columns)
        usuarios = [
            (1, "Administrador General", "admin", "Administrador", "admin@mail.com"),
            (2, "Dr. Juan Méndez", "jmendez", "Médico", "juan.mendez@mail.com"),
            (3, "Dra. Ana Torres", "atorres", "Médico", "ana.torres@imss.com"),
            (4, "Aux. Carla López", "clopez", "Auxiliar", "carla.lopez@similares.com")
        ]
        self.insert_data(table, usuarios)
        self.create_crud_buttons()

    # ====== Pacientes ======
    def show_pacientes(self):
        self.clear_content("Pacientes")

        columns = ("ID", "Nombre", "Edad", "Género")
        table = self.create_table(columns)
        pacientes = [
            (1, "Juan Pérez", 30, "Masculino"),
            (2, "María García", 25, "Femenino"),
            (3, "Ana López", 40, "Femenino"),
            (4, "Carlos Torres", 55, "Masculino"),
        ]
        self.insert_data(table, pacientes)
        self.create_crud_buttons()

    # ====== Diagnósticos ======
    def show_diagnosticos(self):
        self.clear_content("Diagnósticos")

        columns = ("ID", "Paciente", "Síntomas", "Diagnóstico", "Tratamiento")
        table = self.create_table(columns)
        diagnosticos = [
            (1, "Juan Pérez", "Tos, fiebre", "Bronquitis", "Reposo e hidratación"),
            (2, "María García", "Dolor de cabeza, fiebre", "Migraña", "Analgésico y descanso"),
            (3, "Ana López", "Dolor abdominal", "Gastritis", "Dieta blanda y omeprazol"),
        ]
        self.insert_data(table, diagnosticos)
        self.create_crud_buttons()

    # ====== Enfermedades ======
    def show_enfermedades(self):
        self.clear_content("Enfermedades")

        columns = ("ID", "Nombre", "Síntomas", "Signos", "Tratamiento")
        table = self.create_table(columns)
        enfermedades = [
            (1, "Bronquitis", "Tos, fiebre, dificultad respiratoria", "Inflamación bronquial", "Reposo e hidratación"),
            (2, "Gastritis", "Dolor abdominal, náusea", "Sensibilidad estomacal", "Dieta blanda y medicamentos"),
            (3, "Migraña", "Dolor de cabeza, mareo", "Fotofobia", "Analgésicos y reposo"),
        ]
        self.insert_data(table, enfermedades)
        self.create_crud_buttons()

    # ====== Historial médico ======
    def show_historial(self):
        self.clear_content("Historial Médico")

        columns = ("ID", "Paciente", "Diagnóstico", "Fecha", "Evolución")
        table = self.create_table(columns)
        historial = [
            (1, "Juan Pérez", "Bronquitis", "2024-09-12", "Mejorando"),
            (2, "María García", "Migraña", "2024-09-13", "Controlado"),
            (3, "Ana López", "Gastritis", "2024-09-15", "En tratamiento"),
            (4, "Carlos Torres", "Sin diagnóstico", "2024-09-17", "Pendiente revisión")
        ]
        self.insert_data(table, historial)
        self.create_crud_buttons()

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

    def create_crud_buttons(self):
        btn_frame = tk.Frame(self.content, bg="white")
        btn_frame.pack(pady=15)
        style = {"bg": "#2563eb", "fg": "white", "relief": "flat", "font": ("Arial", 11, "bold")}
        for text in ["Agregar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(btn_frame, text=text, width=12, **style).pack(side="left", padx=15)


# ======== Ejecutar la app ========
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

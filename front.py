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
            ("Usuarios", self.show_placeholder),
            ("Pacientes", self.show_pacientes),
            ("Diagnósticos", self.show_placeholder),
            ("Enfermedades", self.show_placeholder),
            ("Historial", self.show_placeholder)
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

    def show_welcome(self, username):
        for w in self.content.winfo_children():
            w.destroy()
        tk.Label(self.content, text=f"Bienvenido, {username}",
                 font=("Arial", 18, "bold"), bg="white", fg="#1e40af").pack(pady=60)
        tk.Label(self.content, text="Selecciona una opción del menú lateral",
                 font=("Arial", 12), bg="white").pack()

    def show_placeholder(self):
        for w in self.content.winfo_children():
            w.destroy()
        tk.Label(self.content, text="Sección en desarrollo",
                 font=("Arial", 16, "italic"), bg="white", fg="#6b7280").pack(pady=100)

    def show_pacientes(self):
        for w in self.content.winfo_children():
            w.destroy()

        # Título
        tk.Label(self.content, text="Pacientes", font=("Arial", 18, "bold"),
                 bg="white", fg="#1e40af").pack(pady=15)

        # Marco central
        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(pady=20)

        # Tabla mejorada
        columns = ("ID", "Nombre", "Edad", "Género")
        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=7)
        for col in columns:
            table.heading(col, text=col)
        table.column("ID", width=60, anchor="center")
        table.column("Nombre", width=200, anchor="w")
        table.column("Edad", width=100, anchor="center")
        table.column("Género", width=150, anchor="center")

        table.pack(padx=10, pady=10)

        # Datos de ejemplo
        pacientes = [
            (1, "Juan Pérez", 30, "Masculino"),
            (2, "María García", 25, "Femenino"),
            (3, "Ana López", 40, "Femenino")
        ]
        for p in pacientes:
            table.insert("", "end", values=p)

        # Botones CRUD centrados
        btn_frame = tk.Frame(self.content, bg="white")
        btn_frame.pack(pady=15)

        style = {"bg": "#2563eb", "fg": "white", "relief": "flat", "font": ("Arial", 11, "bold")}
        for text in ["Agregar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(btn_frame, text=text, width=12, **style).pack(side="left", padx=15)


# ======== Ejecutar la app ========
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

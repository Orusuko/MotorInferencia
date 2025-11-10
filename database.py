import sqlite3
from sqlite3 import Error
import os

class Database:
    def __init__(self, db_file='medical_system.db'):
        self.db_file = db_file
        self.conn = None
        self.create_tables()

    def create_connection(self):
        """Create a database connection to a SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute('PRAGMA foreign_keys = ON')
            return self.conn
        except Error as e:
            print(e)
        return None

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create all the necessary tables if they don't exist."""
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rol TEXT NOT NULL,
                correo TEXT,
                telefono TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                fecha_nacimiento TEXT,
                genero TEXT,
                direccion TEXT,
                telefono TEXT,
                correo TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS enfermedades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                tratamiento_base TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sintomas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS signos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS enfermedad_sintoma (
                enfermedad_id INTEGER,
                sintoma_id INTEGER,
                PRIMARY KEY (enfermedad_id, sintoma_id),
                FOREIGN KEY (enfermedad_id) REFERENCES enfermedades (id) ON DELETE CASCADE,
                FOREIGN KEY (sintoma_id) REFERENCES sintomas (id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS enfermedad_signo (
                enfermedad_id INTEGER,
                signo_id INTEGER,
                PRIMARY KEY (enfermedad_id, signo_id),
                FOREIGN KEY (enfermedad_id) REFERENCES enfermedades (id) ON DELETE CASCADE,
                FOREIGN KEY (signo_id) REFERENCES signos (id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS diagnosticos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_diagnostico TEXT DEFAULT CURRENT_TIMESTAMP,
                notas TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS diagnostico_enfermedad (
                diagnostico_id INTEGER,
                enfermedad_id INTEGER,
                certeza REAL,
                PRIMARY KEY (diagnostico_id, enfermedad_id),
                FOREIGN KEY (diagnostico_id) REFERENCES diagnosticos (id) ON DELETE CASCADE,
                FOREIGN KEY (enfermedad_id) REFERENCES enfermedades (id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS diagnostico_sintoma (
                diagnostico_id INTEGER,
                sintoma_id INTEGER,
                intensidad INTEGER CHECK(intensidad BETWEEN 1 AND 10),
                PRIMARY KEY (diagnostico_id, sintoma_id),
                FOREIGN KEY (diagnostico_id) REFERENCES diagnosticos (id) ON DELETE CASCADE,
                FOREIGN KEY (sintoma_id) REFERENCES sintomas (id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS diagnostico_signo (
                diagnostico_id INTEGER,
                signo_id INTEGER,
                valor TEXT,
                PRIMARY KEY (diagnostico_id, signo_id),
                FOREIGN KEY (diagnostico_id) REFERENCES diagnosticos (id) ON DELETE CASCADE,
                FOREIGN KEY (signo_id) REFERENCES signos (id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pruebas_lb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                rango_normal TEXT,
                unidades TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pruebas_post_mortem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                procedimiento TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]

        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                conn.commit()
                self.create_default_admin()
            except Error as e:
                print(f"Error creating tables: {e}")
            finally:
                conn.close()

    def create_default_admin(self):
        """Create a default admin user if none exists."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'admin'")
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        """
                        INSERT INTO usuarios (nombre, usuario, password, rol, correo)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        ("Administrador", "admin", "admin123", "admin", "admin@medicalsystem.com")
                    )
                    conn.commit()
            except Error as e:
                print(f"Error creating default admin: {e}")
            finally:
                conn.close()

    # Generic CRUD operations
    def insert(self, table, data):
        """Insert a new record into the specified table."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?'] * len(data))
                sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
                cursor.execute(sql, tuple(data.values()))
                conn.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"Error inserting into {table}: {e}")
                return None
            finally:
                conn.close()
        return None

    def update(self, table, record_id, data):
        """Update a record in the specified table."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
                sql = f'UPDATE {table} SET {set_clause} WHERE id = ?'
                cursor.execute(sql, (*data.values(), record_id))
                conn.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(f"Error updating {table}: {e}")
                return False
            finally:
                conn.close()
        return False

    def delete(self, table, record_id):
        """Delete a record from the specified table."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                sql = f'DELETE FROM {table} WHERE id = ?'
                cursor.execute(sql, (record_id,))
                conn.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(f"Error deleting from {table}: {e}")
                return False
            finally:
                conn.close()
        return False

    def select(self, table, columns="*", where=None, params=None, fetch_one=False):
        """Query data from the specified table."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                sql = f'SELECT {columns} FROM {table}'
                if where:
                    sql += f' WHERE {where}'
                cursor.execute(sql, params or ())
                return cursor.fetchone() if fetch_one else cursor.fetchall()
            except Error as e:
                print(f"Error querying {table}: {e}")
                return None
            finally:
                conn.close()
        return None

    # Authentication
    def authenticate_user(self, username, password):
        """Authenticate a user."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, nombre, rol FROM usuarios 
                    WHERE usuario = ? AND password = ?
                    """,
                    (username, password)
                )
                return cursor.fetchone()
            except Error as e:
                print(f"Authentication error: {e}")
                return None
            finally:
                conn.close()
        return None

# Create database instance
db = Database()

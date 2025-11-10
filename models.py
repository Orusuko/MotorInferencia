from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import re
from database import db

class Model:
    """Base model class with common CRUD operations."""
    
    @classmethod
    def get_all(cls):
        """Get all records."""
        table = cls.__name__.lower() + 's'  # Simple pluralization
        return db.select(table)
    
    @classmethod
    def get_by_id(cls, id):
        """Get a single record by ID."""
        table = cls.__name__.lower() + 's'
        return db.select(table, where="id = ?", params=(id,), fetch_one=True)
    
    @classmethod
    def delete(cls, id):
        """Delete a record by ID."""
        table = cls.__name__.lower() + 's'
        return db.delete(table, id)

@dataclass
class Usuario(Model):
    """User model for authentication and authorization."""
    id: Optional[int] = None
    nombre: str = ""
    usuario: str = ""
    password: str = ""
    rol: str = ""  # admin, medico, auxiliar
    correo: str = ""
    telefono: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @classmethod
    def login(cls, username: str, password: str) -> Optional['Usuario']:
        """Authenticate a user and return user data if successful."""
        user_data = db.authenticate_user(username, password)
        if user_data:
            user = cls()
            user.id = user_data[0]
            user.nombre = user_data[1]
            user.rol = user_data[2]
            return user
        return None
    
    def save(self) -> bool:
        """Save user to database."""
        data = {
            'nombre': self.nombre,
            'usuario': self.usuario,
            'password': self.password,
            'rol': self.rol,
            'correo': self.correo,
            'telefono': self.telefono
        }
        
        if self.id:
            return db.update('usuarios', self.id, data)
        else:
            user_id = db.insert('usuarios', data)
            if user_id:
                self.id = user_id
                return True
            return False

@dataclass
class Paciente(Model):
    """Patient model for medical records."""
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    fecha_nacimiento: str = ""
    genero: str = ""
    direccion: str = ""
    telefono: str = ""
    correo: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def nombre_completo(self) -> str:
        """Return full name."""
        return f"{self.nombre} {self.apellido}".strip()
    
    @property
    def edad(self) -> int:
        """Calculate age from birth date."""
        if not self.fecha_nacimiento:
            return 0
        try:
            birth_date = datetime.fromisoformat(self.fecha_nacimiento)
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except (ValueError, TypeError):
            return 0
    
    def save(self) -> bool:
        """Save patient to database."""
        data = {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento,
            'genero': self.genero,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo
        }
        
        if self.id:
            return db.update('pacientes', self.id, data)
        else:
            paciente_id = db.insert('pacientes', data)
            if paciente_id:
                self.id = paciente_id
                return True
            return False

@dataclass
class Enfermedad(Model):
    """Disease model for medical conditions."""
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    tratamiento_base: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    sintomas: List[Dict] = field(default_factory=list)
    signos: List[Dict] = field(default_factory=list)
    
    def save(self) -> bool:
        """Save disease and its relationships."""
        data = {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tratamiento_base': self.tratamiento_base
        }
        
        conn = db.create_connection()
        if conn is None:
            return False
            
        try:
            cursor = conn.cursor()
            
            if self.id:
                # Update existing disease
                db.update('enfermedades', self.id, data)
                # Clear existing relationships
                cursor.execute("DELETE FROM enfermedad_sintoma WHERE enfermedad_id = ?", (self.id,))
                cursor.execute("DELETE FROM enfermedad_signo WHERE enfermedad_id = ?", (self.id,))
            else:
                # Insert new disease
                self.id = db.insert('enfermedades', data)
                if not self.id:
                    return False
            
            # Save symptoms relationships
            for sintoma in self.sintomas:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO enfermedad_sintoma (enfermedad_id, sintoma_id)
                    VALUES (?, ?)
                    """,
                    (self.id, sintoma['id'])
                )
            
            # Save signs relationships
            for signo in self.signos:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO enfermedad_signo (enfermedad_id, signo_id)
                    VALUES (?, ?)
                    """,
                    (self.id, signo['id'])
                )
            
            conn.commit()
            return True
            
        except Error as e:
            print(f"Error saving enfermedad: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    @classmethod
    def get_by_id(cls, id):
        """Get a disease by ID with its symptoms and signs."""
        enfermedad_data = db.select('enfermedades', where="id = ?", params=(id,), fetch_one=True)
        if not enfermedad_data:
            return None
            
        enfermedad = cls(
            id=enfermedad_data[0],
            nombre=enfermedad_data[1],
            descripcion=enfermedad_data[2] or "",
            tratamiento_base=enfermedad_data[3] or "",
            fecha_creacion=enfermedad_data[4] or ""
        )
        
        # Get related symptoms
        sintomas = db.select(
            """
            SELECT s.id, s.nombre, s.descripcion 
            FROM sintomas s
            JOIN enfermedad_sintoma es ON s.id = es.sintoma_id
            WHERE es.enfermedad_id = ?
            """,
            params=(id,)
        )
        enfermedad.sintomas = [
            {"id": s[0], "nombre": s[1], "descripcion": s[2] or ""}
            for s in sintomas
        ]
        
        # Get related signs
        signos = db.select(
            """
            SELECT s.id, s.nombre, s.descripcion 
            FROM signos s
            JOIN enfermedad_signo es ON s.id = es.signo_id
            WHERE es.enfermedad_id = ?
            """,
            params=(id,)
        )
        enfermedad.signos = [
            {"id": s[0], "nombre": s[1], "descripcion": s[2] or ""}
            for s in signos
        ]
        
        return enfermedad

@dataclass
class Sintoma(Model):
    """Symptom model for patient conditions."""
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def save(self) -> bool:
        """Save symptom to database."""
        data = {
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }
        
        if self.id:
            return db.update('sintomas', self.id, data)
        else:
            sintoma_id = db.insert('sintomas', data)
            if sintoma_id:
                self.id = sintoma_id
                return True
            return False

@dataclass
class Signo(Model):
    """Sign model for clinical findings."""
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def save(self) -> bool:
        """Save sign to database."""
        data = {
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }
        
        if self.id:
            return db.update('signos', self.id, data)
        else:
            signo_id = db.insert('signos', data)
            if signo_id:
                self.id = signo_id
                return True
            return False

@dataclass
class Diagnostico:
    """Diagnosis model for patient evaluations."""
    id: Optional[int] = None
    paciente_id: int = 0
    usuario_id: int = 0
    fecha_diagnostico: str = field(default_factory=lambda: datetime.now().isoformat())
    notas: str = ""
    enfermedades: List[Dict] = field(default_factory=list)
    sintomas: List[Dict] = field(default_factory=list)  # {id: int, intensidad: int}
    signos: List[Dict] = field(default_factory=list)    # {id: int, valor: str}
    
    def save(self) -> bool:
        """Save diagnosis and its relationships."""
        data = {
            'paciente_id': self.paciente_id,
            'usuario_id': self.usuario_id,
            'fecha_diagnostico': self.fecha_diagnostico,
            'notas': self.notas
        }
        
        conn = db.create_connection()
        if conn is None:
            return False
            
        try:
            cursor = conn.cursor()
            
            if self.id:
                # Update existing diagnosis
                db.update('diagnosticos', self.id, data)
                # Clear existing relationships
                cursor.execute("DELETE FROM diagnostico_enfermedad WHERE diagnostico_id = ?", (self.id,))
                cursor.execute("DELETE FROM diagnostico_sintoma WHERE diagnostico_id = ?", (self.id,))
                cursor.execute("DELETE FROM diagnostico_signo WHERE diagnostico_id = ?", (self.id,))
            else:
                # Insert new diagnosis
                self.id = db.insert('diagnosticos', data)
                if not self.id:
                    return False
            
            # Save disease relationships
            for enfermedad in self.enfermedades:
                cursor.execute(
                    """
                    INSERT INTO diagnostico_enfermedad (diagnostico_id, enfermedad_id, certeza)
                    VALUES (?, ?, ?)
                    """,
                    (self.id, enfermedad['id'], enfermedad.get('certeza', 0.0))
                )
            
            # Save symptom relationships
            for sintoma in self.sintomas:
                cursor.execute(
                    """
                    INSERT INTO diagnostico_sintoma (diagnostico_id, sintoma_id, intensidad)
                    VALUES (?, ?, ?)
                    """,
                    (self.id, sintoma['id'], sintoma.get('intensidad', 1))
                )
            
            # Save sign relationships
            for signo in self.signos:
                cursor.execute(
                    """
                    INSERT INTO diagnostico_signo (diagnostico_id, signo_id, valor)
                    VALUES (?, ?, ?)
                    """,
                    (self.id, signo['id'], str(signo.get('valor', '')))
                )
            
            conn.commit()
            return True
            
        except Error as e:
            print(f"Error saving diagnostico: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    @classmethod
    def get_by_paciente_id(cls, paciente_id: int) -> List['Diagnostico']:
        """Get all diagnoses for a specific patient."""
        diagnosticos_data = db.select(
            """
            SELECT d.id, d.paciente_id, d.usuario_id, d.fecha_diagnostico, d.notas,
                   u.nombre as medico_nombre
            FROM diagnosticos d
            JOIN usuarios u ON d.usuario_id = u.id
            WHERE d.paciente_id = ?
            ORDER BY d.fecha_diagnostico DESC
            """,
            params=(paciente_id,)
        )
        
        diagnosticos = []
        for diag_data in diagnosticos_data:
            diagnostico = cls(
                id=diag_data[0],
                paciente_id=diag_data[1],
                usuario_id=diag_data[2],
                fecha_diagnostico=diag_data[3],
                notas=diag_data[4] or ""
            )
            
            # Get related diseases
            enfermedades = db.select(
                """
                SELECT e.id, e.nombre, de.certeza
                FROM enfermedades e
                JOIN diagnostico_enfermedad de ON e.id = de.enfermedad_id
                WHERE de.diagnostico_id = ?
                """,
                params=(diagnostico.id,)
            )
            diagnostico.enfermedades = [
                {"id": e[0], "nombre": e[1], "certeza": e[2]}
                for e in enfermedades
            ]
            
            # Get related symptoms
            sintomas = db.select(
                """
                SELECT s.id, s.nombre, ds.intensidad
                FROM sintomas s
                JOIN diagnostico_sintoma ds ON s.id = ds.sintoma_id
                WHERE ds.diagnostico_id = ?
                """,
                params=(diagnostico.id,)
            )
            diagnostico.sintomas = [
                {"id": s[0], "nombre": s[1], "intensidad": s[2]}
                for s in sintomas
            ]
            
            # Get related signs
            signos = db.select(
                """
                SELECT s.id, s.nombre, ds.valor
                FROM signos s
                JOIN diagnostico_signo ds ON s.id = ds.signo_id
                WHERE ds.diagnostico_id = ?
                """,
                params=(diagnostico.id,)
            )
            diagnostico.signos = [
                {"id": s[0], "nombre": s[1], "valor": s[2]}
                for s in signos
            ]
            
            diagnosticos.append(diagnostico)
        
        return diagnosticos

class MotorInferencia:
    """Medical diagnosis inference engine."""
    
    @staticmethod
    def diagnosticar(sintomas_ids: List[int], signos_ids: List[int]) -> List[Dict]:
        """
        Generate a list of possible diseases based on symptoms and signs.
        
        Args:
            sintomas_ids: List of symptom IDs
            signos_ids: List of sign IDs
            
        Returns:
            List of dictionaries with disease information and match percentage
        """
        if not sintomas_ids and not signos_ids:
            return []
            
        conn = db.create_connection()
        if conn is None:
            return []
            
        try:
            cursor = conn.cursor()
            
            # Get all diseases that match the given symptoms and signs
            query = """
            SELECT 
                e.id, 
                e.nombre,
                e.descripcion,
                e.tratamiento_base,
                COUNT(DISTINCT es.sintoma_id) as sintomas_coincidentes,
                COUNT(DISTINCT es2.sintoma_id) as total_sintomas,
                COUNT(DISTINCT esg.signo_id) as signos_coincidentes,
                COUNT(DISTINCT esg2.signo_id) as total_signos
            FROM enfermedades e
            LEFT JOIN enfermedad_sintoma es ON e.id = es.enfermedad_id AND es.sintoma_id IN ({})
            LEFT JOIN enfermedad_sintoma es2 ON e.id = es2.enfermedad_id
            LEFT JOIN enfermedad_signo esg ON e.id = esg.enfermedad_id AND esg.signo_id IN ({})
            LEFT JOIN enfermedad_signo esg2 ON e.id = esg2.enfermedad_id
            GROUP BY e.id
            HAVING sintomas_coincidentes > 0 OR signos_coincidentes > 0
            ORDER BY (sintomas_coincidentes * 0.7 + signos_coincidentes * 0.3) DESC
            """.format(
                ",".join("?" * len(sintomas_ids)) if sintomas_ids else "NULL",
                ",".join("?" * len(signos_ids)) if signos_ids else "NULL"
            )
            
            params = []
            if sintomas_ids:
                params.extend(sintomas_ids)
            if signos_ids:
                params.extend(signos_ids)
                
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            enfermedades = []
            for row in resultados:
                total_sintomas = row[5] or 0
                total_signos = row[7] or 0
                sintomas_coincidentes = row[4] or 0
                signos_coincidentes = row[6] or 0
                
                # Calculate match percentage (70% symptoms, 30% signs)
                if total_sintomas > 0 or total_signos > 0:
                    porcentaje_sintomas = (sintomas_coincidentes / total_sintomas * 0.7) if total_sintomas > 0 else 0
                    porcentaje_signos = (signos_coincidentes / total_signos * 0.3) if total_signos > 0 else 0
                    porcentaje_total = (porcentaje_sintomas + porcentaje_signos) * 100
                else:
                    porcentaje_total = 0
                
                enfermedades.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2] or "",
                    'tratamiento_base': row[3] or "",
                    'porcentaje': round(porcentaje_total, 2),
                    'sintomas_coincidentes': sintomas_coincidentes,
                    'total_sintomas': total_sintomas,
                    'signos_coincidentes': signos_coincidentes,
                    'total_signos': total_signos
                })
            
            return enfermedades
            
        except Error as e:
            print(f"Error en el motor de inferencia: {e}")
            return []
        finally:
            conn.close()

@dataclass
class PruebaLb(Model):
    """Laboratory Test model for clinical tests."""
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    rango_normal: str = ""
    unidades: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def save(self) -> bool:
        """Save laboratory test to database."""
        data = {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'rango_normal': self.rango_normal,
            'unidades': self.unidades
        }
        
        if self.id:
            return db.update('pruebas_lb', self.id, data)
        else:
            prueba_id = db.insert('pruebas_lb', data)
            if prueba_id:
                self.id = prueba_id
                return True
            return False

@dataclass
class PruebaPostMortem(Model):
    """Post-Mortem Test model for autopsy procedures."""
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    procedimiento: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def save(self) -> bool:
        """Save post-mortem test to database."""
        data = {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'procedimiento': self.procedimiento
        }
        
        if self.id:
            return db.update('pruebas_post_mortem', self.id, data)
        else:
            prueba_id = db.insert('pruebas_post_mortem', data)
            if prueba_id:
                self.id = prueba_id
                return True
            return False

"""
Motor de Inferencia Médico - Sistema Experto con Base de Conocimientos y Razonamiento
Implementa forward chaining para diagnósticos basados en síntomas y signos
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from database import db


@dataclass
class Regla:
    """Representa una regla médica en la base de conocimientos."""
    id: int
    nombre: str
    enfermedad_id: int
    enfermedad_nombre: str
    antecedentes: Dict  # {'sintomas': [id1, id2], 'signos': [id1, id2]}
    consecuente: Dict   # {'enfermedad_id': x, 'certeza_base': 0.7}
    peso_sintomas: float = 0.7  # Importancia de síntomas
    peso_signos: float = 0.3    # Importancia de signos
    
    def evaluar(self, sintomas_presentes: List[int], signos_presentes: List[int]) -> Tuple[bool, float]:
        """
        Evalúa si la regla se aplica y retorna (se_aplica, certeza)
        
        Args:
            sintomas_presentes: IDs de síntomas que reportó el paciente
            signos_presentes: IDs de signos observados
            
        Returns:
            (True/False si la regla se aplica, certeza calculada)
        """
        sintomas_requeridos = self.antecedentes.get('sintomas', [])
        signos_requeridos = self.antecedentes.get('signos', [])
        
        # Contar coincidencias
        sintomas_coincidentes = sum(1 for s in sintomas_requeridos if s in sintomas_presentes)
        signos_coincidentes = sum(1 for s in signos_requeridos if s in signos_presentes)
        
        # Calcular porcentaje de coincidencia
        if sintomas_requeridos:
            porcentaje_sintomas = (sintomas_coincidentes / len(sintomas_requeridos)) * 100
        else:
            porcentaje_sintomas = 0
        
        if signos_requeridos:
            porcentaje_signos = (signos_coincidentes / len(signos_requeridos)) * 100
        else:
            porcentaje_signos = 0 if signos_requeridos else 100
        
        # Calcular certeza ponderada
        certeza = (porcentaje_sintomas * self.peso_sintomas + 
                  porcentaje_signos * self.peso_signos) / 100
        
        # Aplicar factor de certeza base de la enfermedad
        certeza *= self.consecuente.get('certeza_base', 1.0)
        
        # La regla se aplica si hay al menos 1 síntoma coincidente
        se_aplica = sintomas_coincidentes > 0 or (sintomas_requeridos == [] and signos_coincidentes > 0)
        
        return se_aplica, certeza


class BaseConocimiento:
    """Base de Conocimientos Médica - Define todas las reglas del sistema."""
    
    def __init__(self):
        self.reglas: List[Regla] = []
        self.cargar_desde_bd()
    
    def cargar_desde_bd(self):
        """Carga las reglas desde la base de datos."""
        try:
            conn = db.create_connection()
            if conn is None:
                print("❌ Error: No se pudo conectar a la base de datos")
                return
            
            cursor = conn.cursor()
            
            # Obtener todas las enfermedades y sus síntomas/signos asociados
            cursor.execute("""
                SELECT 
                    e.id,
                    e.nombre,
                    e.descripcion,
                    e.tratamiento_base
                FROM enfermedades e
            """)
            
            enfermedades = cursor.fetchall()
            regla_id = 1
            
            for enf in enfermedades:
                enf_id = enf[0]
                enf_nombre = enf[1]
                
                # Obtener síntomas asociados
                cursor.execute("""
                    SELECT s.id
                    FROM sintomas s
                    JOIN enfermedad_sintoma es ON s.id = es.sintoma_id
                    WHERE es.enfermedad_id = ?
                """, (enf_id,))
                sintomas_ids = [row[0] for row in cursor.fetchall()]
                
                # Obtener signos asociados
                cursor.execute("""
                    SELECT s.id
                    FROM signos s
                    JOIN enfermedad_signo es ON s.id = es.signo_id
                    WHERE es.enfermedad_id = ?
                """, (enf_id,))
                signos_ids = [row[0] for row in cursor.fetchall()]
                
                # Crear regla
                if sintomas_ids or signos_ids:
                    regla = Regla(
                        id=regla_id,
                        nombre=f"Diagnostico_{enf_nombre}",
                        enfermedad_id=enf_id,
                        enfermedad_nombre=enf_nombre,
                        antecedentes={
                            'sintomas': sintomas_ids,
                            'signos': signos_ids
                        },
                        consecuente={
                            'enfermedad_id': enf_id,
                            'certeza_base': 0.85  # Factor de confianza base
                        }
                    )
                    self.reglas.append(regla)
                    regla_id += 1
            
            conn.close()
            print(f"✅ Base de conocimientos cargada: {len(self.reglas)} reglas")
            
        except Exception as e:
            print(f"❌ Error cargando base de conocimientos: {e}")
    
    def obtener_reglas_aplicables(self, sintomas: List[int], signos: List[int]) -> List[Tuple[Regla, float]]:
        """
        Obtiene todas las reglas que se aplican a los síntomas/signos dados.
        
        Returns:
            Lista de (Regla, certeza) ordenada por certeza descendente
        """
        reglas_aplicables = []
        
        for regla in self.reglas:
            se_aplica, certeza = regla.evaluar(sintomas, signos)
            if se_aplica and certeza > 0:
                reglas_aplicables.append((regla, certeza))
        
        # Ordenar por certeza descendente
        return sorted(reglas_aplicables, key=lambda x: x[1], reverse=True)


class MotorInferencia:
    """Motor de Inferencia con razonamiento forward chaining."""
    
    def __init__(self):
        self.base_conocimiento = BaseConocimiento()
        self.hechos: Dict[str, any] = {}  # Hechos actuales
        self.conclusiones: List[Dict] = []  # Conclusiones derivadas
    
    def establecer_hechos(self, sintomas: List[int], signos: List[int]) -> None:
        """Establece los hechos (síntomas y signos del paciente)."""
        self.hechos = {
            'sintomas': sintomas,
            'signos': signos,
            'timestamp': datetime.now().isoformat()
        }
        self.conclusiones = []
    
    def razonar(self, sintomas: List[int], signos: List[int] = None) -> List[Dict]:
        """
        Ejecuta el motor de inferencia usando forward chaining.
        
        Args:
            sintomas: Lista de IDs de síntomas presentes
            signos: Lista de IDs de signos presentes (opcional)
            
        Returns:
            Lista de diagnósticos posibles ordenados por certeza
        """
        if signos is None:
            signos = []
        
        # Paso 1: Establecer hechos
        self.establecer_hechos(sintomas, signos)
        
        # Paso 2: Forward Chaining - Aplicar todas las reglas
        reglas_aplicables = self.base_conocimiento.obtener_reglas_aplicables(sintomas, signos)
        
        # Paso 3: Derivar conclusiones
        diagnosticos = []
        
        for regla, certeza in reglas_aplicables:
            diagnostico = {
                'id': regla.consecuente['enfermedad_id'],
                'nombre': regla.enfermedad_nombre,
                'certeza': round(certeza * 100, 2),  # Convertir a porcentaje
                'certeza_decimal': round(certeza, 3),
                'regla_aplicada': regla.nombre,
                'sintomas_coincidentes': sum(1 for s in regla.antecedentes['sintomas'] if s in sintomas),
                'total_sintomas': len(regla.antecedentes['sintomas']),
                'signos_coincidentes': sum(1 for s in regla.antecedentes['signos'] if s in signos),
                'total_signos': len(regla.antecedentes['signos'])
            }
            diagnosticos.append(diagnostico)
        
        # Ordenar por certeza descendente
        diagnosticos_ordenados = sorted(diagnosticos, key=lambda x: x['certeza'], reverse=True)
        
        return diagnosticos_ordenados
    
    def diagnosticar_detallado(self, sintomas: List[int], signos: List[int] = None) -> Dict:
        """
        Proporciona un diagnóstico detallado con explicaciones.
        
        Returns:
            Diccionario con diagnósticos y razonamiento
        """
        if signos is None:
            signos = []
        
        diagnosticos = self.razonar(sintomas, signos)
        
        # Obtener información adicional de la BD
        try:
            conn = db.create_connection()
            if conn:
                cursor = conn.cursor()
                
                for diag in diagnosticos:
                    # Obtener descripción y tratamiento
                    cursor.execute("""
                        SELECT descripcion, tratamiento_base
                        FROM enfermedades
                        WHERE id = ?
                    """, (diag['id'],))
                    
                    result = cursor.fetchone()
                    if result:
                        diag['descripcion'] = result[0] or "Sin descripción"
                        diag['tratamiento'] = result[1] or "Consultar médico"
                
                conn.close()
        except Exception as e:
            print(f"Error obteniendo detalles: {e}")
        
        return {
            'hechos': self.hechos,
            'diagnosticos': diagnosticos,
            'diagnostico_principal': diagnosticos[0] if diagnosticos else None,
            'confiabilidad_general': round(diagnosticos[0]['certeza'], 2) if diagnosticos else 0
        }


# Función pública de compatibilidad con el código existente
def diagnosticar(sintomas_ids: List[int], signos_ids: List[int] = None) -> List[Dict]:
    """
    Función para mantener compatibilidad con el código existente en front.py
    
    Uso:
        from motorInferencia import diagnosticar
        resultados = diagnosticar([1, 2, 3], [4, 5])
    """
    if signos_ids is None:
        signos_ids = []
    
    motor = MotorInferencia()
    return motor.razonar(sintomas_ids, signos_ids)


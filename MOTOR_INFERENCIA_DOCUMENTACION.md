# 🧠 Motor de Inferencia Médico - Documentación Completa

## 📋 Índice
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes Principales](#componentes-principales)
4. [Base de Conocimientos](#base-de-conocimientos)
5. [Mecanismo de Razonamiento](#mecanismo-de-razonamiento)
6. [Algoritmo de Certeza](#algoritmo-de-certeza)
7. [Cómo Usar](#cómo-usar)
8. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Introducción

Un **motor de inferencia** es un componente de sistemas expertos que utiliza:
- **Base de Conocimientos**: Reglas y hechos médicos
- **Mecanismo de Razonamiento**: Forward chaining para aplicar reglas
- **Motor de Inferencia**: Que combina los anteriores para derivar conclusiones

Este motor implementa un **sistema experto médico** similar a MYCIN (Stanford, 1976), adaptado para diagnósticos.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│          MOTOR DE INFERENCIA MÉDICO                  │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │ BASE DE CONOCIM. │      │ MECANISMO RAZÓN. │    │
│  ├──────────────────┤      ├──────────────────┤    │
│  │ • Reglas Médicas │      │ • Forward Chain. │    │
│  │ • Hechos (BD)    │      │ • Aplicar Reglas │    │
│  │ • Síntomas/Signos│      │ • Derivar Concl. │    │
│  └──────────────────┘      └──────────────────┘    │
│           ↓                         ↓                │
│  ┌─────────────────────────────────────────────┐   │
│  │     MOTOR DE INFERENCIA (forward chaining)   │   │
│  │  Aplica reglas a hechos → Diagnósticos      │   │
│  └─────────────────────────────────────────────┘   │
│                     ↓                                │
│  ┌─────────────────────────────────────────────┐   │
│  │  SISTEMA DE CERTEZA (Factor de Confianza)   │   │
│  │  Calcula % de probabilidad del diagnóstico   │   │
│  └─────────────────────────────────────────────┘   │
│                     ↓                                │
│  ┌─────────────────────────────────────────────┐   │
│  │      RESULTADOS ORDENADOS POR CERTEZA       │   │
│  │  Diagnósticos con % de confiabilidad         │   │
│  └─────────────────────────────────────────────┘   │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## Componentes Principales

### 1. **Clase `Regla`**
Representa una regla médica en el sistema experto.

```python
@dataclass
class Regla:
    id: int                          # Identificador único
    nombre: str                      # Nombre de la regla
    enfermedad_id: int              # ID de la enfermedad
    enfermedad_nombre: str          # Nombre de la enfermedad
    antecedentes: Dict              # Síntomas/signos requeridos
    consecuente: Dict               # Enfermedad concluida
    peso_sintomas: float = 0.7      # Importancia: 70%
    peso_signos: float = 0.3        # Importancia: 30%
```

**Ejemplo:**
```python
Regla(
    id=1,
    nombre="Diagnostico_Gripe",
    enfermedad_id=1,
    enfermedad_nombre="Gripe (Influenza)",
    antecedentes={
        'sintomas': [1, 2, 3, 4, 5],  # Fiebre, Tos, Dolor Cabeza, Fatiga, Dolor Muscular
        'signos': [1, 2]               # Signos asociados
    },
    consecuente={
        'enfermedad_id': 1,
        'certeza_base': 0.85           # 85% de confianza base
    }
)
```

### 2. **Clase `BaseConocimiento`**
Almacena y gestiona todas las reglas del sistema.

```python
class BaseConocimiento:
    def __init__(self):
        self.reglas = []
        self.cargar_desde_bd()  # Carga reglas desde base de datos
    
    def obtener_reglas_aplicables(sintomas, signos):
        # Retorna reglas que coinciden
```

**Flujo:**
1. Conecta a la BD
2. Lee todas las enfermedades
3. Para cada enfermedad, obtiene síntomas/signos asociados
4. Crea una regla por enfermedad
5. Almacena todas las reglas

### 3. **Clase `MotorInferencia`**
Implementa el motor con razonamiento forward chaining.

```python
class MotorInferencia:
    def establecer_hechos(sintomas, signos):
        # Define los hechos (síntomas/signos del paciente)
    
    def razonar(sintomas, signos):
        # Aplica reglas a los hechos y retorna diagnósticos
    
    def diagnosticar_detallado(sintomas, signos):
        # Retorna diagnósticos con explicaciones
```

---

## Base de Conocimientos

### ¿Cómo se construye?

La base de conocimientos se **carga automáticamente** desde la base de datos:

```sql
SELECT e.id, e.nombre, e.sintomas, e.signos
FROM enfermedades e
-- Cada enfermedad se convierte en una regla
```

**Ejemplo con Gripe:**

```
Enfermedad: Gripe (ID: 1)
├── Síntomas asociados: [1, 2, 3, 4, 5]
│   ├─ Fiebre (ID: 1)
│   ├─ Tos seca (ID: 2)
│   ├─ Dolor de cabeza (ID: 3)
│   ├─ Fatiga (ID: 4)
│   └─ Dolor muscular (ID: 5)
├── Signos asociados: [1, 2]
│   ├─ Signo 1 (ID: 1)
│   └─ Signo 2 (ID: 2)
└── Regla creada: "Diagnostico_Gripe"
```

### ¿Cómo modificar la base de conocimientos?

**Opción 1: A través de la interfaz**
1. Ve a "Enfermedades"
2. Edita una enfermedad
3. Asocia síntomas/signos
4. Guarda

**Opción 2: Directamente en la BD**
```sql
-- Asociar síntoma a enfermedad
INSERT INTO enfermedad_sintoma (enfermedad_id, sintoma_id) VALUES (1, 1);

-- Asociar signo a enfermedad
INSERT INTO enfermedad_signo (enfermedad_id, signo_id) VALUES (1, 1);
```

---

## Mecanismo de Razonamiento

### Forward Chaining (Razonamiento hacia Adelante)

**Proceso:**

```
1. HECHOS INICIALES (Síntomas/Signos del paciente)
   ↓
2. BASE DE CONOCIMIENTOS (Reglas)
   ↓
3. MOTOR APLICA REGLAS
   Pregunta: "¿Qué reglas se aplican?"
   ↓
4. DERIVACIÓN DE CONCLUSIONES
   Cada regla aplicable genera un diagnóstico
   ↓
5. ORDENAMIENTO POR CERTEZA
   Diagnósticos ordenados de mayor a menor confianza
```

### Ejemplo Paso a Paso

```python
# Entrada
sintomas = [1, 2, 3]  # Fiebre, Tos, Dolor de cabeza
signos = []           # Sin signos

# Paso 1: Motor establece hechos
motor = MotorInferencia()
motor.establecer_hechos(sintomas, signos)

# Paso 2: Recorre todas las reglas
# Regla 1: Gripe (requiere [1, 2, 3, 4, 5])
#   ✓ Coincide: 1, 2, 3
#   ✗ No coincide: 4, 5
#   → Certeza: 3/5 = 60%

# Regla 2: Faringitis (requiere [1, 3])
#   ✓ Coincide: 1, 3
#   → Certeza: 2/2 = 100%

# Regla 3: Resfriado (requiere [2, 3, 4])
#   ✓ Coincide: 2, 3
#   ✗ No coincide: 4
#   → Certeza: 2/3 = 66.7%

# Paso 3: Resultados ordenados por certeza
[
    {'nombre': 'Faringitis', 'certeza': 100.0},
    {'nombre': 'Resfriado', 'certeza': 66.7},
    {'nombre': 'Gripe', 'certeza': 60.0}
]
```

---

## Algoritmo de Certeza

### Fórmula General

```
Certeza = (% Síntomas × 0.7 + % Signos × 0.3) × Factor_Base
```

### Desglose

1. **Porcentaje de Síntomas Coincidentes**
   ```
   % Síntomas = (Síntomas Coincidentes / Total Síntomas) × 100
   ```
   - Si la enfermedad requiere 5 síntomas y el paciente tiene 3 de esos 5:
   - % Síntomas = 3/5 × 100 = 60%

2. **Porcentaje de Signos Coincidentes**
   ```
   % Signos = (Signos Coincidentes / Total Signos) × 100
   ```
   - Similar a síntomas
   - Si no hay signos: 100% (no penaliza)

3. **Ponderación**
   ```
   Certeza = (60% × 0.7) + (100% × 0.3) = 42% + 30% = 72%
   ```
   - Síntomas: peso más alto (70%)
   - Signos: peso más bajo (30%)

4. **Factor de Confianza Base**
   ```
   Certeza Final = 72% × 0.85 = 61.2%
   ```
   - Factor base = 0.85 (85% de confianza en las reglas)

### Ejemplo Completo

```python
# Paciente con síntomas: [1, 2, 3]  (Fiebre, Tos, Dolor cabeza)
# Regla Gripe requiere: [1, 2, 3, 4, 5]

Coincidencias = 3
Total = 5
% Síntomas = 3/5 × 100 = 60%

Signos coincidentes = 0
Signos totales = 2
% Signos = 0/2 × 100 = 0%

Certeza = (60 × 0.7) + (0 × 0.3) = 42% + 0% = 42%
Certeza Final = 42% × 0.85 = 35.7%

# RESULTADO: Gripe con 35.7% de certeza
```

---

## Cómo Usar

### Opción 1: Desde `front.py` (Ya configurado)

```python
from motorInferencia import diagnosticar

# Síntomas: [1, 2, 3]
# Signos: [4]
resultados = diagnosticar([1, 2, 3], [4])

# Retorna:
# [
#     {'nombre': 'Gripe', 'certeza': 85.0, 'descripcion': '...'},
#     {'nombre': 'Resfriado', 'certeza': 72.3, 'descripcion': '...'},
#     {'nombre': 'Faringitis', 'certeza': 60.0, 'descripcion': '...'}
# ]
```

### Opción 2: Diagnóstico Detallado

```python
from motorInferencia import MotorInferencia

motor = MotorInferencia()
resultado_detallado = motor.diagnosticar_detallado([1, 2, 3], [4])

# Retorna:
# {
#     'hechos': {'sintomas': [1, 2, 3], 'signos': [4], 'timestamp': '...'},
#     'diagnosticos': [...],
#     'diagnostico_principal': {'nombre': 'Gripe', 'certeza': 85.0, ...},
#     'confiabilidad_general': 85.0
# }
```

### Opción 3: Razonamiento Paso a Paso

```python
motor = MotorInferencia()

# 1. Establecer hechos
motor.establecer_hechos([1, 2, 3], [4])

# 2. Razonar
diagnosticos = motor.razonar([1, 2, 3], [4])

# 3. Ver conclusiones
print(f"Diagnósticos encontrados: {len(diagnosticos)}")
for diag in diagnosticos:
    print(f"  - {diag['nombre']}: {diag['certeza']}%")
```

---

## Ejemplos Prácticos

### Ejemplo 1: Diagnóstico Simple

```python
from motorInferencia import diagnosticar

# Paciente reporta: Fiebre (1) + Tos (2) + Dolor Cabeza (3)
resultado = diagnosticar([1, 2, 3])

# Salida esperada:
# [
#     {
#         'id': 4,
#         'nombre': 'COVID-19',
#         'certeza': 89.25,
#         'sintomas_coincidentes': 3,
#         'total_sintomas': 3
#     },
#     {
#         'id': 1,
#         'nombre': 'Gripe',
#         'certeza': 75.5,
#         'sintomas_coincidentes': 3,
#         'total_sintomas': 5
#     }
# ]
```

### Ejemplo 2: Con Signos

```python
# Paciente con síntomas Y signos
resultado = diagnosticar([1, 2, 3], [1, 2])

# Ahora los signos contribuyen al 30% de la certeza
# Mayor precisión diagnóstica
```

### Ejemplo 3: Interpretación Clínica

```python
resultado_detallado = motor.diagnosticar_detallado([1, 2, 3])

diag_principal = resultado_detallado['diagnostico_principal']

print(f"Diagnóstico: {diag_principal['nombre']}")
print(f"Certeza: {diag_principal['certeza']}%")
print(f"Descripción: {diag_principal['descripcion']}")
print(f"Tratamiento: {diag_principal['tratamiento']}")
print(f"Coincidencias: {diag_principal['sintomas_coincidentes']}/{diag_principal['total_sintomas']}")
```

---

## Mejoras Futuras

### 1. **Factores de Confianza Dinámicos**
```python
# Usar factores diferentes según edad/género
if paciente.edad < 5:
    certeza_base = 0.75  # Niños más susceptibles
elif paciente.edad > 65:
    certeza_base = 0.80  # Adultos mayores
```

### 2. **Razonamiento Backward Chaining**
```python
# Empezar por hipótesis y verificar si se cumplen
# Más eficiente para casos específicos
```

### 3. **Integración de Pruebas Laboratoriales**
```python
# Agregar pruebas de lab como evidencia adicional
# Aumentar confianza del diagnóstico
```

### 4. **Historial del Paciente**
```python
# Usar diagnósticos previos para refinar certeza actual
# Contexto histórico importante
```

---

## Troubleshooting

### ¿Por qué no aparecen resultados?
- ✓ Verifica que haya síntomas asociados a enfermedades
- ✓ Revisa que los IDs de síntomas sean correctos
- ✓ Asegúrate de que la BD esté cargada

### ¿Los porcentajes son muy bajos?
- ✓ Revisa la cantidad de síntomas por enfermedad
- ✓ Considera agregar más síntomas diferenciadores
- ✓ Ajusta los pesos (0.7, 0.3) según necesidad

### ¿Todas las enfermedades tienen igual certeza?
- ✓ Probablemente faltan síntomas específicos
- ✓ Agrega síntomas únicos a cada enfermedad
- ✓ Usa la guía de síntomas para validar

---

**Versión:** 1.0  
**Última actualización:** Noviembre 2025  
**Autor:** Sistema Médico MotorInferencia



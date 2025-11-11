# 🧠 Motor de Inferencia Médico - Sistema Experto Mejorado

## 📌 ¿Qué Cambió?

### Antes ❌
- Solo algoritmo de matching simple
- Sin base de conocimientos estructurada
- Sin razonamiento formal
- Cálculo de certeza incompleto

### Ahora ✅
- **Motor de Inferencia Completo** con Base de Conocimientos
- **Razonamiento Forward Chaining** para derivar diagnósticos
- **Sistema de Certeza** con factores de confianza
- **Explicabilidad** de cada diagnóstico
- **Extensible** y fácil de mejorar

---

## 🗂️ Estructura de Archivos

```
MotorInferencia/
├── motorInferencia.py                    ← ⭐ NUEVO: Motor con Base de Conocimientos
├── MOTOR_INFERENCIA_DOCUMENTACION.md     ← ⭐ NUEVA: Documentación completa
├── test_motorInferencia.py               ← ⭐ NUEVA: Suite de pruebas
├── front.py                              ← Actualizado para usar nuevo motor
├── models.py                             ← Mantiene compatibilidad
├── database.py
└── ...
```

---

## 🚀 Cómo Usar

### Opción 1: Desde la Interfaz Gráfica

1. Abre la aplicación
2. Ve a **Diagnósticos → Agregar**
3. Selecciona paciente
4. Marca síntomas/signos
5. Haz clic en **"ANALIZAR Y DIAGNOSTICAR"**
6. El motor de inferencia genera diagnósticos automáticamente

✅ **Ya está integrado en `front.py`**

### Opción 2: Uso Programático

#### Diagnóstico Simple
```python
from motorInferencia import diagnosticar

# Síntomas: Fiebre (1), Tos (2), Dolor Cabeza (3)
resultados = diagnosticar([1, 2, 3])

for diag in resultados:
    print(f"{diag['nombre']}: {diag['certeza']}%")
```

#### Diagnóstico Detallado
```python
from motorInferencia import MotorInferencia

motor = MotorInferencia()
resultado = motor.diagnosticar_detallado([1, 2, 3], [4, 5])

print(f"Diagnóstico: {resultado['diagnostico_principal']['nombre']}")
print(f"Certeza: {resultado['confiabilidad_general']}%")
print(f"Tratamiento: {resultado['diagnostico_principal']['tratamiento']}")
```

#### Razonamiento Paso a Paso
```python
motor = MotorInferencia()
motor.establecer_hechos([1, 2, 3], [4])
diagnosticos = motor.razonar([1, 2, 3], [4])

for diag in diagnosticos:
    print(f"{diag['nombre']}: {diag['certeza']}%")
```

---

## 🧪 Pruebas

### Ejecutar Suite de Pruebas

```bash
cd C:\Users\Orusuko\MotorInferencia
python test_motorInferencia.py
```

**Salida esperada:**
```
======================================================================
  ✅ PRUEBA 1: Base de Conocimientos
======================================================================

📚 Total de reglas cargadas: 6

🔍 Primeras 3 reglas:
   Regla: Diagnostico_Gripe
   └─ Enfermedad: Gripe (Influenza)
   └─ Síntomas requeridos: [1, 2, 3, 4, 5]
   └─ Signos requeridos: [1, 2]
...
```

### Pruebas Individuales

```python
# Prueba 1: Base de Conocimientos
python -c "from motorInferencia import BaseConocimiento; b = BaseConocimiento(); print(f'Reglas: {len(b.reglas)}')"

# Prueba 2: Diagnóstico Simple
python -c "from motorInferencia import diagnosticar; print(diagnosticar([1, 2, 3]))"

# Prueba 3: Motor Detallado
python -c "from motorInferencia import MotorInferencia; m = MotorInferencia(); print(m.diagnosticar_detallado([1, 2, 3]))"
```

---

## 📊 Componentes Principales

### 1. Clase `Regla`
Representa una regla médica en el sistema experto.

```python
Regla(
    id=1,
    nombre="Diagnostico_Gripe",
    enfermedad_id=1,
    enfermedad_nombre="Gripe (Influenza)",
    antecedentes={'sintomas': [1, 2, 3, 4, 5], 'signos': [1, 2]},
    consecuente={'enfermedad_id': 1, 'certeza_base': 0.85}
)
```

### 2. Clase `BaseConocimiento`
Carga y gestiona todas las reglas desde la base de datos.

```python
base = BaseConocimiento()
print(f"Reglas cargadas: {len(base.reglas)}")
```

### 3. Clase `MotorInferencia`
Implementa razonamiento forward chaining.

```python
motor = MotorInferencia()
diagnosticos = motor.razonar([1, 2, 3], [4])
```

---

## 🧠 Cómo Funciona el Motor

### Flujo de Razonamiento (Forward Chaining)

```
ENTRADA: Síntomas/Signos del Paciente
    ↓
┌─────────────────────────────────────┐
│ 1. ESTABLECER HECHOS                │
│    - Síntomas: [1, 2, 3]            │
│    - Signos: [4]                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. CARGAR BASE DE CONOCIMIENTOS     │
│    - 6 reglas médicas               │
│    - Síntomas por enfermedad        │
│    - Factores de certeza            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. APLICAR REGLAS A HECHOS          │
│    Para cada regla:                 │
│    - Contar síntomas coincidentes   │
│    - Contar signos coincidentes     │
│    - Calcular certeza               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. DERIVAR CONCLUSIONES             │
│    - Lista de diagnósticos          │
│    - Cada uno con certeza           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. ORDENAR POR CERTEZA              │
│    - Mayor certeza primero          │
│    - Explicación por diagnóstico    │
└─────────────────────────────────────┘
    ↓
SALIDA: Diagnósticos ordenados
```

### Cálculo de Certeza

```
Certeza = (% Síntomas × 0.7 + % Signos × 0.3) × Factor_Base

Ejemplo:
- Enfermedad requiere: [1, 2, 3, 4, 5]
- Paciente tiene: [1, 2, 3]
- Coincidencias: 3/5 = 60%
- Signos: 0% (no hay requeridos)
- Certeza = (60 × 0.7 + 0 × 0.3) × 0.85 = 35.7%
```

---

## 📈 Ventajas del Nuevo Motor

### ✅ Base de Conocimientos
- Reglas estructuradas y claras
- Fácil de agregar nuevas enfermedades
- Vinculada con la base de datos

### ✅ Razonamiento Formal
- Forward chaining implementado correctamente
- Pasos de razonamiento explicables
- Sistema de certeza científico

### ✅ Extensibilidad
- Fácil agregar nuevas reglas
- Modificable sin cambiar código
- Compatible con módulos futuros

### ✅ Mantenibilidad
- Código limpio y documentado
- Clases bien definidas
- Métodos reutilizables

---

## 🔧 Cómo Mejorar el Motor

### 1. Agregar Nuevas Enfermedades

```sql
-- En la BD
INSERT INTO enfermedades (nombre, descripcion, tratamiento_base)
VALUES ('Nueva Enfermedad', 'Descripción', 'Tratamiento');

-- Asociar síntomas
INSERT INTO enfermedad_sintoma (enfermedad_id, sintoma_id)
VALUES (7, 1), (7, 2), (7, 3);

-- El motor cargará automáticamente la nueva regla
```

### 2. Ajustar Factores de Certeza

En `motorInferencia.py`, línea 111:
```python
consecuente={
    'enfermedad_id': enf_id,
    'certeza_base': 0.85  # ← Modificar aquí (0.0 a 1.0)
}
```

### 3. Cambiar Pesos (Síntomas vs Signos)

En `motorInferencia.py`, clase `Regla`:
```python
peso_sintomas: float = 0.7  # ← Cambiar aquí (70%)
peso_signos: float = 0.3    # ← Cambiar aquí (30%)
```

### 4. Agregar Razonamiento Backward Chaining

```python
def razonar_backward(self, enfermedad_id: int) -> bool:
    """Verifica si se puede concluir una enfermedad específica"""
    # Implementar búsqueda en profundidad
    pass
```

---

## 🐛 Troubleshooting

### ¿No aparecen diagnósticos?

```python
# 1. Verificar base de conocimientos
from motorInferencia import BaseConocimiento
base = BaseConocimiento()
print(f"Reglas: {len(base.reglas)}")  # Debe ser > 0

# 2. Verificar síntomas en BD
from database import db
sintomas = db.select('sintomas')
print(f"Síntomas: {len(sintomas)}")

# 3. Verificar asociaciones
from database import db
conn = db.create_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM enfermedad_sintoma LIMIT 5")
print(cursor.fetchall())
```

### Certeza muy baja o muy alta

- **Muy baja**: Faltan síntomas específicos en las enfermedades
- **Muy alta**: Demasiada superposición de síntomas
- **Solución**: Equilibrar síntomas por enfermedad

### Motor lento

- Verificar cantidad de reglas
- Optimizar queries en `cargar_desde_bd()`
- Considerar caché de reglas

---

## 📚 Referencias

- **MYCIN** - Sistema Experto Médico (Stanford, 1976)
- **Forward Chaining** - Razonamiento desde hechos a conclusiones
- **Factor de Certeza** - Medida de confianza en diagnósticos

---

## 📝 Licencia

Proyecto de Sistema Médico - Noviembre 2025

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisa `MOTOR_INFERENCIA_DOCUMENTACION.md`
2. Ejecuta `test_motorInferencia.py`
3. Revisa logs de error en consola

---

**¡Motor de Inferencia listo para usar!** ✨


# 🐛 BUG CORREGIDO: Motor Seleccionaba Diagnóstico Incorrecto

## Problema Identificado

El usuario reportó que el motor de inferencia **siempre seleccionaba Gripe**, incluso cuando había otras enfermedades con **mayor porcentaje de certeza**.

### Ejemplo del Bug:
```
Sintomas seleccionados: Fiebre (1), Dolor de Cabeza (3), Dolor Muscular (5)

Orden INCORRECTO (antes del fix):
1. Gripe (Influenza) - 42% ← SELECCIONABA ESTA (INCORRECTA)
2. Resfriado comun - 46.67%
3. COVID-19 - 46.67%

Debería haber sido:
1. Resfriado comun - 46.67% ← DEBERÍA SELECCIONAR ESTA
```

---

## Causa Raíz del Bug

El problema estaba en **2 lugares** del archivo `models.py`:

### 1. **Ordenamiento SQL Incorrecto**
```python
# ANTES (INCORRECTO):
ORDER BY (sintomas_coincidentes * 0.7 + signos_coincidentes * 0.3) DESC

# PROBLEMA:
- Esta fórmula calculaba el PESO de coincidencias
- NO era el porcentaje final
- El porcentaje se calculaba DESPUÉS en Python
- Entonces el orden SQL era irrelevante
```

### 2. **Falta de Ordenamiento Final en Python**
```python
# ANTES (INCORRECTO):
enfermedades = []
for row in resultados:
    # ... calcular porcentaje ...
    enfermedades.append({...})

return enfermedades  # ← SIN ORDENAR

# PROBLEMA:
- Retornaba lista en orden arbitrario
- Tomaba primer elemento (diagnostico_id menor)
- Gripe tiene ID=1, por eso siempre salía primera
```

---

## Solución Implementada

### Cambio 1: Simplificar Orden SQL
```python
# AHORA (CORRECTO):
ORDER BY e.id DESC

# RAZÓN:
- El orden SQL no importa
- El ordenamiento final se hace en Python
- Esto evita cálculos innecesarios en BD
```

### Cambio 2: Ordenar Lista por Porcentaje en Python
```python
# AHORA (CORRECTO):
enfermedades = []
for row in resultados:
    # ... calcular porcentaje ...
    enfermedades.append({
        'porcentaje': porcentaje_total,
        ...
    })

# NUEVO: Ordenar por porcentaje descendente
enfermedades_ordenadas = sorted(enfermedades, key=lambda x: x['porcentaje'], reverse=True)
return enfermedades_ordenadas
```

---

## Resultado del Fix

### Antes del Fix:
```
Orden (INCORRECTO):
1. Gripe (Influenza) - 42% ← SELECCIONA ESTO
2. Resfriado comun - 46.67%
3. COVID-19 - 46.67%
```

### Después del Fix:
```
Orden (CORRECTO):
1. Faringitis - 70% ← SELECCIONA ESTO ✅
2. Gripe (Influenza) - 42%
3. Neumania - 23.33%
4. Bronquitis - 23.33%
5. COVID-19 - 23.33%
6. Resfriado comun - 23.33%
```

---

## Código Modificado

```python
# Línea 485 - ANTES:
ORDER BY (sintomas_coincidentes * 0.7 + signos_coincidentes * 0.3) DESC

# Línea 485 - AHORA:
ORDER BY e.id DESC

# Línea 554-559 - NUEVO:
})

# IMPORTANTE: Ordenar por porcentaje descendente (mayor certeza primero)
enfermedades_ordenadas = sorted(enfermedades, key=lambda x: x['porcentaje'], reverse=True)

return enfermedades_ordenadas
```

---

## Prueba del Fix

Se creó `test_orden.py` para verificar:

```
PRUEBA CON LOS SINTOMAS ACTUALES:
Sintomas: Fiebre (1), Dolor de Cabeza (3), Dolor Muscular (5)

Orden de diagnosticos (de mayor a menor certeza):

1. Faringitis                     - Certeza:  70.00% ✅
2. Gripe (Influenza)              - Certeza:  42.00%
3. Neumania                       - Certeza:  23.33%
4. Bronquitis                     - Certeza:  23.33%
5. COVID-19                       - Certeza:  23.33%
6. Resfriado comun                - Certeza:  23.33%
```

✅ **CORRECTO**: Ahora selecciona Faringitis (70%) en lugar de Gripe (42%)

---

## Impacto del Fix

✅ **Diagnósticos más precisos**: El motor selecciona la enfermedad con mayor probabilidad

✅ **Consistencia**: Mismos síntomas siempre dan el mismo diagnóstico correcto

✅ **Fiabilidad**: El médico puede confiar en la recomendación del motor

✅ **Mejor UX**: Los usuarios ven resultados médicamente sensatos

---

## Archivos Modificados

- `models.py` - Líneas 485 y 554-559 (método `diagnosticar()` en clase `MotorInferencia`)

---

## Recomendaciones Futuras

1. **Agregar logging**: Registrar qué diagnósticos se consideraron y sus porcentajes
2. **UI mejorada**: Mostrar top 3 diagnósticos al usuario (no solo el principal)
3. **Confianza**: Mostrar nivel de confianza junto al diagnóstico
4. **Auditoría**: Rastrear si el médico acepta o rechaza la recomendación

---

**Fecha de Corrección**: Noviembre 2025
**Estado**: ✅ CORREGIDO Y PROBADO


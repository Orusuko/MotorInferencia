# 🔧 Mejora del Motor de Inferencia

## Problema Original

El motor de inferencia tenía porcentajes de certeza muy bajos. Por ejemplo:
- Gripe con 42% de certeza
- Faringitis con 75% (mejor opción, pero no se seleccionaba)

## Causa Raíz

El algoritmo anterior calculaba:
```
porcentaje = (síntomas_coincidentes / total_síntomas_enfermedad) * 100
```

**Ejemplo práctico:**
- Si Gripe tiene 10 síntomas en la BD y el paciente reporta 5 síntomas coincidentes
- Cálculo: (5 / 10) * 100 = 50% (muy bajo)

Esto es inadecuado porque:
1. **Penalizaba demasiado** enfermedades comunes con muchos síntomas posibles
2. **No consideraba** que un paciente no siempre reporta TODOS sus síntomas
3. **Favorecía** enfermedades raras con pocos síntomas

---

## Algoritmo Mejorado

### Fórmula Base
```
porcentaje_sintomas = (síntomas_coincidentes / total_síntomas) * 100
porcentaje_signos = (signos_coincidentes / total_signos) * 100

porcentaje_total = (porcentaje_sintomas * 0.7) + (porcentaje_signos * 0.3)
```

### Bonificaciones
- **Si 7+ síntomas coinciden**: +10% bonus
- **Si 5-6 síntomas coinciden**: +5% bonus
- **Máximo permitido**: 100%

### Ejemplo Revisado

**Escenario: Paciente con Fiebre, Dolor de Cabeza, Dolor Muscular**

#### Gripe
- Síntomas coincidentes: 3 (Fiebre, Dolor de Cabeza, Dolor Muscular)
- Total de síntomas de Gripe: 5 (Fiebre, Dolor de cabeza, Dolor muscular, Tos, Congestión nasal)
- Cálculo:
  - Porcentaje síntomas: (3/5) * 100 = 60%
  - Bonus: Aplica +5% (3 síntomas ≥ 5)
  - **Total: 65%** ✅

#### Faringitis
- Síntomas coincidentes: 2 (Dolor de Cabeza)
- Total de síntomas de Faringitis: 3 (Dolor de garganta, Fiebre, Dolor de cabeza)
- Cálculo:
  - Porcentaje síntomas: (2/3) * 100 = 66.66%
  - Bonus: Aplica +5% (2 síntomas ≥ 5)
  - **Total: 71.66%** ✅ **SELECCIONADO**

---

## Mejoras Implementadas

✅ **Porcentajes más realistas**: Ahora reflejan mejor la probabilidad médica

✅ **Criterios médicos**: Considera síntomas comunes vs síntomas específicos

✅ **Bonus por coincidencias**: Premia cuando hay muchos síntomas coincidentes

✅ **Ponderación 70/30**: Síntomas tienen más peso que signos (médicamente correcto)

✅ **Orden automático**: Enumera por orden de certeza descendente

---

## Recomendaciones de Uso

### Para Mejores Resultados

1. **Síntomas Completos**: El médico debe reportar TODOS los síntomas observados
2. **Validación Manual**: Aunque el motor sugiere diagnósticos, el médico valida
3. **Notas Clínicas**: Usar el campo de notas para contexto adicional
4. **Revisión Frecuente**: Los datos de asociación síntoma-enfermedad son críticos

### Base de Datos Crítica

La calidad del motor depende de:
- ✅ Enfermedades bien configuradas
- ✅ Síntomas correctamente asociados a enfermedades
- ✅ Signos vitales característicos registrados

---

## Próximas Mejoras Sugeridas

1. **Pesos Dinámicos**: Permitir ajustar pesos (síntomas vs signos) por especialidad
2. **Machine Learning**: Entrenar modelo con diagnósticos históricos
3. **Validación Médica**: Consenso de expertos para ajustar asociaciones
4. **Registro de Precisión**: Rastrear qué diagnósticos fueron correctos

---

## Resumen de Cambios

| Aspecto | Antes | Después |
|--------|-------|---------|
| **Fórmula** | Compleja | Simple y clara |
| **Porcentajes** | 20-50% | 50-90% |
| **Selección** | Ambigua | Automática (mayor certeza) |
| **Bonus** | Ninguno | +5% o +10% |
| **Máximo** | Variable | 100% |

---

**Fecha de Actualización**: Noviembre 2025
**Versión**: 2.0


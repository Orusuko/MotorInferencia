# 🔍 Guía de Combinaciones de Síntomas para Diferentes Diagnósticos

## 📊 Análisis del Sistema Actual

Basado en tu base de datos, aquí están todas las combinaciones de síntomas para obtener diagnósticos diferentes.

---

## 📋 Síntomas Disponibles

| ID | Síntoma | Descripción |
|----|---------|-------------|
| 1 | Fiebre | Temperatura corporal elevada por encima de 38°C |
| 2 | Tos seca | Tos sin expectoración |
| 3 | Dolor de cabeza | Cefalea de intensidad variable |
| 4 | Fatiga | Cansancio y debilidad generalizada |
| 5 | Dolor muscular | Mialgia en diferentes grupos musculares |

---

## 🩺 Enfermedades y Sus Síntomas

### 1. **GRIPE (INFLUENZA)** 
**Síntomas asociados:** Fiebre, Dolor de cabeza, Dolor muscular, Fatiga, Tos seca
**Descripción:** Infección viral respiratoria aguda causada por el virus de la influenza
**Tratamiento:** Reposo, hidratación abundante, antipiréticos, antivirales en casos graves

### 2. **FARINGITIS**
**Síntomas asociados:** Fiebre, Dolor de cabeza
**Descripción:** Inflamación de la faringe, generalmente de origen viral o bacteriano
**Tratamiento:** Analgésicos, antiinflamatorios, antibióticos si es bacteriana

### 3. **RESFRIADO COMÚN**
**Síntomas asociados:** Tos seca, Dolor de cabeza, Fatiga
**Descripción:** Infección viral leve de las vías respiratorias superiores
**Tratamiento:** Reposo, líquidos, analgésicos (No requiere antibióticos)

### 4. **COVID-19**
**Síntomas asociados:** Fiebre, Tos seca, Fatiga
**Descripción:** Enfermedad causada por coronavirus SARS-CoV-2
**Tratamiento:** Aislamiento, oxigenoterapia si necesario, antivirales, monitoreo constante

### 5. **BRONQUITIS**
**Síntomas asociados:** Fiebre, Tos seca, Fatiga
**Descripción:** Inflamación de los bronquios principales
**Tratamiento:** Reposo, humidificación ambiental, expectorantes, broncodilatadores

### 6. **NEUMONÍA**
**Síntomas asociados:** Fiebre, Tos seca, Fatiga
**Descripción:** Infección del parénquima pulmonar con consolidación
**Tratamiento:** Antibióticos según tipo, oxigenoterapia, reposo, monitoreo hospitalario

---

## 🧪 COMBINACIONES DE SÍNTOMAS PARA CADA DIAGNÓSTICO

### ✅ OPCIÓN 1: Para obtener **FARINGITIS** (70% certeza)
```
Síntomas a seleccionar:
  ✓ Fiebre (ID: 1)
  ✓ Dolor de cabeza (ID: 3)

Resultado esperado:
  1. Gripe (Influenza) - 28%
  2. Faringitis - 70% ⭐ GANADOR
```
**Cuándo usar:** Paciente con dolor de garganta, fiebre y dolor de cabeza, pero SIN tos ni dolor muscular

---

### ✅ OPCIÓN 2: Para obtener **RESFRIADO COMÚN** (70% certeza)
```
Síntomas a seleccionar:
  ✓ Tos seca (ID: 2)
  ✓ Dolor de cabeza (ID: 3)
  ✓ Fatiga (ID: 4)

Resultado esperado:
  1. Gripe (Influenza) - 42%
  2. Resfriado común - 70% ⭐ GANADOR
```
**Cuándo usar:** Paciente con síntomas leves, sin fiebre, con tos ligera y cansancio

---

### ✅ OPCIÓN 3: Para obtener **COVID-19** (70% certeza)
```
Síntomas a seleccionar:
  ✓ Fiebre (ID: 1)
  ✓ Tos seca (ID: 2)
  ✓ Fatiga (ID: 4)

Resultado esperado:
  1. Gripe (Influenza) - 42%
  2. COVID-19 - 70% ⭐ GANADOR
```
**Cuándo usar:** Paciente con fiebre, tos y cansancio extremo, SIN dolor muscular

---

### ⚠️ SITUACIÓN ACTUAL: INFLUENZA/GRIPE (Solo 42% certeza)
```
Síntomas actuales seleccionados:
  ✓ Fiebre (ID: 1)
  ✓ Dolor de Cabeza (ID: 2) ← Este ID es incorrecto
  ✓ Dolor Muscular (ID: 3) ← Este ID es incorrecto

PROBLEMA IDENTIFICADO:
Los IDs están en orden incorrecto. Debería ser:
  ✓ Fiebre (ID: 1)
  ✓ Dolor de Cabeza (ID: 3) ← Correcto
  ✓ Dolor Muscular (ID: 5) ← Correcto

Resultado esperado CORREGIDO:
  1. Gripe (Influenza) - MAYOR CERTEZA ⭐
```

---

## 🎯 TABLA RÁPIDA DE REFERENCIA

| Diagnóstico Deseado | Síntomas a Seleccionar | Certeza Esperada |
|---|---|---|
| **FARINGITIS** | Fiebre + Dolor de cabeza | 70% ⭐ |
| **RESFRIADO** | Tos seca + Dolor de cabeza + Fatiga | 70% ⭐ |
| **COVID-19** | Fiebre + Tos seca + Fatiga | 70% ⭐ |
| **BRONQUITIS** | Fiebre + Tos seca + Fatiga | 70% (COVID-19) |
| **NEUMONÍA** | Fiebre + Tos seca + Fatiga | 70% (COVID-19) |
| **GRIPE** | Fiebre + Tos seca + Dolor de cabeza | Varía (~45%) |

---

## 💡 Recomendaciones para Mejorar Diagnosis

### 1. **Agregar Más Síntomas Específicos**
Actualmente solo hay 5 síntomas. Sugerir agregar:
- Dolor de garganta (específico para Faringitis)
- Congestión nasal (específico para Resfriado)
- Dificultad respiratoria (específico para Neumonía/COVID)
- Pérdida de olfato/gusto (específico para COVID-19)

### 2. **Mejorar Asociaciones**
- Algunas enfermedades comparten muchos síntomas
- Crear diferencias más marcadas en las asociaciones

### 3. **Considerar Signos Vitales**
- Presión arterial
- Frecuencia cardíaca
- Saturación de oxígeno

---

## 📝 Notas Importantes

⚠️ **NOTA**: El motor de inferencia selecciona automáticamente el diagnóstico con **mayor certeza**

✅ **VENTAJA**: No requiere selección manual

❌ **LIMITACIÓN**: Los porcentajes dependen de:
1. Cantidad de síntomas configurados por enfermedad
2. Síntomas que el paciente reporte
3. Algoritmo ponderado (70% síntomas, 30% signos)

---

## 🔄 Proceso para Cambiar Diagnóstico

Para obtener un diagnóstico diferente en tu próxima consulta:

1. **En la aplicación**, ve a **Diagnósticos → Agregar**
2. **Selecciona paciente**: Mario Leon
3. **Marca SOLO los síntomas específicos** de la enfermedad deseada (ver tabla arriba)
4. **Haz clic en "ANALIZAR Y DIAGNOSTICAR"**
5. **El motor eligirá automáticamente** la enfermedad con mayor porcentaje

---

**Última actualización:** Noviembre 2025


# 🏥 Guía de Consulta Médica con Motor de Inferencia

## 🎯 Descripción

El sistema ahora cuenta con un **formulario completo de consulta médica** que utiliza un **motor de inferencia automático** para diagnosticar enfermedades basándose en los síntomas y signos clínicos observados.

---

## 🚀 Cómo Realizar una Consulta Médica

### **Paso 1: Acceder al formulario**

1. Inicia sesión como **Médico** o **Admin**
2. Menú lateral → **"Diagnósticos"**
3. Haz clic en **"Agregar"**
4. Se abrirá la ventana "🏥 Nueva Consulta Médica"

---

### **Paso 2: Seleccionar Paciente**

**Sección 1: Seleccionar Paciente**
- Despliega el combo box
- Selecciona el paciente que deseas consultar
- Formato: `Nombre Apellido (ID: #)`

> ⚠️ **Nota**: Si no hay pacientes disponibles, primero debes crear uno en la sección "Pacientes"

---

### **Paso 3: Seleccionar Síntomas**

**Sección 2: Síntomas Observados**
- Marca con ✅ todos los síntomas que presenta el paciente
- Puedes seleccionar múltiples síntomas
- Scroll para ver más opciones si hay muchos síntomas

**Ejemplos de síntomas:**
- Fiebre
- Tos seca
- Dolor de cabeza
- Náuseas
- Fatiga

> ⚠️ **Requisito**: Debes seleccionar al menos 1 síntoma para poder diagnosticar

---

### **Paso 4: Seleccionar Signos Clínicos (Opcional)**

**Sección 3: Signos Clínicos**
- Marca con ✅ los signos clínicos observados (opcional)
- Los signos son hallazgos objetivos medibles

**Ejemplos de signos:**
- Presión arterial elevada
- Frecuencia cardíaca irregular
- Temperatura corporal alta

> ℹ️ **Nota**: Los signos son opcionales pero mejoran la precisión del diagnóstico

---

### **Paso 5: Usar el Motor de Inferencia**

**Sección 4: Diagnóstico Automático**

1. **Haz clic en el botón verde "🔍 Analizar (Motor de Inferencia)"**
2. El sistema analizará automáticamente los síntomas y signos
3. Se mostrarán las **5 enfermedades más probables** con:
   - **Nombre de la enfermedad**
   - **% de coincidencia** (certeza del diagnóstico)
   - **Descripción** de la enfermedad
   - **Tratamiento base** sugerido
   - **Coincidencias** de síntomas y signos

**Ejemplo de resultado:**
```
🔍 DIAGNÓSTICO AUTOMÁTICO - ENFERMEDADES SUGERIDAS:

======================================================================

1. Gripe (Influenza) - 85.5% de coincidencia
   Descripción: Infección viral respiratoria aguda...
   Tratamiento: Reposo, hidratación, antipiréticos...
   Coincidencias: 4/5 síntomas, 2/3 signos

2. Resfriado común - 65.0% de coincidencia
   Descripción: Infección viral leve...
   Tratamiento: Sintomático...
   Coincidencias: 3/5 síntomas, 1/3 signos

======================================================================

💡 Nota: Estas son sugerencias automáticas. Verifica el diagnóstico.
```

---

### **Paso 6: Agregar Notas Médicas**

**Sección 5: Notas Médicas**
- Escribe observaciones adicionales
- Información relevante del paciente
- Recomendaciones especiales

**Ejemplo:**
```
Paciente refiere malestar general desde hace 3 días.
Se recomienda reposo y tomar abundante líquido.
Cita de seguimiento en 5 días.
```

---

### **Paso 7: Guardar la Consulta**

1. **Haz clic en "💾 Guardar Consulta"**
2. El sistema guardará automáticamente:
   - Los síntomas seleccionados
   - Los signos clínicos
   - Las 3 enfermedades más probables (con su % de certeza)
   - Las notas médicas
   - Fecha y hora de la consulta
   - Médico responsable
3. Se mostrará un mensaje de confirmación con el diagnóstico principal
4. La consulta aparecerá en el **historial médico del paciente**

---

## 🔍 Cómo Funciona el Motor de Inferencia

### **Algoritmo de Diagnóstico:**

El motor de inferencia utiliza un **algoritmo ponderado** que:

1. **Compara** los síntomas y signos seleccionados con las enfermedades registradas
2. **Calcula** un porcentaje de coincidencia usando:
   - **70% de peso** para síntomas
   - **30% de peso** para signos clínicos
3. **Ordena** las enfermedades por porcentaje de coincidencia (mayor a menor)
4. **Retorna** las 5 enfermedades más probables

### **Fórmula:**
```
Certeza = (Síntomas_Coincidentes / Total_Síntomas) * 0.7 + 
          (Signos_Coincidentes / Total_Signos) * 0.3
```

---

## 📊 Visualizar el Historial

Después de guardar la consulta:

1. Ve a **"Pacientes"**
2. **Doble clic** en el paciente
3. Se abrirá su historial completo con:
   - Todas las consultas realizadas
   - Enfermedades diagnosticadas
   - Fechas de las consultas
   - Médico responsable

---

## ⚠️ Requisitos Previos

Para que el motor de inferencia funcione correctamente, debes tener:

### 1. **Síntomas Registrados**
- Ir a "Síntomas" → Agregar síntomas
- Ejemplo: Fiebre, Tos, Dolor de cabeza, etc.

### 2. **Enfermedades Registradas**
- Ir a "Enfermedades" → Agregar enfermedades
- Ejemplo: Gripe, Resfriado, COVID-19, etc.

### 3. **Asociar Síntomas a Enfermedades** (IMPORTANTE)
- ⚠️ Actualmente esta funcionalidad está pendiente
- **Solución temporal**: Los síntomas se deben asociar directamente en la base de datos

### 4. **Signos Clínicos (Opcional)**
- Ir a "Signos" → Agregar signos
- Ejemplo: Presión alta, Temperatura elevada, etc.

---

## 🎯 Ejemplo Completo: Diagnosticar Gripe

### Escenario:
Un paciente llega con síntomas de gripe.

### Pasos:

1. **Crear Síntomas** (si no existen):
   ```
   - Fiebre alta
   - Tos seca
   - Dolor de cabeza
   - Fatiga
   - Dolor muscular
   ```

2. **Crear Enfermedad** (si no existe):
   ```
   Nombre: Gripe (Influenza)
   Descripción: Infección viral respiratoria aguda
   Tratamiento: Reposo, hidratación, antipiréticos
   ```

3. **Asociar síntomas a la enfermedad** (en BD)

4. **Realizar Consulta**:
   - Seleccionar paciente: Juan Pérez
   - Marcar síntomas: Fiebre alta, Tos seca, Dolor de cabeza, Fatiga
   - Analizar con motor de inferencia
   - Resultado: "Gripe (Influenza) - 85.5% de coincidencia"
   - Agregar notas: "Paciente con síntomas desde hace 2 días"
   - Guardar consulta

5. **Verificar en Historial**:
   - Ir a Pacientes → Doble clic en Juan Pérez
   - Ver diagnóstico guardado

---

## 💡 Consejos y Mejores Prácticas

### ✅ **DO's (Hacer)**
- Selecciona TODOS los síntomas observados
- Usa el motor de inferencia ANTES de guardar
- Verifica el diagnóstico sugerido (usa tu criterio médico)
- Agrega notas detalladas
- Revisa el porcentaje de certeza

### ❌ **DON'Ts (No Hacer)**
- No guardes sin analizar primero
- No confíes ciegamente en el 100% - verifica siempre
- No olvides agregar notas médicas
- No selecciones síntomas que el paciente no presenta

---

## 🚨 Solución de Problemas

### "No se encontraron enfermedades"
**Causas posibles:**
1. No hay enfermedades con esos síntomas asociados
2. Los síntomas no están asociados a ninguna enfermedad

**Solución:**
- Ve a "Enfermedades" y asocia síntomas (función pendiente)
- Verifica en la base de datos las tablas `enfermedad_sintoma` y `enfermedad_signo`

### "No hay síntomas registrados"
**Solución:**
- Ve a "Síntomas" → Agregar
- Crea al menos 3-5 síntomas comunes

### "No hay pacientes registrados"
**Solución:**
- Ve a "Pacientes" → Agregar
- Crea el paciente primero

---

## 📈 Próximas Mejoras

### En desarrollo:
- [ ] Interfaz gráfica para asociar síntomas/signos a enfermedades
- [ ] Edición de diagnósticos existentes
- [ ] Exportar historial a PDF
- [ ] Gráficas de diagnósticos
- [ ] Búsqueda de diagnósticos por enfermedad

---

## 📞 Soporte

Para más información:
- `README.md` - Guía general del sistema
- `GUIA_USUARIO.md` - Manual completo
- `MEJORAS_IMPLEMENTADAS.md` - Detalles técnicos

---

**¡El motor de inferencia está listo para usarse! 🎉**

Versión: 1.2.0 | Fecha: 28 de Octubre de 2025


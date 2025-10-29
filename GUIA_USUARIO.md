# 📖 Guía de Usuario - Motor Diagnóstico Médico

## 🔐 Inicio de Sesión

### Credenciales por Defecto

| Rol | Usuario | Contraseña |
|-----|---------|-----------|
| Admin | `admin` | `admin123` |

> ℹ️ **Nota**: Estos son los datos por defecto. Otros usuarios pueden ser creados por el administrador.

### Roles Disponibles
- **Admin**: Acceso completo a todas las funcionalidades
- **Médico**: Gestiona pacientes, diagnósticos y síntomas
- **Auxiliar**: Solo puede visualizar (lectura)

---

## 📋 Menú Principal

Después de iniciar sesión, verás diferentes opciones según tu rol:

### Para Administrador:
```
- Usuarios
- Pacientes
- Enfermedades
- Historial
- Síntomas
- Signos
```

### Para Médicos:
```
- Pacientes
- Diagnósticos
- Enfermedades
- Síntomas
- Historial
```

### Para Auxiliares:
```
- Pacientes
- Historial
```

---

## 🆕 Funcionalidades Nuevas

### 1️⃣ **GESTIÓN DE SÍNTOMAS** (Nueva)

#### ¿Dónde está?
Menú lateral → **Síntomas**

#### ¿Quién puede acceder?
- ✅ Admin (acceso completo)
- ✅ Médicos (acceso completo)
- ❌ Auxiliares (sin acceso)

#### Operaciones Disponibles

**➕ Agregar Síntoma**
1. Haz clic en botón "Agregar"
2. Se abrirá un formulario con:
   - **Nombre**: Nombre del síntoma (ej: "Fiebre", "Tos seca")
   - **Descripción**: Detalles del síntoma
3. Haz clic en "Guardar"
4. Se validará que el nombre no sea duplicado

**✏️ Editar Síntoma**
1. Selecciona el síntoma de la tabla
2. Haz clic en "Editar"
3. Modifica los datos
4. Haz clic en "Guardar"

**🗑️ Eliminar Síntoma**
1. Selecciona el síntoma de la tabla
2. Haz clic en "Eliminar"
3. Confirma la eliminación

**🔍 Buscar Síntoma**
1. Haz clic en "Buscar"
2. Ingresa el término de búsqueda
3. Presiona Enter o el botón OK
4. Se mostrarán los resultados

**🔄 Refrescar**
- Haz clic en "Refrescar" para actualizar la lista

---

### 2️⃣ **GESTIÓN DE SIGNOS CLÍNICOS** (Bonus)

#### ¿Dónde está?
Menú lateral → **Signos** (solo disponible para Admin)

#### Funcionamiento
Idéntico a Síntomas:
- Agregar nuevos signos (hallazgos clínicos)
- Editar signos existentes
- Eliminar signos
- Buscar y refrescar

---

### 3️⃣ **LISTA DE PACIENTES INTERACTIVA** (Mejorada)

#### ¿Dónde está?
Menú lateral → **Pacientes**

#### Visualización
Se muestra una tabla con:
- ID del paciente
- Nombre y Apellido
- Edad (calculada automáticamente)
- Género
- Teléfono

#### 💡 **NUEVA: Ver Historial del Paciente**

**Paso a Paso:**
1. Ve a "Pacientes"
2. **Haz doble clic** en el paciente que deseas ver
3. Se abrirá una ventana con el historial completo

**Información que verás:**
- Nombre completo del paciente
- Todos sus diagnósticos (ordenados por fecha, más recientes primero)
- Para cada diagnóstico:
  - ID del diagnóstico
  - Notas médicas
  - Enfermedades diagnosticadas
  - Fecha del diagnóstico
  - Médico que lo realizó

**Ejemplo:**
```
Historial Médico de Juan Pérez

ID  | Diagnóstico    | Enfermedades              | Fecha      | Médico
----|----------------|---------------------------|------------|--------
5   | Fiebre alta    | Influenza, Gripe común   | 2025-01-15 | Dr. López
3   | Dolor de pecho | Angina de pecho          | 2024-12-20 | Dra. García
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Crear Nuevo Síntoma
```
1. Admin inicia sesión
2. Menú → Síntomas
3. Botón "Agregar"
4. Ingresa:
   - Nombre: "Dolor abdominal"
   - Descripción: "Dolor en la región abdominal..."
5. Guardar
```

### Caso 2: Ver Historial Médico de un Paciente
```
1. Médico inicia sesión
2. Menú → Pacientes
3. Se ve la lista de pacientes
4. Doble clic en "María López"
5. Se abre ventana con todos sus diagnósticos históricos
```

### Caso 3: Editar un Síntoma
```
1. Admin → Síntomas
2. Selecciona "Fiebre" de la tabla
3. Botón "Editar"
4. Modifica la descripción
5. Guardar
```

---

## ⌨️ Atajos y Consejos

| Acción | Atajo/Tip |
|--------|-----------|
| Ver historial paciente | Doble clic en paciente |
| Refrescar datos | Botón "Refrescar" en cualquier sección |
| Buscar rápido | Botón "Buscar" + término |
| Volver | Botón "Volver" o cerrar ventana |

---

## ⚠️ Validaciones y Restricciones

### Síntomas
- ✓ El nombre es requerido
- ✓ No se permiten nombres duplicados
- ✓ La descripción es opcional

### Signos
- ✓ El nombre es requerido
- ✓ No se permiten nombres duplicados
- ✓ La descripción es opcional

### Pacientes
- ✓ Nombre y Apellido requeridos
- ✓ Fecha de nacimiento: formato YYYY-MM-DD (ej: 1990-05-15)
- ✓ Email: formato válido (opcional)
- ✓ Teléfono: formato válido (opcional)

---

## 🐛 Solución de Problemas

### Problema: "No se puede ver el historial del paciente"
**Solución**: Asegúrate de hacer **doble clic** (no un solo clic). Debe aparecer un mensaje si no lo haces correctamente.

### Problema: "No puedo crear síntomas"
**Solución**: Verifica que tengas rol de Admin o Médico. Solo estos roles pueden crear síntomas.

### Problema: "La tabla de pacientes está vacía"
**Solución**: Primero debe haber pacientes en el sistema. Ve a "Pacientes" → "Agregar" para crear uno.

### Problema: "El síntoma no se guarda"
**Solución**: Verifica:
1. El nombre no esté vacío
2. El nombre no sea duplicado (ya existe)
3. Haya conectividad con la base de datos

---

## 📞 Contacto y Soporte

Para problemas o sugerencias:
- Consulta el archivo `MEJORAS_IMPLEMENTADAS.md`
- Revisa los logs de la aplicación
- Contacta al administrador del sistema

---

## 📚 Archivos Relacionados

- `front.py` - Interfaz gráfica (actualizada)
- `database.py` - Base de datos
- `models.py` - Modelos de datos
- `medical_system.db` - Archivo de base de datos SQLite

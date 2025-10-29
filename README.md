# 🏥 Motor Diagnóstico Médico - Sistema de Gestión

## 📌 Descripción

**Motor Diagnóstico Médico** es una aplicación de escritorio para gestionar pacientes, diagnósticos, síntomas y signos clínicos. Diseñada para médicos, administradores y auxiliares médicos.

**Versión**: 1.2.0 (Motor de Inferencia Automático)  
**Última actualización**: 28 de Octubre de 2025

---

## 🎯 Características Principales

### ✅ Gestión de Síntomas (NUEVO)
- Crear, editar y eliminar síntomas médicos
- Búsqueda y filtrado
- Validación de duplicados

### ✅ Historial Médico Interactivo (MEJORADO)
- Doble clic en paciente para ver historial completo
- Diagnósticos históricos ordenados por fecha
- Información del médico responsable

### ✅ Gestión de Pacientes
- Registro completo de pacientes
- Cálculo automático de edad
- Información de contacto

### ✅ Control de Diagnósticos (NUEVO - Motor de Inferencia)
- **Consulta médica completa** con motor de inferencia automático
- Selección de síntomas y signos clínicos
- **Diagnóstico automático** basado en IA
- Sugerencia de enfermedades con % de certeza
- Registro completo en historial médico

### ✅ Gestión de Usuarios y Roles
- Tres niveles de acceso (Admin, Médico, Auxiliar)
- Control de permisos basado en roles
- Autenticación segura

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.7+
- tkinter (incluido con Python)
- SQLite3 (incluido con Python)

### Instalación

1. **Clonar o descargar el proyecto**
```bash
cd C:\Users\Orusuko\MotorInferencia
```

2. **(OPCIONAL) Cargar datos de ejemplo** - Recomendado para probar el motor de inferencia
```bash
python ejemplo_datos_iniciales.py
```
Este script crea síntomas, enfermedades y sus asociaciones automáticamente.

3. **Ejecutar la aplicación**
```bash
python front.py
```

4. **Credenciales por defecto**
```
Usuario: admin
Contraseña: admin123
```

---

## 📚 Documentación

### 📖 Guías Disponibles

| Archivo | Contenido |
|---------|-----------|
| **README.md** | Este archivo (inicio rápido) |
| **GUIA_USUARIO.md** | Manual completo de usuario con casos de uso |
| **GUIA_CONSULTA_MEDICA.md** | 🆕 Guía completa del motor de inferencia |
| **MEJORAS_IMPLEMENTADAS.md** | Detalles técnicos de todas las mejoras |
| **RESUMEN_CAMBIOS.md** | Resumen ejecutivo de cambios |
| **ejemplo_datos_iniciales.py** | 🆕 Script para cargar datos de prueba |

---

## 🎮 Uso Básico

### Para Ver el Historial de un Paciente (NUEVO)
```
1. Ir a "Pacientes"
2. Hacer DOBLE CLIC en el paciente deseado
3. Se abrirá una ventana con su historial completo
```

### Para Crear un Nuevo Síntoma (NUEVO)
```
1. Ir a "Síntomas" (solo Admin/Médicos)
2. Hacer clic en "Agregar"
3. Llenar el formulario
4. Guardar
```

### Para Buscar Síntomas
```
1. Ir a "Síntomas"
2. Hacer clic en "Buscar"
3. Ingresa el término de búsqueda
4. Ver resultados
```

### Para Realizar una Consulta Médica (NUEVO - Motor de Inferencia)
```
1. Ir a "Diagnósticos" → "Agregar"
2. Seleccionar el paciente
3. Marcar síntomas observados
4. (Opcional) Marcar signos clínicos
5. Clic en "🔍 Analizar (Motor de Inferencia)"
6. El sistema sugiere enfermedades con % de certeza
7. Agregar notas médicas
8. Guardar consulta
9. ¡El diagnóstico se guarda automáticamente en el historial!
```

---

## 🏗️ Estructura del Proyecto

```
MotorInferencia/
├── front.py                      # Interfaz gráfica (ACTUALIZADO)
├── models.py                     # Modelos de datos
├── database.py                   # Gestión de base de datos
├── medical_system.db             # Base de datos SQLite
├── README.md                     # Este archivo
├── GUIA_USUARIO.md              # Manual de usuario
├── MEJORAS_IMPLEMENTADAS.md     # Documentación técnica
└── RESUMEN_CAMBIOS.md           # Resumen ejecutivo
```

---

## 👥 Roles y Permisos

### Administrador
- ✅ Gestionar usuarios
- ✅ Gestionar pacientes
- ✅ Gestionar enfermedades
- ✅ Gestionar síntomas
- ✅ Ver historial

### Médico
- ✅ Gestionar pacientes
- ✅ Crear diagnósticos
- ✅ Gestionar síntomas
- ✅ Ver historial

### Auxiliar
- ✅ Ver pacientes (solo lectura)
- ✅ Ver historial (solo lectura)

---

## 🔧 Cambios Recientes (v1.2.0)

### 🆕 Nuevas Funcionalidades
1. **Motor de Inferencia Automático** ⭐ NUEVO
   - Diagnóstico automático basado en síntomas y signos
   - Algoritmo inteligente con % de certeza
   - Sugerencia de top 5 enfermedades más probables
   - Integración completa con historial médico

2. **Formulario de Consulta Médica Completo** ⭐ NUEVO
   - Selección de paciente
   - Selección múltiple de síntomas
   - Selección de signos clínicos (opcional)
   - Análisis automático con IA
   - Notas médicas
   - Guardado completo en historial

3. **Gestión de Síntomas Completa**
   - Agregar síntomas
   - Editar síntomas
   - Eliminar síntomas
   - Buscar síntomas

4. **Historial Interactivo**
   - Doble clic en paciente abre historial
   - Vista completa de diagnósticos
   - Información del médico responsable

5. **Gestión de Signos Clínicos**
   - Similar a síntomas
   - Disponible para administradores

6. **Script de Datos de Ejemplo** ⭐ NUEVO
   - Carga automática de síntomas
   - Enfermedades pre-configuradas
   - Asociaciones listas para usar

### Mejoras de UX
- Instrucciones visuales en cada sección
- Validaciones automáticas
- Mensajes de confirmación
- Interfaz mejorada

---

## 📊 Ejemplo de Uso

### Caso 1: Crear y usar un Síntoma
```
1. Admin login: admin / admin123
2. Menú → Síntomas
3. Botón "Agregar"
4. Nombre: "Fiebre"
5. Descripción: "Temperatura corporal elevada"
6. Guardar
```

### Caso 2: Ver Historial de Paciente
```
1. Médico login
2. Menú → Pacientes
3. DOBLE CLIC en "Juan Pérez"
4. Se abre ventana con todos sus diagnósticos
5. Ver fechas, enfermedades, médico responsable
```

---

## 🐛 Solución de Problemas

### "No puedo ver el historial"
- Asegúrate de hacer **DOBLE clic** (no un solo clic)

### "Los síntomas no aparecen"
- Solo Admin y Médicos pueden crear síntomas
- Verifica tu rol en el sistema

### "La tabla está vacía"
- Primero debe haber datos en el sistema
- Usa "Agregar" para crear nuevos registros

### "Error de validación"
- El nombre no puede estar vacío
- Los nombres no pueden ser duplicados
- Revisa el formato de los datos

---

## 📞 Soporte y Contribuciones

Para reportar problemas o sugerir mejoras:
1. Consulta la documentación incluida
2. Revisa los logs de la aplicación
3. Contacta al administrador del sistema

---

## 📋 Requisitos Futuros

- ✏️ Implementar formulario completo de diagnóstico
- ✏️ Asociar síntomas/signos a enfermedades
- ✏️ Exportar historial a PDF
- ✏️ Dashboard de médico
- ✏️ API REST

---

## 📄 Licencia

Proyecto de gestión médica para uso interno.

---

## ✨ Características Destacadas

- 🔒 **Seguro**: Control de permisos por rol
- 🎯 **Intuitivo**: Interfaz clara y fácil de usar
- 📊 **Completo**: Gestión integral de pacientes
- 🚀 **Rápido**: Búsquedas y filtrados optimizados
- 📱 **Responsive**: Interfaz adaptable
- 🛡️ **Validado**: Validaciones en todos los formularios

---

## 🎉 ¡Listo para Usar!

La aplicación está completamente funcional y lista para producción.

**Próximo paso**: Lee `GUIA_USUARIO.md` para conocer todas las funcionalidades en detalle.

---

**Motor Diagnóstico Médico v1.2.0 con IA** | 28 de Octubre de 2025

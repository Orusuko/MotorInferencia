"""
Script para actualizar las asociaciones sintoma-enfermedad correctamente.
Ejecutar: python actualizar_sintomas.py
"""

from database import db
import sqlite3

# Definir claramente qué síntomas tiene cada enfermedad
asociaciones_correctas = {
    'Gripe (Influenza)': ['Fiebre', 'Tos seca', 'Dolor de cabeza', 'Fatiga', 'Dolor muscular'],
    'Resfriado comun': ['Tos seca', 'Dolor de cabeza', 'Fatiga'],
    'COVID-19': ['Fiebre', 'Tos seca', 'Fatiga'],
    'Faringitis': ['Dolor de cabeza', 'Fiebre'],
    'Bronquitis': ['Tos seca', 'Fatiga', 'Fiebre'],
    'Neumania': ['Fiebre', 'Tos seca', 'Fatiga'],
}

print("[INICIO] Actualizando asociaciones sintoma-enfermedad...")

conn = db.create_connection()
if conn:
    cursor = conn.cursor()
    
    # Primero, limpiar todas las asociaciones existentes
    print("[PASO 1] Limpiando asociaciones existentes...")
    cursor.execute("DELETE FROM enfermedad_sintoma")
    conn.commit()
    print("[OK] Asociaciones limpias")
    
    # Obtener IDs de síntomas y enfermedades
    cursor.execute("SELECT id, nombre FROM sintomas")
    sintomas_dict = {nombre: id_s for id_s, nombre in cursor.fetchall()}
    
    cursor.execute("SELECT id, nombre FROM enfermedades")
    enfermedades_dict = {nombre: id_e for id_e, nombre in cursor.fetchall()}
    
    print(f"\n[PASO 2] Creando nuevas asociaciones...")
    print(f"Sintomas disponibles: {list(sintomas_dict.keys())}")
    print(f"Enfermedades disponibles: {list(enfermedades_dict.keys())}\n")
    
    # Crear las nuevas asociaciones
    for enfermedad_nombre, sintomas_nombres in asociaciones_correctas.items():
        if enfermedad_nombre not in enfermedades_dict:
            print(f"[ADVERTENCIA] Enfermedad '{enfermedad_nombre}' no encontrada en BD")
            continue
        
        enfermedad_id = enfermedades_dict[enfermedad_nombre]
        
        for sintoma_nombre in sintomas_nombres:
            if sintoma_nombre not in sintomas_dict:
                print(f"[ADVERTENCIA] Sintoma '{sintoma_nombre}' no encontrado en BD")
                continue
            
            sintoma_id = sintomas_dict[sintoma_nombre]
            
            # Insertar la asociación
            cursor.execute(
                "INSERT INTO enfermedad_sintoma (enfermedad_id, sintoma_id) VALUES (?, ?)",
                (enfermedad_id, sintoma_id)
            )
            print(f"[OK] {enfermedad_nombre} -> {sintoma_nombre}")
    
    conn.commit()
    
    # Verificar las asociaciones creadas
    print("\n[PASO 3] Verificando asociaciones creadas...")
    cursor.execute("""
        SELECT e.nombre, GROUP_CONCAT(s.nombre, ', ')
        FROM enfermedades e
        LEFT JOIN enfermedad_sintoma es ON e.id = es.enfermedad_id
        LEFT JOIN sintomas s ON es.sintoma_id = s.id
        GROUP BY e.id
    """)
    
    for enfermedad, sintomas in cursor.fetchall():
        print(f"  {enfermedad}: {sintomas}")
    
    conn.close()
    print("\n[EXITO] Todas las asociaciones actualizadas correctamente!")
    print("Ahora puedes ver los sintomas en: Menu > Enfermedades > Refrescar")

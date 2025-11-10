"""
Script para analizar enfermedades y sus sintomas asociados.
Ayuda a entender que combinaciones de sintomas dan que diagnosticos.
"""

from database import db
from models import MotorInferencia

print("=" * 100)
print("ANALISIS DE ENFERMEDADES Y SINTOMAS")
print("=" * 100)

# Obtener todas las enfermedades
enfermedades = db.select('enfermedades', 'id, nombre, descripcion, tratamiento_base')

print("\n[ENFERMEDADES EN EL SISTEMA]\n")

enfermedades_dict = {}
for enf in enfermedades:
    enf_id, nombre, descripcion, tratamiento = enf
    enfermedades_dict[enf_id] = nombre
    
    print(f"\n{'='*100}")
    print(f"[ENFERMEDAD] {nombre.upper()}")
    print(f"{'='*100}")
    print(f"Descripcion: {descripcion}")
    print(f"Tratamiento: {tratamiento}\n")
    
    # Obtener sintomas de cada enfermedad
    conn = db.create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.nombre, s.descripcion
        FROM sintomas s
        JOIN enfermedad_sintoma es ON s.id = es.sintoma_id
        WHERE es.enfermedad_id = ?
        ORDER BY s.nombre
    """, (enf_id,))
    sintomas = cursor.fetchall()
    conn.close()
    
    if sintomas:
        print("Sintomas asociados:")
        for i, sint in enumerate(sintomas, 1):
            print(f"  {i}. {sint[1]} (ID: {sint[0]})")
            if sint[2]:
                print(f"     - {sint[2]}")
    else:
        print("[AVISO] Sintomas: Ninguno configurado")

# Obtener todos los sintomas
print("\n\n" + "=" * 100)
print("[SINTOMAS DISPONIBLES EN EL SISTEMA]:")
print("=" * 100 + "\n")

sintomas_list = db.select('sintomas', 'id, nombre, descripcion')
sintomas_dict = {}

for sint in sintomas_list:
    sintomas_dict[sint[0]] = sint[1]
    print(f"ID {sint[0]:2d}: {sint[1]:30s} - {sint[2] or 'Sin descripcion'}")

# Probar combinaciones
print("\n\n" + "=" * 100)
print("[PRUEBA DE COMBINACIONES DE SINTOMAS]:")
print("=" * 100 + "\n")

# Ejemplo 1: Sintomas de Influenza (Gripe)
print("\n[1] COMBINACION ACTUAL (que da Influenza):")
print("-" * 100)
print("Sintomas: Fiebre (1), Dolor de Cabeza (2), Dolor Muscular (3)")
resultado = MotorInferencia.diagnosticar([1, 2, 3], [])
if resultado:
    print("\nResultado del Motor de Inferencia:")
    for i, diag in enumerate(resultado[:3], 1):  # Mostrar top 3
        print(f"  {i}. {diag['nombre']:30s} - Certeza: {diag['porcentaje']:6.2f}% "
              f"({diag['sintomas_coincidentes']}/{diag['total_sintomas']} sintomas)")

# Ejemplo 2: Sintomas que podrian dar otro resultado
print("\n\n[2] COMBINACIONES PARA OBTENER RESULTADOS DIFERENTES:")
print("-" * 100)

# Analizar que sintomas tiene cada enfermedad
conn = db.create_connection()
cursor = conn.cursor()

# Buscar enfermedades
enfermedades_especiales = {}
cursor.execute("""
    SELECT DISTINCT e.id, e.nombre
    FROM enfermedades e
    ORDER BY e.nombre
""")
for eid, ename in cursor.fetchall():
    cursor.execute("""
        SELECT s.id, s.nombre
        FROM sintomas s
        JOIN enfermedad_sintoma es ON s.id = es.sintoma_id
        WHERE es.enfermedad_id = ?
    """, (eid,))
    enfermedades_especiales[eid] = {
        'nombre': ename,
        'sintomas': [row[0] for row in cursor.fetchall()]
    }

conn.close()

# Mostrar combinaciones alternativas
print("\nEnfermedades alternativas y sintomas para obtenerlas:\n")

contador = 1
for eid, enf_data in enfermedades_especiales.items():
    nombre = enf_data['nombre']
    sintomas_ids = enf_data['sintomas']
    
    if sintomas_ids and nombre.lower() != 'gripe' and nombre.lower() != 'influenza':
        # Tomar primeros 3 sintomas
        sintomas_prueba = sintomas_ids[:3] if len(sintomas_ids) >= 3 else sintomas_ids
        
        if sintomas_prueba:
            resultado = MotorInferencia.diagnosticar(sintomas_prueba, [])
            
            nombres_sintomas = [sintomas_dict.get(sid, f"ID {sid}") for sid in sintomas_prueba]
            print(f"\nOPCION {contador}: Para obtener '{nombre}':")
            print(f"   Sintomas a seleccionar: {', '.join(nombres_sintomas)}")
            print(f"   (IDs: {', '.join(map(str, sintomas_prueba))})")
            
            if resultado:
                print(f"   Resultados esperados:")
                for i, diag in enumerate(resultado[:2], 1):
                    print(f"     {i}. {diag['nombre']:30s} - {diag['porcentaje']:6.2f}%")
            
            contador += 1

print("\n" + "=" * 100)
print("RESUMEN: Usa las combinaciones de arriba para probar diferentes diagnosticos")
print("=" * 100)

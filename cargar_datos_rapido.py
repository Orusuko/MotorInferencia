"""
Script para cargar enfermedades y sintomas en la base de datos.
Ejecutar: python cargar_datos_rapido.py
"""

from database import db

# Crear sintomas
sintomas_data = [
    {'nombre': 'Fiebre', 'descripcion': 'Temperatura corporal elevada por encima de 38C'},
    {'nombre': 'Tos seca', 'descripcion': 'Tos sin expectoracion'},
    {'nombre': 'Dolor de cabeza', 'descripcion': 'Cefalea de intensidad variable'},
    {'nombre': 'Fatiga', 'descripcion': 'Cansancio y debilidad generalizada'},
    {'nombre': 'Dolor muscular', 'descripcion': 'Mialgia en diferentes grupos musculares'},
]

sintomas_ids = {}
print("[SINTOMAS] Cargando sintomas...")
for sintoma in sintomas_data:
    existing = db.select('sintomas', where="nombre = ?", params=(sintoma['nombre'],), fetch_one=True)
    if not existing:
        sid = db.insert('sintomas', sintoma)
        if sid:
            sintomas_ids[sintoma['nombre']] = sid
            print(f"[OK] {sintoma['nombre']}")

# Crear enfermedades
enfermedades_data = [
    {
        'nombre': 'Gripe (Influenza)',
        'descripcion': 'Infeccion viral respiratoria aguda causada por el virus de la influenza. Altamente contagiosa.',
        'tratamiento_base': 'Reposo, hidratacion abundante, antipiricos (paracetamol), antivirales en casos graves'
    },
    {
        'nombre': 'Resfriado comun',
        'descripcion': 'Infeccion viral leve de las vias respiratorias superiores. Autolimitada.',
        'tratamiento_base': 'Sintomatico: reposo, liquidos, analgesicos. No requiere antibioticos'
    },
    {
        'nombre': 'COVID-19',
        'descripcion': 'Enfermedad causada por el coronavirus SARS-CoV-2. Puede ser leve o grave.',
        'tratamiento_base': 'Aislamiento, oxigenoterapia si necesario, antivirales segun protocolo, monitoreo constante'
    },
    {
        'nombre': 'Faringitis',
        'descripcion': 'Inflamacion de la faringe, generalmente de origen viral o bacteriano.',
        'tratamiento_base': 'Analgesicos, antiinflamatorios, antibioticos si es bacteriana (Estreptococo)'
    },
    {
        'nombre': 'Bronquitis',
        'descripcion': 'Inflamacion de los bronquios principales. Puede ser viral o bacteriana.',
        'tratamiento_base': 'Reposo, humidificacion ambiental, expectorantes, broncodilatadores si necesario, antibioticos si es bacteriana'
    },
    {
        'nombre': 'Neumania',
        'descripcion': 'Infeccion del parenchima pulmonar con consolidacion. Puede ser viral o bacteriana.',
        'tratamiento_base': 'Antibioticos segun tipo, oxigenoterapia, reposo, hidratacion, monitoreo hospitalario en casos graves'
    },
]

enfermedades_ids = {}
print("\n[ENFERMEDADES] Cargando enfermedades...")
for enfermedad in enfermedades_data:
    existing = db.select('enfermedades', where="nombre = ?", params=(enfermedad['nombre'],), fetch_one=True)
    if not existing:
        eid = db.insert('enfermedades', enfermedad)
        if eid:
            enfermedades_ids[enfermedad['nombre']] = eid
            print(f"[OK] {enfermedad['nombre']}")

# Asociar sintomas a enfermedades
print("\n[ASOCIACIONES] Asociando sintomas a enfermedades...")
asociaciones = {
    'Gripe (Influenza)': ['Fiebre', 'Tos seca', 'Dolor de cabeza', 'Fatiga', 'Dolor muscular'],
    'Resfriado comun': ['Tos seca', 'Dolor de cabeza', 'Fatiga'],
    'COVID-19': ['Fiebre', 'Tos seca', 'Fatiga'],
    'Faringitis': ['Dolor de cabeza', 'Fiebre'],
    'Bronquitis': ['Tos seca', 'Fatiga', 'Fiebre'],
    'Neumania': ['Fiebre', 'Tos seca', 'Fatiga'],
}

conn = db.create_connection()
if conn:
    cursor = conn.cursor()
    for enfermedad, sintomas in asociaciones.items():
        if enfermedad in enfermedades_ids:
            for sintoma in sintomas:
                if sintoma in sintomas_ids:
                    cursor.execute(
                        "INSERT OR IGNORE INTO enfermedad_sintoma (enfermedad_id, sintoma_id) VALUES (?, ?)",
                        (enfermedades_ids[enfermedad], sintomas_ids[sintoma])
                    )
                    print(f"[OK] {enfermedad} - {sintoma}")
    conn.commit()
    conn.close()

print("\n[EXITO] Datos cargados exitosamente!")
print("Ahora puedes ver las enfermedades en: Menu > Enfermedades > Refrescar")

"""
Script de ejemplo para poblar la base de datos con datos iniciales.
Crea síntomas, signos, enfermedades y sus asociaciones.

IMPORTANTE: Este script es solo para pruebas iniciales.
Ejecutar una sola vez para crear datos de ejemplo.

Uso:
    python ejemplo_datos_iniciales.py
"""

from database import db

def crear_sintomas_ejemplo():
    """Crear síntomas de ejemplo."""
    print("\n📋 Creando síntomas de ejemplo...")
    
    sintomas = [
        {'nombre': 'Fiebre', 'descripcion': 'Temperatura corporal elevada por encima de 38°C'},
        {'nombre': 'Tos seca', 'descripcion': 'Tos sin expectoración'},
        {'nombre': 'Dolor de cabeza', 'descripcion': 'Cefalea de intensidad variable'},
        {'nombre': 'Fatiga', 'descripcion': 'Cansancio y debilidad generalizada'},
        {'nombre': 'Dolor muscular', 'descripcion': 'Mialgia en diferentes grupos musculares'},
        {'nombre': 'Dolor de garganta', 'descripcion': 'Odinofagia al tragar'},
        {'nombre': 'Congestión nasal', 'descripcion': 'Obstrucción de las vías nasales'},
        {'nombre': 'Náuseas', 'descripcion': 'Sensación de malestar estomacal'},
        {'nombre': 'Dificultad respiratoria', 'descripcion': 'Disnea o sensación de falta de aire'},
        {'nombre': 'Pérdida de olfato', 'descripcion': 'Anosmia o disminución del sentido del olfato'},
        # Nuevos síntomas
        {'nombre': 'Escalofríos', 'descripcion': 'Temblores corporales involuntarios por frío'},
        {'nombre': 'Vómitos', 'descripcion': 'Expulsión del contenido gástrico por la boca'},
        {'nombre': 'Diarrea', 'descripcion': 'Deposiciones frecuentes y acuosas'},
        {'nombre': 'Dolor abdominal', 'descripcion': 'Dolor en la región abdominal'},
        {'nombre': 'Mareos', 'descripcion': 'Sensación de inestabilidad o vértigo'},
        {'nombre': 'Sudoración excesiva', 'descripcion': 'Transpiración profusa sin causa aparente'},
        {'nombre': 'Tos con flemas', 'descripcion': 'Tos productiva con expectoración'},
        {'nombre': 'Dolor en el pecho', 'descripcion': 'Molestia torácica'},
        {'nombre': 'Ojos rojos', 'descripcion': 'Conjuntivitis o enrojecimiento ocular'},
        {'nombre': 'Erupción cutánea', 'descripcion': 'Aparición de manchas o ampollas en la piel'},
        # Síntomas adicionales faltantes
        {'nombre': 'Estornudo', 'descripcion': 'Expulsión brusca de aire por nariz y boca'},
        {'nombre': 'Dificultad para tragar', 'descripcion': 'Disfagia - dificultad en la deglución'},
        {'nombre': 'Dolor en el oído', 'descripcion': 'Otalgia - dolor en el conducto auditivo'},
        {'nombre': 'Picazón', 'descripcion': 'Prurito o comezón de la piel'},
    ]
    
    sintomas_ids = {}
    for sintoma in sintomas:
        # Verificar si ya existe
        existing = db.select('sintomas', where="nombre = ?", params=(sintoma['nombre'],), fetch_one=True)
        if existing:
            print(f"  ✓ Síntoma '{sintoma['nombre']}' ya existe")
            sintomas_ids[sintoma['nombre']] = existing[0]
        else:
            sid = db.insert('sintomas', sintoma)
            if sid:
                print(f"  ✅ Creado: {sintoma['nombre']}")
                sintomas_ids[sintoma['nombre']] = sid
            else:
                print(f"  ❌ Error al crear: {sintoma['nombre']}")
    
    return sintomas_ids


def crear_signos_ejemplo():
    """Crear signos clínicos de ejemplo."""
    print("\n🔬 Creando signos clínicos de ejemplo...")
    
    signos = [
        {'nombre': 'Temperatura elevada', 'descripcion': 'Temperatura corporal superior a 38°C medida'},
        {'nombre': 'Frecuencia respiratoria aumentada', 'descripcion': 'Taquipnea - más de 20 respiraciones por minuto'},
        {'nombre': 'Presión arterial elevada', 'descripcion': 'Hipertensión arterial'},
        {'nombre': 'Saturación de oxígeno baja', 'descripcion': 'SpO2 menor a 95%'},
    ]
    
    signos_ids = {}
    for signo in signos:
        # Verificar si ya existe
        existing = db.select('signos', where="nombre = ?", params=(signo['nombre'],), fetch_one=True)
        if existing:
            print(f"  ✓ Signo '{signo['nombre']}' ya existe")
            signos_ids[signo['nombre']] = existing[0]
        else:
            sid = db.insert('signos', signo)
            if sid:
                print(f"  ✅ Creado: {signo['nombre']}")
                signos_ids[signo['nombre']] = sid
            else:
                print(f"  ❌ Error al crear: {signo['nombre']}")
    
    return signos_ids


def crear_enfermedades_ejemplo():
    """Crear enfermedades de ejemplo."""
    print("\n🦠 Creando enfermedades de ejemplo...")
    
    enfermedades = [
        {
            'nombre': 'Gripe (Influenza)',
            'descripcion': 'Infección viral respiratoria aguda causada por el virus de la influenza. Altamente contagiosa.',
            'tratamiento_base': 'Reposo, hidratación abundante, antipiréticos (paracetamol), antivirales en casos graves'
        },
        {
            'nombre': 'Resfriado común',
            'descripcion': 'Infección viral leve de las vías respiratorias superiores. Autolimitada.',
            'tratamiento_base': 'Sintomático: reposo, líquidos, analgésicos. No requiere antibióticos'
        },
        {
            'nombre': 'COVID-19',
            'descripcion': 'Enfermedad causada por el coronavirus SARS-CoV-2. Puede ser leve o grave.',
            'tratamiento_base': 'Aislamiento, oxigenoterapia si necesario, antivirales según protocolo, monitoreo constante'
        },
        {
            'nombre': 'Faringitis',
            'descripcion': 'Inflamación de la faringe, generalmente de origen viral o bacteriano.',
            'tratamiento_base': 'Analgésicos, antiinflamatorios, antibióticos si es bacteriana (Estreptococo)'
        },
        # Nuevas enfermedades
        {
            'nombre': 'Bronquitis',
            'descripcion': 'Inflamación de los bronquios principales. Puede ser viral o bacteriana.',
            'tratamiento_base': 'Reposo, humidificación ambiental, expectorantes, broncodilatadores si necesario, antibióticos si es bacteriana'
        },
        {
            'nombre': 'Neumonía',
            'descripcion': 'Infección del parénquima pulmonar con consolidación. Puede ser viral o bacteriana.',
            'tratamiento_base': 'Antibióticos según tipo, oxigenoterapia, reposo, hidratación, monitoreo hospitalario en casos graves'
        },
        {
            'nombre': 'Sinusitis',
            'descripcion': 'Inflamación de los senos paranasales, generalmente por infección viral o bacteriana.',
            'tratamiento_base': 'Descongestivos, irrigación nasal salina, analgésicos, antibióticos si es bacteriana, corticoides nasales'
        },
        {
            'nombre': 'Gastroenteritis',
            'descripcion': 'Inflamación del estómago e intestino delgado por virus o bacteria (comúnmente norovirus o rotavirus).',
            'tratamiento_base': 'Rehidratación oral, dieta blanda, antieméticos si es necesario, evitar productos lácteos, antibióticos solo si es bacteriana'
        },
        {
            'nombre': 'Amigdalitis',
            'descripcion': 'Inflamación de las amígdalas, frecuentemente de origen bacteriano (Estreptococo del grupo A).',
            'tratamiento_base': 'Analgésicos, antiinflamatorios, enjuagues con agua salada, antibióticos si es bacteriana, reposo'
        },
        {
            'nombre': 'Otitis media',
            'descripcion': 'Infección del oído medio, común en niños. Puede ser viral o bacteriana.',
            'tratamiento_base': 'Analgésicos, descongestionantes, antibióticos tópicos u orales, drenaje si es necesario'
        },
        {
            'nombre': 'Dengue',
            'descripcion': 'Enfermedad viral transmitida por mosquito Aedes aegypti. Puede ser clásico o hemorrágico.',
            'tratamiento_base': 'Reposo, hidratación abundante, paracetamol (evitar AINEs), vigilancia del nivel de plaquetas, hospitalización si es grave'
        },
        {
            'nombre': 'Alergia estacional',
            'descripcion': 'Respuesta inmunológica exagerada a alérgenos ambientales (polen, polvo).',
            'tratamiento_base': 'Antihistamínicos, descongestivos nasales, corticoides nasales, evitar alérgeno, antileucotrienoicos si es necesario'
        },
        {
            'nombre': 'Conjuntivitis alérgica',
            'descripcion': 'Inflamación de la conjuntiva por reacción alérgica.',
            'tratamiento_base': 'Gotas oftálmicas antihistamínicas, compresas frías, evitar alérgeno, corticoides oftálmicos en casos severos'
        },
        {
            'nombre': 'Varicela',
            'descripcion': 'Infección viral aguda por virus varicela-zóster. Altamente contagiosa.',
            'tratamiento_base': 'Aislamiento, antipiréticos, aciclovir si es necesario, baños con permanganato potásico, higiene para evitar infecciones secundarias'
        },
        {
            'nombre': 'Sarampión',
            'descripcion': 'Infección viral exantemática por virus del sarampión. Altamente contagiosa.',
            'tratamiento_base': 'Reposo, vitamina A, antipiréticos, hidratación, aislar paciente, antibióticos si hay sobreinfección bacteriana'
        },
    ]
    
    enfermedades_ids = {}
    for enfermedad in enfermedades:
        # Verificar si ya existe
        existing = db.select('enfermedades', where="nombre = ?", params=(enfermedad['nombre'],), fetch_one=True)
        if existing:
            print(f"  ✓ Enfermedad '{enfermedad['nombre']}' ya existe")
            enfermedades_ids[enfermedad['nombre']] = existing[0]
        else:
            eid = db.insert('enfermedades', enfermedad)
            if eid:
                print(f"  ✅ Creado: {enfermedad['nombre']}")
                enfermedades_ids[enfermedad['nombre']] = eid
            else:
                print(f"  ❌ Error al crear: {enfermedad['nombre']}")
    
    return enfermedades_ids


def asociar_sintomas_enfermedades(enfermedades_ids, sintomas_ids):
    """Asociar síntomas a enfermedades."""
    print("\n🔗 Asociando síntomas a enfermedades...")
    
    # Definir qué síntomas tiene cada enfermedad
    asociaciones = {
        'Gripe (Influenza)': [
            'Fiebre',
            'Tos seca',
            'Dolor de cabeza',
            'Fatiga',
            'Dolor muscular',
            'Escalofríos',
        ],
        'Resfriado común': [
            'Congestión nasal',
            'Dolor de garganta',
            'Tos seca',
            'Fatiga',
            'Estornudo',
        ],
        'COVID-19': [
            'Fiebre',
            'Tos seca',
            'Fatiga',
            'Pérdida de olfato',
            'Dificultad respiratoria',
            'Dolor muscular',
        ],
        'Faringitis': [
            'Dolor de garganta',
            'Fiebre',
            'Dolor de cabeza',
            'Dificultad para tragar',
        ],
        'Bronquitis': [
            'Tos con flemas',
            'Dificultad respiratoria',
            'Fatiga',
            'Fiebre',
            'Dolor en el pecho',
        ],
        'Neumonía': [
            'Fiebre',
            'Tos con flemas',
            'Dificultad respiratoria',
            'Dolor en el pecho',
            'Fatiga',
            'Escalofríos',
        ],
        'Sinusitis': [
            'Dolor de cabeza',
            'Congestión nasal',
            'Fiebre',
            'Tos seca',
        ],
        'Gastroenteritis': [
            'Vómitos',
            'Diarrea',
            'Dolor abdominal',
            'Náuseas',
            'Fatiga',
            'Fiebre',
        ],
        'Amigdalitis': [
            'Dolor de garganta',
            'Fiebre',
            'Dificultad para tragar',
            'Dolor de cabeza',
        ],
        'Otitis media': [
            'Dolor en el oído',
            'Fiebre',
            'Fatiga',
        ],
        'Dengue': [
            'Fiebre',
            'Dolor muscular',
            'Dolor de cabeza',
            'Fatiga',
            'Náuseas',
            'Erupción cutánea',
        ],
        'Alergia estacional': [
            'Congestión nasal',
            'Estornudo',
            'Ojos rojos',
            'Picazón',
        ],
        'Conjuntivitis alérgica': [
            'Ojos rojos',
            'Picazón',
            'Congestión nasal',
        ],
        'Varicela': [
            'Fiebre',
            'Erupción cutánea',
            'Dolor de cabeza',
            'Fatiga',
            'Escalofríos',
        ],
        'Sarampión': [
            'Fiebre',
            'Tos seca',
            'Congestión nasal',
            'Ojos rojos',
            'Erupción cutánea',
            'Dolor de cabeza',
        ],
    }
    
    conn = db.create_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor()
        
        for enfermedad, sintomas in asociaciones.items():
            if enfermedad not in enfermedades_ids:
                print(f"  ⚠️  Enfermedad '{enfermedad}' no encontrada")
                continue
            
            enfermedad_id = enfermedades_ids[enfermedad]
            
            for sintoma in sintomas:
                if sintoma not in sintomas_ids:
                    print(f"  ⚠️  Síntoma '{sintoma}' no encontrado")
                    continue
                
                sintoma_id = sintomas_ids[sintoma]
                
                # Verificar si ya existe la asociación
                cursor.execute(
                    "SELECT 1 FROM enfermedad_sintoma WHERE enfermedad_id = ? AND sintoma_id = ?",
                    (enfermedad_id, sintoma_id)
                )
                
                if cursor.fetchone():
                    print(f"  ✓ Ya existe: {enfermedad} - {sintoma}")
                else:
                    cursor.execute(
                        "INSERT INTO enfermedad_sintoma (enfermedad_id, sintoma_id) VALUES (?, ?)",
                        (enfermedad_id, sintoma_id)
                    )
                    print(f"  ✅ Asociado: {enfermedad} - {sintoma}")
        
        conn.commit()
        print("\n✅ Asociaciones creadas correctamente")
        
    except Exception as e:
        print(f"\n❌ Error al crear asociaciones: {e}")
        conn.rollback()
    finally:
        conn.close()


def asociar_signos_enfermedades(enfermedades_ids, signos_ids):
    """Asociar signos clínicos a enfermedades."""
    print("\n🔗 Asociando signos a enfermedades...")
    
    # Definir qué signos tiene cada enfermedad
    asociaciones = {
        'Gripe (Influenza)': [
            'Temperatura elevada',
            'Frecuencia respiratoria aumentada',
        ],
        'COVID-19': [
            'Temperatura elevada',
            'Saturación de oxígeno baja',
            'Frecuencia respiratoria aumentada',
        ],
        'Faringitis': [
            'Temperatura elevada',
        ],
    }
    
    conn = db.create_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor()
        
        for enfermedad, signos in asociaciones.items():
            if enfermedad not in enfermedades_ids:
                print(f"  ⚠️  Enfermedad '{enfermedad}' no encontrada")
                continue
            
            enfermedad_id = enfermedades_ids[enfermedad]
            
            for signo in signos:
                if signo not in signos_ids:
                    print(f"  ⚠️  Signo '{signo}' no encontrado")
                    continue
                
                signo_id = signos_ids[signo]
                
                # Verificar si ya existe la asociación
                cursor.execute(
                    "SELECT 1 FROM enfermedad_signo WHERE enfermedad_id = ? AND signo_id = ?",
                    (enfermedad_id, signo_id)
                )
                
                if cursor.fetchone():
                    print(f"  ✓ Ya existe: {enfermedad} - {signo}")
                else:
                    cursor.execute(
                        "INSERT INTO enfermedad_signo (enfermedad_id, signo_id) VALUES (?, ?)",
                        (enfermedad_id, signo_id)
                    )
                    print(f"  ✅ Asociado: {enfermedad} - {signo}")
        
        conn.commit()
        print("\n✅ Asociaciones de signos creadas correctamente")
        
    except Exception as e:
        print(f"\n❌ Error al crear asociaciones: {e}")
        conn.rollback()
    finally:
        conn.close()


def main():
    """Función principal."""
    print("=" * 70)
    print("  🏥 SCRIPT DE INICIALIZACIÓN DE DATOS DE EJEMPLO")
    print("=" * 70)
    print("\nEste script creará datos de ejemplo para probar el motor de inferencia.")
    print("Incluye: síntomas, signos, enfermedades y sus asociaciones.")
    
    respuesta = input("\n¿Deseas continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("\n❌ Operación cancelada")
        return
    
    # Crear datos
    sintomas_ids = crear_sintomas_ejemplo()
    signos_ids = crear_signos_ejemplo()
    enfermedades_ids = crear_enfermedades_ejemplo()
    
    # Crear asociaciones
    asociar_sintomas_enfermedades(enfermedades_ids, sintomas_ids)
    asociar_signos_enfermedades(enfermedades_ids, signos_ids)
    
    print("\n" + "=" * 70)
    print("  ✅ ¡DATOS DE EJEMPLO CREADOS EXITOSAMENTE!")
    print("=" * 70)
    print("\nAhora puedes:")
    print("  1. Ejecutar la aplicación: python front.py")
    print("  2. Ir a 'Diagnósticos' → 'Agregar'")
    print("  3. Seleccionar síntomas y usar el Motor de Inferencia")
    print("  4. Ver cómo el sistema sugiere diagnósticos automáticamente")
    print("\n💡 Tip: Prueba seleccionando 'Fiebre', 'Tos seca' y 'Fatiga'")
    print("         El sistema debería sugerir 'Gripe' con alta certeza\n")


if __name__ == "__main__":
    main()


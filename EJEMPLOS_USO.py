"""
EJEMPLOS DE USO DEL MOTOR DE INFERENCIA MÉDICO
Ejecuta: python EJEMPLOS_USO.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from motorInferencia import diagnosticar, MotorInferencia


# ============================================================================
# EJEMPLO 1: USO SIMPLE CON LA FUNCIÓN diagnosticar()
# ============================================================================
def ejemplo_1_simple():
    print("\n" + "="*80)
    print("EJEMPLO 1: Diagnóstico Simple (Función diagnosticar)")
    print("="*80)
    
    # Paciente reporta: Fiebre + Tos + Dolor de cabeza
    sintomas = [1, 2, 3]
    
    print("\n🏥 Paciente reporta los siguientes síntomas:")
    print("   • Fiebre (ID: 1)")
    print("   • Tos seca (ID: 2)")
    print("   • Dolor de cabeza (ID: 3)")
    
    print("\n🔍 Ejecutando diagnóstico...")
    resultados = diagnosticar(sintomas)
    
    print(f"\n✅ Se encontraron {len(resultados)} diagnósticos posibles:\n")
    
    for i, diag in enumerate(resultados, 1):
        print(f"{i}. {diag['nombre']:<25} - Certeza: {diag['certeza']:>6.2f}%")
    
    print(f"\n🎯 Diagnóstico principal: {resultados[0]['nombre']} ({resultados[0]['certeza']}%)")


# ============================================================================
# EJEMPLO 2: CON SÍNTOMAS Y SIGNOS
# ============================================================================
def ejemplo_2_con_signos():
    print("\n" + "="*80)
    print("EJEMPLO 2: Diagnóstico con Síntomas + Signos")
    print("="*80)
    
    sintomas = [1, 2, 4]  # Fiebre, Tos, Fatiga
    signos = [1, 2]       # Dos signos presentes
    
    print("\n🏥 Síntomas reportados:")
    print("   • Fiebre (ID: 1)")
    print("   • Tos seca (ID: 2)")
    print("   • Fatiga (ID: 4)")
    
    print("\n📋 Signos observados:")
    print("   • Signo 1 (ID: 1)")
    print("   • Signo 2 (ID: 2)")
    
    print("\n🔍 Ejecutando diagnóstico...")
    resultados = diagnosticar(sintomas, signos)
    
    print(f"\n✅ Resultados (con signos como contexto adicional):\n")
    
    for i, diag in enumerate(resultados[:3], 1):
        print(f"{i}. {diag['nombre']:<25} - Certeza: {diag['certeza']:>6.2f}%")
        print(f"   Síntomas: {diag['sintomas_coincidentes']}/{diag['total_sintomas']}")
        print(f"   Signos: {diag['signos_coincidentes']}/{diag['total_signos']}\n")


# ============================================================================
# EJEMPLO 3: DIAGNÓSTICO DETALLADO CON INFORMACIÓN COMPLETA
# ============================================================================
def ejemplo_3_detallado():
    print("\n" + "="*80)
    print("EJEMPLO 3: Diagnóstico Detallado")
    print("="*80)
    
    motor = MotorInferencia()
    
    # Todos los síntomas de gripe
    sintomas = [1, 2, 3, 4, 5]
    
    print("\n🏥 Paciente con síntomas completos:")
    print("   • Fiebre (ID: 1)")
    print("   • Tos seca (ID: 2)")
    print("   • Dolor de cabeza (ID: 3)")
    print("   • Fatiga (ID: 4)")
    print("   • Dolor muscular (ID: 5)")
    
    print("\n🔍 Ejecutando diagnóstico detallado...")
    resultado = motor.diagnosticar_detallado(sintomas, [])
    
    if resultado['diagnostico_principal']:
        diag = resultado['diagnostico_principal']
        
        print(f"\n🎯 DIAGNÓSTICO PRINCIPAL")
        print(f"   Enfermedad: {diag['nombre']}")
        print(f"   Certeza: {diag['certeza']}%")
        print(f"   Confiabilidad General: {resultado['confiabilidad_general']}%")
        
        print(f"\n📝 Descripción:")
        print(f"   {diag['descripcion']}")
        
        print(f"\n💊 Tratamiento Recomendado:")
        print(f"   {diag['tratamiento']}")
        
        print(f"\n📊 Estadísticas:")
        print(f"   Síntomas coincidentes: {diag['sintomas_coincidentes']}/{diag['total_sintomas']}")
        print(f"   Factor de confianza aplicado: 0.85")


# ============================================================================
# EJEMPLO 4: RAZONAMIENTO PASO A PASO (CÓMO FUNCIONA)
# ============================================================================
def ejemplo_4_paso_a_paso():
    print("\n" + "="*80)
    print("EJEMPLO 4: Razonamiento Paso a Paso (Forward Chaining)")
    print("="*80)
    
    motor = MotorInferencia()
    
    print("\n📚 PASO 1: Cargar Base de Conocimientos")
    base = motor.base_conocimiento
    print(f"   ✓ Reglas cargadas: {len(base.reglas)}")
    for regla in base.reglas[:3]:
        print(f"     - {regla.enfermedad_nombre}: {len(regla.antecedentes['sintomas'])} síntomas")
    
    print("\n🏥 PASO 2: Establecer Hechos del Paciente")
    sintomas = [1, 3]
    print(f"   ✓ Síntomas: {sintomas}")
    motor.establecer_hechos(sintomas, [])
    print(f"   ✓ Hechos establecidos: {motor.hechos}")
    
    print("\n🔄 PASO 3: Aplicar Reglas (Forward Chaining)")
    print("   Evaluando cada regla:")
    
    resultados = []
    for regla in base.reglas[:3]:
        se_aplica, certeza = regla.evaluar(sintomas, [])
        if se_aplica:
            resultados.append((regla, certeza))
            print(f"     ✓ {regla.enfermedad_nombre}: {certeza*100:.2f}% de certeza")
    
    print("\n📊 PASO 4: Ordenar por Certeza")
    resultados_ordenados = sorted(resultados, key=lambda x: x[1], reverse=True)
    for i, (regla, certeza) in enumerate(resultados_ordenados, 1):
        print(f"   {i}. {regla.enfermedad_nombre}: {certeza*100:.2f}%")
    
    print("\n✅ PASO 5: Diagnósticos Finales")
    diagnosticos = motor.razonar(sintomas, [])
    for diag in diagnosticos[:3]:
        print(f"   {diag['nombre']}: {diag['certeza']}%")


# ============================================================================
# EJEMPLO 5: COMPARACIÓN DE CASOS CLÍNICOS
# ============================================================================
def ejemplo_5_comparacion():
    print("\n" + "="*80)
    print("EJEMPLO 5: Comparación de Casos Clínicos")
    print("="*80)
    
    casos = [
        {
            'nombre': 'Caso 1: Síntomas respiratorios leves',
            'sintomas': [2, 3, 4],
            'descripcion': 'Tos + Dolor cabeza + Fatiga'
        },
        {
            'nombre': 'Caso 2: Síntomas de fiebre',
            'sintomas': [1, 3],
            'descripcion': 'Fiebre + Dolor cabeza'
        },
        {
            'nombre': 'Caso 3: Síntomas severos',
            'sintomas': [1, 2, 3, 4, 5],
            'descripcion': 'Todos los síntomas'
        }
    ]
    
    for caso in casos:
        print(f"\n{caso['nombre']}")
        print(f"   Síntomas: {caso['descripcion']}")
        
        resultados = diagnosticar(caso['sintomas'])
        print(f"   Diagnóstico principal: {resultados[0]['nombre']} ({resultados[0]['certeza']}%)")


# ============================================================================
# EJEMPLO 6: USO EN APLICACIÓN MÉDICA
# ============================================================================
def ejemplo_6_uso_aplicacion():
    print("\n" + "="*80)
    print("EJEMPLO 6: Integración en Aplicación Médica")
    print("="*80)
    
    print("\n💻 Código de integración en front.py:")
    print("""
    def analizar_y_diagnosticar():
        # Obtener síntomas seleccionados
        sintomas_seleccionados = [
            sint_id for sint_id, var in sintomas_vars.items() 
            if var.get()
        ]
        
        # Obtener signos seleccionados
        signos_seleccionados = [
            sign_id for sign_id, var in signos_vars.items() 
            if var.get()
        ]
        
        # USAR MOTOR DE INFERENCIA
        from motorInferencia import diagnosticar
        diagnosticos_sugeridos = diagnosticar(
            sintomas_seleccionados, 
            signos_seleccionados
        )
        
        # Obtener diagnóstico con mayor certeza
        diagnostico_principal = diagnosticos_sugeridos[0]
        
        # Mostrar al usuario
        messagebox.showinfo(
            "Diagnóstico",
            f"Enfermedad: {diagnostico_principal['nombre']}\\n"
            f"Certeza: {diagnostico_principal['certeza']}%"
        )
    """)
    
    print("\n✅ El motor se integra automáticamente en la aplicación")


# ============================================================================
# EJEMPLO 7: CÓMO EXTENDER EL MOTOR
# ============================================================================
def ejemplo_7_extension():
    print("\n" + "="*80)
    print("EJEMPLO 7: Cómo Extender el Motor")
    print("="*80)
    
    print("\n🔧 Opción 1: Agregar Nueva Enfermedad")
    print("""
    # En la base de datos:
    INSERT INTO enfermedades (nombre, descripcion, tratamiento_base)
    VALUES ('Alergia', 'Reacción inmunológica', 'Antihistamínicos');
    
    INSERT INTO enfermedad_sintoma VALUES (8, 2);  -- Tos
    INSERT INTO enfermedad_sintoma VALUES (8, 3);  -- Dolor cabeza
    
    # El motor cargará automáticamente la nueva regla
    """)
    
    print("\n🔧 Opción 2: Ajustar Factor de Confianza")
    print("""
    # En motorInferencia.py, línea ~111:
    consecuente={
        'enfermedad_id': enf_id,
        'certeza_base': 0.95  # Cambiar de 0.85 a 0.95
    }
    """)
    
    print("\n🔧 Opción 3: Cambiar Pesos (Síntomas vs Signos)")
    print("""
    # En motorInferencia.py, clase Regla:
    peso_sintomas: float = 0.8  # Aumentar de 0.7 a 0.8
    peso_signos: float = 0.2    # Disminuir de 0.3 a 0.2
    """)


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  EJEMPLOS DE USO: MOTOR DE INFERENCIA MÉDICO".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    try:
        ejemplo_1_simple()
        ejemplo_2_con_signos()
        ejemplo_3_detallado()
        ejemplo_4_paso_a_paso()
        ejemplo_5_comparacion()
        ejemplo_6_uso_aplicacion()
        ejemplo_7_extension()
        
        print("\n" + "="*80)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


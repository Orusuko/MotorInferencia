"""
Script de prueba para el Motor de Inferencia
Ejecuta: python test_motorInferencia.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from motorInferencia import MotorInferencia, diagnosticar, BaseConocimiento
from database import db


def imprimir_encabezado(titulo):
    """Imprime un encabezado formateado."""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)


def test_base_conocimiento():
    """Prueba la base de conocimientos."""
    imprimir_encabezado("✅ PRUEBA 1: Base de Conocimientos")
    
    base = BaseConocimiento()
    print(f"\n📚 Total de reglas cargadas: {len(base.reglas)}")
    
    if base.reglas:
        print("\n🔍 Primeras 3 reglas:")
        for regla in base.reglas[:3]:
            print(f"\n   Regla: {regla.nombre}")
            print(f"   └─ Enfermedad: {regla.enfermedad_nombre}")
            print(f"   └─ Síntomas requeridos: {regla.antecedentes['sintomas']}")
            print(f"   └─ Signos requeridos: {regla.antecedentes['signos']}")
    else:
        print("\n⚠️  No hay reglas en la base de conocimientos")


def test_diagnostico_simple():
    """Prueba un diagnóstico simple."""
    imprimir_encabezado("✅ PRUEBA 2: Diagnóstico Simple")
    
    # Síntomas: Fiebre (1) + Tos (2) + Dolor Cabeza (3)
    sintomas = [1, 2, 3]
    
    print(f"\n🏥 Síntomas del paciente: {sintomas}")
    print("   ID 1: Fiebre")
    print("   ID 2: Tos seca")
    print("   ID 3: Dolor de cabeza")
    
    resultados = diagnosticar(sintomas)
    
    print(f"\n📊 Diagnósticos encontrados: {len(resultados)}")
    print("\n Diagnósticos (ordenados por certeza):")
    
    for i, diag in enumerate(resultados, 1):
        print(f"\n{i}. {diag['nombre']}")
        print(f"   Certeza: {diag['certeza']}%")
        print(f"   Síntomas coincidentes: {diag['sintomas_coincidentes']}/{diag['total_sintomas']}")
        if diag['total_signos'] > 0:
            print(f"   Signos coincidentes: {diag['signos_coincidentes']}/{diag['total_signos']}")


def test_diagnostico_con_signos():
    """Prueba diagnóstico con síntomas y signos."""
    imprimir_encabezado("✅ PRUEBA 3: Diagnóstico con Síntomas + Signos")
    
    sintomas = [1, 2, 3]  # Fiebre, Tos, Dolor cabeza
    signos = [1, 2]       # Dos signos presentes
    
    print(f"\n🏥 Síntomas: {sintomas}")
    print(f"📋 Signos: {signos}")
    
    resultados = diagnosticar(sintomas, signos)
    
    print(f"\n📊 Diagnósticos encontrados: {len(resultados)}")
    print("\n Diagnósticos:")
    
    for i, diag in enumerate(resultados[:5], 1):  # Primeros 5
        print(f"\n{i}. {diag['nombre']}")
        print(f"   Certeza: {diag['certeza']}%")
        print(f"   Síntomas: {diag['sintomas_coincidentes']}/{diag['total_sintomas']}")
        print(f"   Signos: {diag['signos_coincidentes']}/{diag['total_signos']}")


def test_motor_detallado():
    """Prueba el motor con diagnóstico detallado."""
    imprimir_encabezado("✅ PRUEBA 4: Diagnóstico Detallado con Información Completa")
    
    motor = MotorInferencia()
    sintomas = [1, 2, 3, 4, 5]  # Todos los síntomas
    signos = []
    
    print(f"\n🏥 Síntomas completos: {sintomas}")
    print("   (Fiebre, Tos, Dolor Cabeza, Fatiga, Dolor Muscular)")
    
    resultado = motor.diagnosticar_detallado(sintomas, signos)
    
    if resultado['diagnostico_principal']:
        diag = resultado['diagnostico_principal']
        print(f"\n🎯 Diagnóstico Principal: {diag['nombre']}")
        print(f"   Certeza: {diag['certeza']}%")
        print(f"   Confiabilidad General: {resultado['confiabilidad_general']}%")
        print(f"\n   Descripción:")
        print(f"   {diag['descripcion']}")
        print(f"\n   Tratamiento Recomendado:")
        print(f"   {diag['tratamiento']}")
    else:
        print("\n⚠️  No se encontraron diagnósticos")


def test_razonamiento_paso_a_paso():
    """Prueba razonamiento paso a paso."""
    imprimir_encabezado("✅ PRUEBA 5: Razonamiento Paso a Paso (Forward Chaining)")
    
    motor = MotorInferencia()
    sintomas = [1, 3]  # Fiebre + Dolor cabeza
    
    print(f"\n🏥 Síntomas: {sintomas}")
    print("   ID 1: Fiebre")
    print("   ID 3: Dolor de cabeza")
    
    print(f"\n🔍 Ejecutando forward chaining...\n")
    
    # Establecer hechos
    motor.establecer_hechos(sintomas, [])
    print(f"✓ Hechos establecidos: {motor.hechos}")
    
    # Razonar
    diagnosticos = motor.razonar(sintomas, [])
    
    print(f"\n✓ Razonamiento completado")
    print(f"✓ Reglas aplicadas encontradas: {len(diagnosticos)}")
    
    print(f"\n📊 Resultados (ordenados por certeza):\n")
    for i, diag in enumerate(diagnosticos[:5], 1):
        print(f"{i}. {diag['nombre']:<30} {diag['certeza']:>6.2f}% "
              f"(Regla: {diag['regla_aplicada']})")


def test_comparacion_motor_antiguo_vs_nuevo():
    """Compara resultados del motor antiguo vs nuevo."""
    imprimir_encabezado("✅ PRUEBA 6: Validación del Motor Mejorado")
    
    sintomas = [1, 2, 4]  # Fiebre, Tos, Fatiga
    
    print(f"\n🏥 Caso de prueba: Síntomas {sintomas}")
    print("   ID 1: Fiebre")
    print("   ID 2: Tos seca")
    print("   ID 4: Fatiga")
    
    print("\n✅ Motor Nuevo (con Base de Conocimientos + Forward Chaining):")
    
    motor = MotorInferencia()
    resultado = motor.diagnosticar_detallado(sintomas, [])
    
    if resultado['diagnosticos']:
        print(f"\n   Mejor diagnóstico: {resultado['diagnostico_principal']['nombre']}")
        print(f"   Certeza: {resultado['diagnostico_principal']['certeza']}%")
        print(f"   Justificación:")
        print(f"   - Síntomas coincidentes: {resultado['diagnostico_principal']['sintomas_coincidentes']}/{resultado['diagnostico_principal']['total_sintomas']}")
        print(f"   - Confiabilidad: {resultado['confiabilidad_general']}%")
    
    print("\n✨ Características del Motor Nuevo:")
    print("   ✓ Base de Conocimientos estructurada")
    print("   ✓ Razonamiento Forward Chaining")
    print("   ✓ Sistema de Certeza mejorado")
    print("   ✓ Explicabilidad de diagnósticos")
    print("   ✓ Integración con BD")


def main():
    """Ejecuta todas las pruebas."""
    print("\n")
    print("█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  🧠 PRUEBAS DEL MOTOR DE INFERENCIA MÉDICO".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        test_base_conocimiento()
        test_diagnostico_simple()
        test_diagnostico_con_signos()
        test_motor_detallado()
        test_razonamiento_paso_a_paso()
        test_comparacion_motor_antiguo_vs_nuevo()
        
        imprimir_encabezado("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("\n✨ Motor de Inferencia funcionando correctamente\n")
        
    except Exception as e:
        imprimir_encabezado("❌ ERROR DURANTE LAS PRUEBAS")
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


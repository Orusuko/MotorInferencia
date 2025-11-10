from models import MotorInferencia

print("PRUEBA CON LOS SINTOMAS ACTUALES:")
print("Sintomas: Fiebre (1), Dolor de Cabeza (3), Dolor Muscular (5)")
print()

resultado = MotorInferencia.diagnosticar([1, 3, 5], [])

if resultado:
    print("Orden de diagnosticos (de mayor a menor certeza):")
    print()
    for i, diag in enumerate(resultado[:6], 1):
        print(f"{i}. {diag['nombre']:30s} - Certeza: {diag['porcentaje']:6.2f}%")


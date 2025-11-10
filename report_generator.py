"""
Módulo para generar reportes HTML de diagnósticos y consultas médicas.
"""

from datetime import datetime
from database import db

class ReportGenerator:
    """Generador de reportes HTML para consultas médicas."""
    
    @staticmethod
    def generate_diagnosis_report(diagnostico_id):
        """Generar reporte HTML de un diagnóstico específico."""
        try:
            conn = db.create_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            
            # Obtener información del diagnóstico
            cursor.execute("""
                SELECT d.id, d.fecha_diagnostico, d.notas,
                       p.nombre, p.apellido, p.genero, p.fecha_nacimiento,
                       p.direccion, p.telefono, p.correo,
                       u.nombre as medico_nombre
                FROM diagnosticos d
                JOIN pacientes p ON d.paciente_id = p.id
                JOIN usuarios u ON d.usuario_id = u.id
                WHERE d.id = ?
            """, (diagnostico_id,))
            
            diag_data = cursor.fetchone()
            if not diag_data:
                conn.close()
                return None
            
            diagnostico_id, fecha_diagnostico, notas, \
            paciente_nombre, paciente_apellido, genero, fecha_nacimiento, \
            direccion, telefono, correo, medico_nombre = diag_data
            
            # Obtener enfermedades diagnosticadas
            cursor.execute("""
                SELECT e.nombre, e.descripcion, e.tratamiento_base, de.certeza
                FROM diagnostico_enfermedad de
                JOIN enfermedades e ON de.enfermedad_id = e.id
                WHERE de.diagnostico_id = ?
                ORDER BY de.certeza DESC
            """, (diagnostico_id,))
            
            enfermedades = cursor.fetchall()
            
            # Obtener síntomas observados
            cursor.execute("""
                SELECT s.nombre, s.descripcion, ds.intensidad
                FROM diagnostico_sintoma ds
                JOIN sintomas s ON ds.sintoma_id = s.id
                WHERE ds.diagnostico_id = ?
                ORDER BY ds.intensidad DESC
            """, (diagnostico_id,))
            
            sintomas = cursor.fetchall()
            
            # Obtener signos observados
            cursor.execute("""
                SELECT s.nombre, s.descripcion, ds.valor
                FROM diagnostico_signo ds
                JOIN signos s ON ds.signo_id = s.id
                WHERE ds.diagnostico_id = ?
            """, (diagnostico_id,))
            
            signos = cursor.fetchall()
            
            conn.close()
            
            # Calcular edad
            from datetime import datetime as dt
            if fecha_nacimiento:
                birth_date = dt.fromisoformat(fecha_nacimiento)
                today = dt.today()
                edad = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                edad = "N/A"
            
            # Generar HTML
            html_content = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte de Consulta Médica</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        padding: 20px;
                        line-height: 1.6;
                        color: #333;
                    }}
                    
                    .container {{
                        max-width: 900px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 40px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    
                    .header {{
                        text-align: center;
                        border-bottom: 3px solid #1e40af;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }}
                    
                    .header h1 {{
                        color: #1e40af;
                        font-size: 28px;
                        margin-bottom: 5px;
                    }}
                    
                    .header p {{
                        color: #666;
                        font-size: 14px;
                    }}
                    
                    .section {{
                        margin-bottom: 30px;
                    }}
                    
                    .section-title {{
                        background-color: #1e40af;
                        color: white;
                        padding: 12px 15px;
                        border-radius: 4px;
                        font-size: 16px;
                        font-weight: bold;
                        margin-bottom: 15px;
                    }}
                    
                    .info-grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 20px;
                        margin-bottom: 20px;
                    }}
                    
                    .info-item {{
                        background-color: #f9f9f9;
                        padding: 15px;
                        border-left: 4px solid #2563eb;
                        border-radius: 4px;
                    }}
                    
                    .info-item label {{
                        font-weight: bold;
                        color: #1e40af;
                        display: block;
                        font-size: 12px;
                        text-transform: uppercase;
                        margin-bottom: 5px;
                    }}
                    
                    .info-item value {{
                        display: block;
                        font-size: 15px;
                        color: #333;
                    }}
                    
                    .list-item {{
                        background-color: #f9f9f9;
                        padding: 12px 15px;
                        margin-bottom: 10px;
                        border-left: 4px solid #10b981;
                        border-radius: 4px;
                    }}
                    
                    .list-item-title {{
                        font-weight: bold;
                        color: #1e40af;
                        font-size: 14px;
                    }}
                    
                    .list-item-desc {{
                        color: #666;
                        font-size: 13px;
                        margin-top: 5px;
                    }}
                    
                    .list-item-value {{
                        color: #10b981;
                        font-weight: bold;
                        font-size: 12px;
                        margin-top: 5px;
                        text-transform: uppercase;
                    }}
                    
                    .treatment-box {{
                        background-color: #fffbeb;
                        border: 2px solid #fbbf24;
                        padding: 15px;
                        border-radius: 4px;
                        margin-top: 10px;
                    }}
                    
                    .treatment-box h4 {{
                        color: #f59e0b;
                        font-size: 13px;
                        margin-bottom: 8px;
                        text-transform: uppercase;
                    }}
                    
                    .treatment-box p {{
                        color: #333;
                        font-size: 14px;
                        line-height: 1.5;
                    }}
                    
                    .empty-state {{
                        text-align: center;
                        color: #999;
                        padding: 20px;
                        background-color: #f9f9f9;
                        border-radius: 4px;
                    }}
                    
                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        padding-top: 20px;
                        border-top: 1px solid #e0e0e0;
                        color: #999;
                        font-size: 12px;
                    }}
                    
                    .notes-section {{
                        background-color: #e0f2fe;
                        border: 1px solid #0284c7;
                        padding: 15px;
                        border-radius: 4px;
                        margin-top: 10px;
                    }}
                    
                    .notes-section p {{
                        color: #0c4a6e;
                        font-size: 14px;
                        line-height: 1.6;
                    }}
                    
                    @media print {{
                        body {{
                            background-color: white;
                            padding: 0;
                        }}
                        .container {{
                            box-shadow: none;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏥 Reporte de Consulta Médica</h1>
                        <p>Motor Diagnóstico Médico</p>
                    </div>
                    
                    <!-- Información del Paciente -->
                    <div class="section">
                        <div class="section-title">👤 Información del Paciente</div>
                        <div class="info-grid">
                            <div class="info-item">
                                <label>Nombre Completo</label>
                                <value>{paciente_nombre} {paciente_apellido}</value>
                            </div>
                            <div class="info-item">
                                <label>Edad / Género</label>
                                <value>{edad} años / {genero or 'No especificado'}</value>
                            </div>
                            <div class="info-item">
                                <label>Teléfono</label>
                                <value>{telefono or 'No registrado'}</value>
                            </div>
                            <div class="info-item">
                                <label>Correo</label>
                                <value>{correo or 'No registrado'}</value>
                            </div>
                            <div class="info-item">
                                <label>Dirección</label>
                                <value>{direccion or 'No registrada'}</value>
                            </div>
                            <div class="info-item">
                                <label>Fecha de Nacimiento</label>
                                <value>{fecha_nacimiento or 'No registrada'}</value>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Información de la Consulta -->
                    <div class="section">
                        <div class="section-title">📋 Información de la Consulta</div>
                        <div class="info-grid">
                            <div class="info-item">
                                <label>Médico Responsable</label>
                                <value>{medico_nombre}</value>
                            </div>
                            <div class="info-item">
                                <label>Fecha y Hora de la Consulta</label>
                                <value>{fecha_diagnostico}</value>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Síntomas Observados -->
                    <div class="section">
                        <div class="section-title">🔍 Síntomas Observados</div>
                        {
                            ''.join([
                                f'''<div class="list-item">
                                    <div class="list-item-title">{sintoma[0]}</div>
                                    <div class="list-item-desc">{sintoma[1] or 'Sin descripción'}</div>
                                    <div class="list-item-value">Intensidad: {sintoma[2]}/10</div>
                                </div>'''
                                for sintoma in sintomas
                            ]) or '<div class="empty-state">No se registraron síntomas</div>'
                        }
                    </div>
                    
                    <!-- Signos Observados -->
                    <div class="section">
                        <div class="section-title">📊 Signos Observados</div>
                        {
                            ''.join([
                                f'''<div class="list-item">
                                    <div class="list-item-title">{signo[0]}</div>
                                    <div class="list-item-desc">{signo[1] or 'Sin descripción'}</div>
                                    <div class="list-item-value">Valor: {signo[2]}</div>
                                </div>'''
                                for signo in signos
                            ]) or '<div class="empty-state">No se registraron signos</div>'
                        }
                    </div>
                    
                    <!-- Diagnósticos -->
                    <div class="section">
                        <div class="section-title">🩺 Diagnósticos Identificados</div>
                        {
                            ''.join([
                                f'''<div class="list-item">
                                    <div class="list-item-title">{enfermedad[0]}</div>
                                    <div class="list-item-desc">{enfermedad[1] or 'Sin descripción'}</div>
                                    <div class="list-item-value">Certeza: {round(enfermedad[3] * 100, 2)}%</div>
                                    <div class="treatment-box">
                                        <h4>💊 Tratamiento Base Recomendado</h4>
                                        <p>{enfermedad[2] or 'No disponible'}</p>
                                    </div>
                                </div>'''
                                for enfermedad in enfermedades
                            ]) or '<div class="empty-state">No se identificaron diagnósticos</div>'
                        }
                    </div>
                    
                    <!-- Notas Adicionales -->
                    {
                        f'''<div class="section">
                            <div class="section-title">📝 Notas Adicionales</div>
                            <div class="notes-section">
                                <p>{notas or 'Sin notas adicionales'}</p>
                            </div>
                        </div>''' if notas else ''
                    }
                    
                    <!-- Footer -->
                    <div class="footer">
                        <p>Este reporte fue generado automáticamente por el Motor Diagnóstico Médico</p>
                        <p>Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>Para más información, contacte al médico responsable</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html_content
            
        except Exception as e:
            print(f"Error generando reporte: {e}")
            return None


# MEECETeacherManager/utils.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.utils import timezone

def generate_profile_pdf(teacher):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos actualizados
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50'),
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#2C3E50')
    )

    # Título y RUT
    elements.append(Paragraph(f"{teacher.name}", header_style))
    elements.append(Paragraph(f"RUT: {teacher.rut}", 
        ParagraphStyle(
            'RutStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=30,
            fontName='Helvetica'
        )
    ))
    
    if hasattr(teacher, 'profile'):
        # Título de la sección
        elements.append(Paragraph("Información del docente", 
            ParagraphStyle(
                'SectionStyle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2980B9'),
                spaceAfter=20,
                fontName='Helvetica-Bold'
            )
        ))
        
        # Datos del perfil
        profile_data = [
            ["Categoría:", Paragraph(teacher.profile.category.name, normal_style)],
            ["Correo Institucional:", Paragraph(teacher.profile.institutional_email or "No especificado", normal_style)],
            ["Correo Personal:", Paragraph(teacher.profile.personal_email or "No especificado", normal_style)],
            ["Celular:", Paragraph(teacher.profile.phone or "No especificado", normal_style)],
            ["Profesión:", Paragraph(teacher.profile.profession or "No especificado", normal_style)],
            ["Grado Académico:", Paragraph(teacher.profile.academic_degree or "No especificado", normal_style)],
        ]
        
        table = Table(profile_data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F6FA')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 10),
            
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            f"Este documento fue generado el {teacher.profile.updated_at.strftime('%d/%m/%Y %H:%M')}",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_CENTER
            )
        ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_schedule_pdf(teacher):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos actualizados
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50'),
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#2C3E50')
    )
    
    # Título y datos del docente
    elements.append(Paragraph(f"{teacher.name}", header_style))
    elements.append(Paragraph(f"RUT: {teacher.rut}", 
        ParagraphStyle(
            'RutStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=30,
            fontName='Helvetica'
        )
    ))
    
    if teacher.schedules.exists():
        # Datos de la tabla con Paragraph para manejar textos largos
        table_data = [[
            'Código',
            'Asignatura',
            'INTAKE',
            'Modalidad',
            'Día',
            'Horario',
            'Período',
            'Vacantes'
        ]]
        
        for schedule in teacher.schedules.all().order_by('day', 'start_time'):
            table_data.append([
                Paragraph(schedule.course.code, normal_style),
                Paragraph(schedule.course.name, normal_style),
                Paragraph(str(schedule.intake), normal_style),
                Paragraph(schedule.get_modality_display(), normal_style),
                Paragraph(schedule.get_day_display(), normal_style),
                Paragraph(f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}", normal_style),
                Paragraph(f"{schedule.start_date.strftime('%d/%m/%Y')} - {schedule.end_date.strftime('%d/%m/%Y')}", normal_style),
                Paragraph(str(schedule.vacancies), normal_style)
            ])
        
        # Ajustar anchos de columna
        col_widths = [
            0.8*inch,  # Código
            1.5*inch,  # Asignatura
            0.8*inch,  # INTAKE
            1.0*inch,  # Modalidad
            0.8*inch,  # Día
            1.0*inch,  # Horario
            1.3*inch,  # Período
            0.8*inch   # Vacantes
        ]
        
        # Crear y estilizar la tabla
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            # Estilos del encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Estilos del contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordes y espaciado
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2C3E50')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
    else:
        elements.append(
            Paragraph(
                "No hay carga horaria registrada para este docente.",
                styles['Normal']
            )
        )

    # Pie de página
    elements.append(Spacer(1, 30))
    elements.append(
        Paragraph(
            f"Documento generado el {timezone.localtime().strftime('%d/%m/%Y %H:%M')}",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_CENTER
            )
        )
    )
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_compliance_report_pdf(task_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos actualizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor('#2C3E50')
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#2C3E50'),
        fontName='Helvetica-Bold',  # Hacer el texto en negrita
        spaceBefore=15,  # Espacio antes del texto
        spaceAfter=10    # Espacio después del texto
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#2C3E50')
    )
    
    # Título del reporte
    elements.append(Paragraph("Reporte de Cumplimiento por Tarea", title_style))
    elements.append(Spacer(1, 20))
    
    for task in task_data:
        # Título de la tarea
        elements.append(Paragraph(task['name'], subtitle_style))
        elements.append(Spacer(1, 10))
        
        # Docentes que cumplen - ahora con el nuevo estilo y más espacio
        elements.append(Paragraph("Docentes que cumplen:", section_style))
        if task['completed_teachers']:
            data = [[Paragraph("Nombre", normal_style), Paragraph("RUT", normal_style)]]
            for teacher in task['completed_teachers']:
                data.append([
                    Paragraph(teacher['name'], normal_style),
                    Paragraph(teacher['rut'], normal_style)
                ])
            
            table = Table(data, colWidths=[4*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#27AE60')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#E8F5E9'), colors.white]),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No hay docentes que hayan completado esta tarea.", normal_style))
        
        elements.append(Spacer(1, 20))  # Aumentado el espacio entre secciones
        
        # Docentes pendientes - ahora con el nuevo estilo y más espacio
        elements.append(Paragraph("Docentes pendientes:", section_style))
        if task['pending_teachers']:
            data = [[Paragraph("Nombre", normal_style), Paragraph("RUT", normal_style)]]
            for teacher in task['pending_teachers']:
                data.append([
                    Paragraph(teacher['name'], normal_style),
                    Paragraph(teacher['rut'], normal_style)
                ])
            
            table = Table(data, colWidths=[4*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1C40F')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF9C4')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#F1C40F')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFF9C4'), colors.white]),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No hay docentes pendientes para esta tarea.", normal_style))
        
        elements.append(Spacer(1, 30))  # Aumentado el espacio entre tareas
    
    # Pie de página
    elements.append(Paragraph(
        f"Reporte generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
    ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_course_overview_pdf(schedules):
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50')
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.whitesmoke,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    )
    
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor('#2C3E50')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#2C3E50')
    )
    
    error_row_style = ParagraphStyle(
        'ErrorRow',
        parent=normal_style,
        textColor=colors.HexColor('#2C3E50')
    )
    
    conflict_style = ParagraphStyle(
        'ConflictStyle',
        parent=normal_style,
        textColor=colors.red,
        leading=12,
        leftIndent=10
    )
    
    elements.append(Paragraph("Resumen de Asignaturas y Horarios", title_style))
    
    # Agrupar por profesor
    teacher_schedules = {}
    for schedule in schedules:
        if schedule.teacher_id not in teacher_schedules:
            teacher_schedules[schedule.teacher_id] = {
                'name': schedule.teacher.name,
                'schedules': []
            }
        teacher_schedules[schedule.teacher_id]['schedules'].append(schedule)
    
    for teacher_id, data in teacher_schedules.items():
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Profesor: {data['name']}", subtitle_style))
        elements.append(Spacer(1, 10))
        
        # Datos de la tabla
        table_data = []
        # Encabezados
        headers = ["Asignatura", "Código", "Día", "Horario", "Período", "Modalidad", "MPA", "Estado"]
        table_data.append([Paragraph(h, header_style) for h in headers])
        
        for schedule in sorted(data['schedules'], key=lambda x: (x.start_date, x.day)):
            has_error = hasattr(schedule, 'conflicts') and schedule.conflicts
            has_mpa_match = False
            mpa_status = ""
            state_status = ""
            
            # Determinar estado MPA
            if hasattr(schedule, 'mpa_conflicts'):
                for match in schedule.mpa_conflicts:
                    if match['type'] == 'coincide':
                        has_mpa_match = True
                        mpa_status = f"✓ {match['sheet'].intake}"
                        break
                    elif match['type'] == 'no_encontrado':
                        mpa_status = "✗ No encontrado"
            
            # Determinar estado general
            if has_error:
                state_status = "⚠️ Ver detalles"
            elif not has_mpa_match:
                if hasattr(schedule, 'mpa_conflicts') and schedule.mpa_conflicts[0].get('intakes'):
                    state_status = "⚠️ Ver detalles"
                else:
                    state_status = "✓ OK"
            else:
                state_status = "✓ OK"
            
            row = [
                Paragraph(schedule.course.name, error_row_style if has_error else normal_style),
                Paragraph(schedule.course.code, error_row_style if has_error else normal_style),
                Paragraph(schedule.get_day_display(), error_row_style if has_error else normal_style),
                Paragraph(
                    f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}", 
                    error_row_style if has_error else normal_style
                ),
                Paragraph(
                    f"{schedule.start_date.strftime('%d/%m/%Y')} - {schedule.end_date.strftime('%d/%m/%Y')}", 
                    error_row_style if has_error else normal_style
                ),
                Paragraph(schedule.get_modality_display(), error_row_style if has_error else normal_style),
                Paragraph(
                    mpa_status,
                    ParagraphStyle(
                        'MpaStatus',
                        parent=normal_style,
                        textColor=colors.green if has_mpa_match else colors.red
                    )
                ),
                Paragraph(
                    state_status,
                    ParagraphStyle(
                        'StateStatus',
                        parent=normal_style,
                        textColor=colors.green if state_status.startswith("✓") else colors.orange
                    )
                )
            ]
            table_data.append(row)
            
            # Si hay conflictos, agregar una fila para cada error
            if has_error:
                for conflict in schedule.conflicts:
                    error_message = f"⚠️ {conflict['message']}"
                    # Agregar el mensaje de error en una sola celda que luego se expandirá
                    table_data.append([Paragraph(error_message, conflict_style)])
            
            # Si hay conflictos de MPA, mostrarlos
            if not has_mpa_match and hasattr(schedule, 'mpa_conflicts'):
                for match in schedule.mpa_conflicts:
                    if match['type'] == 'no_encontrado' and match.get('intakes'):
                        intakes_list = ", ".join(match['intakes'])
                        mpa_message = f"ℹ️ INTAKEs revisados: {intakes_list}"
                        table_data.append([Paragraph(mpa_message, ParagraphStyle(
                            'MpaInfo',
                            parent=conflict_style,
                            textColor=colors.blue
                        ))])
        
        # Crear tabla con anchos definidos
        col_widths = [2*inch, 0.8*inch, 0.8*inch, 1*inch, 1.5*inch, 1*inch, 1*inch, 1*inch]
        table = Table(table_data, colWidths=col_widths)
        
        # Estilos de la tabla
        table_style = [
            # Estilo del encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Aumentar tamaño de fuente de encabezados
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Más espacio debajo de encabezados
            ('TOPPADDING', (0, 0), (-1, 0), 10),  # Más espacio arriba de encabezados
            
            # Líneas y bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2C3E50')),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#2C3E50')),  # Línea más gruesa bajo encabezados
            
            # Alineación y espaciado del contenido
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Alinear contenido a la izquierda
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Padding izquierdo para mejor legibilidad
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Padding derecho para mejor legibilidad
            
            # Fondo alternado para las filas normales
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]

        # Agregar estilos específicos para las filas de error
        for i, row in enumerate(table_data[1:], 1):
            if len(row) == 6 and isinstance(row[0], Paragraph) and '⚠️' in row[0].text:
                # Color de fondo para la fila con error
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FFF3F3')))
            elif len(row) == 1 and isinstance(row[0], Paragraph) and '⚠️' in row[0].text:
                # Expandir y colorear la fila del mensaje de error
                table_style.extend([
                    ('SPAN', (0, i), (-1, i)),  # Expandir a todas las columnas
                    ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FFEBEE')),
                ])

        table.setStyle(TableStyle(table_style))
        elements.append(table)
    
    # Pie de página
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f"Reporte generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
    ))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer



def generate_mpa_validation_pdf(validation_results):
   buffer = BytesIO()
   doc = SimpleDocTemplate(
       buffer,
       pagesize=letter,
       rightMargin=50,
       leftMargin=50,
       topMargin=50,
       bottomMargin=50
   )
   elements = []
   styles = getSampleStyleSheet()

   def clean_text_for_pdf(text):
       if text is None:
           return ''
       return str(text).replace('\xa0', ' ').strip()

   def add_text_with_bullet(text, style):
       cleaned_text = clean_text_for_pdf(text)
       max_length = 80
       if len(cleaned_text) > max_length:
           parts = [cleaned_text[i:i+max_length] for i in range(0, len(cleaned_text), max_length)]
           for i, part in enumerate(parts):
               bullet = "• " if i == 0 else "  "
               elements.append(Paragraph(f"{bullet}{part}", style))
       else:
           elements.append(Paragraph(f"• {cleaned_text}", style))

   # Estilos personalizados
   title_style = ParagraphStyle(
       'CustomTitle',
       parent=styles['Heading1'],
       fontSize=16,
       spaceAfter=20,
       alignment=TA_CENTER,
       textColor=colors.HexColor('#2C3E50')
   )
   
   subtitle_style = ParagraphStyle(
       'CustomSubtitle',
       parent=styles['Heading2'],
       fontSize=14,
       spaceAfter=10,
       textColor=colors.HexColor('#2C3E50')
   )
   
   normal_style = ParagraphStyle(
       'CustomNormal',
       parent=styles['Normal'],
       fontSize=10,
       leading=12,
       textColor=colors.HexColor('#2C3E50')
   )

   error_style = ParagraphStyle(
       'Error',
       parent=normal_style,
       leftIndent=20,
       textColor=colors.red,
       leading=14
   )

   warning_style = ParagraphStyle(
       'Warning',
       parent=normal_style,
       leftIndent=20,
       textColor=colors.orange,
       leading=14
   )

   # Título con el filtro aplicado si existe
   title_text = "Reporte de Validación MPAs"
   if validation_results and 'filter_type' in validation_results[0]:
       filter_name = {
           'teacher_conflict': 'Conflictos de Profesor',
           'date_mismatch': 'Fechas Incorrectas',
           'invalid_saturday_schedule': 'Horario Sábado',
           'duration_mismatch': 'Duración Incorrecta',
           'large_gap': 'Intervalos Grandes'
       }.get(validation_results[0]['filter_type'], 'Todos los conflictos')
       title_text += f" - {filter_name}"

   elements.append(Paragraph(title_text, title_style))
   elements.append(Spacer(1, 20))

   for mpa_validation in validation_results:
       if not mpa_validation.get('sheets_validation', []):
           continue

       mpa = mpa_validation['mpa']
       elements.append(Paragraph(clean_text_for_pdf(mpa.program_name), subtitle_style))
       elements.append(Paragraph(f"Código: {clean_text_for_pdf(mpa.program_code)}", normal_style))
       elements.append(Spacer(1, 10))

       for sheet_validation in mpa_validation['sheets_validation']:
           if not sheet_validation['conflicts']:
               continue

           elements.append(Paragraph(clean_text_for_pdf(sheet_validation['sheet'].intake), subtitle_style))
           
           # Agrupar por severidad
           errors = [c for c in sheet_validation['conflicts'] if c['severity'] == 'error']
           warnings = [c for c in sheet_validation['conflicts'] if c['severity'] == 'warning']

           if errors:
               elements.append(Paragraph("Errores:", ParagraphStyle(
                   'ErrorTitle',
                   parent=normal_style,
                   textColor=colors.red,
                   fontName='Helvetica-Bold',
                   spaceAfter=6
               )))
               for error in errors:
                   add_text_with_bullet(error['message'], error_style)
                   if 'schedule' in error:
                       schedule = error['schedule']
                       details = f"   {schedule.course_code} - {schedule.day} {schedule.schedule}"
                       elements.append(Paragraph(details, ParagraphStyle(
                           'ErrorDetail',
                           parent=error_style,
                           leftIndent=40,
                           fontSize=9
                       )))
                   elements.append(Spacer(1, 3))

           if warnings:
               elements.append(Paragraph("Advertencias:", ParagraphStyle(
                   'WarningTitle',
                   parent=normal_style,
                   textColor=colors.orange,
                   fontName='Helvetica-Bold',
                   spaceAfter=6
               )))
               for warning in warnings:
                   add_text_with_bullet(warning['message'], warning_style)
                   if 'schedule' in warning:
                       schedule = warning['schedule']
                       details = f"   {schedule.course_code} - {schedule.day} {schedule.schedule}"
                       elements.append(Paragraph(details, ParagraphStyle(
                           'WarningDetail',
                           parent=warning_style,
                           leftIndent=40,
                           fontSize=9
                       )))
                   elements.append(Spacer(1, 3))

           elements.append(Spacer(1, 10))

   # Pie de página
   elements.append(Spacer(1, 20))
   elements.append(Paragraph(
       f"Reporte generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}",
       ParagraphStyle(
           'Footer',
           parent=styles['Normal'],
           fontSize=8,
           textColor=colors.grey,
           alignment=TA_CENTER
       )
   ))

   doc.build(elements)
   buffer.seek(0)
   return buffer


def generate_intake_summary_pdf(intake_status):
   buffer = BytesIO()
   doc = SimpleDocTemplate(
       buffer,
       pagesize=letter,
       rightMargin=50,
       leftMargin=50,
       topMargin=50,
       bottomMargin=50
   )
   elements = []
   styles = getSampleStyleSheet()
   
   def clean_text_for_pdf(text):
       if text is None:
           return ''
       return str(text).replace('\xa0', ' ').strip()
   
   # Estilos
   title_style = ParagraphStyle(
       'CustomTitle',
       parent=styles['Heading1'],
       fontSize=16,
       spaceAfter=20,
       alignment=TA_CENTER,
       textColor=colors.HexColor('#2C3E50')
   )
   
   subtitle_style = ParagraphStyle(
       'CustomSubtitle',
       parent=styles['Heading2'],
       fontSize=14,
       spaceAfter=10,
       textColor=colors.HexColor('#2C3E50')
   )
   
   normal_style = ParagraphStyle(
       'CustomNormal',
       parent=styles['Normal'],
       fontSize=10,
       leading=12,
       textColor=colors.HexColor('#2C3E50')
   )

   elements.append(Paragraph("Resumen de INTAKEs", title_style))
   elements.append(Spacer(1, 20))

   for status in intake_status:
       # Título del INTAKE
       elements.append(Paragraph(clean_text_for_pdf(status['sheet'].intake), subtitle_style))
       
       # Información general
       if status['global_start'] and status['global_end']:
           general_info = [
               ['Periodo:', f"{status['global_start'].strftime('%d/%m/%Y')} - {status['global_end'].strftime('%d/%m/%Y')}"],
               ['Estado:', 'Finalizado' if status['is_finished'] else 'En curso']
           ]
           
           table = Table(general_info, colWidths=[100, 300])
           table.setStyle(TableStyle([
               ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
               ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
               ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
               ('FONTSIZE', (0, 0), (-1, -1), 10),
               ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
           ]))
           elements.append(table)
           elements.append(Spacer(1, 10))

       # Cursos actuales o próximos
       if status['current_courses']:
           elements.append(Paragraph("Asignaturas en curso:", subtitle_style))
           current_data = [["Código", "Asignatura", "Profesor", "Horario", "Periodo"]]
           
           for course in status['current_courses']:
               current_data.append([
                   clean_text_for_pdf(course.course_code),
                   Paragraph(clean_text_for_pdf(course.course_name), normal_style),
                   clean_text_for_pdf(course.teacher_name),
                   f"{clean_text_for_pdf(course.day)} {clean_text_for_pdf(course.schedule)}",
                   f"{course.start_date.strftime('%d/%m/%Y')} - {course.end_date.strftime('%d/%m/%Y')}"
               ])
           
           course_table = Table(current_data, colWidths=[60, 150, 100, 100, 100])
           course_table.setStyle(TableStyle([
               ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
               ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
               ('FONTSIZE', (0, 0), (-1, -1), 8),
               ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
               ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
               ('VALIGN', (0, 0), (-1, -1), 'TOP'),
               ('WORDWRAP', (0, 0), (-1, -1), True),
           ]))
           elements.append(course_table)
           elements.append(Spacer(1, 10))
       elif status['next_course']:
           next_course = status['next_course']
           elements.append(Paragraph("Próxima asignatura:", subtitle_style))
           elements.append(Spacer(1, 5))
           
           next_data = [
               ['Asignatura:', f"{clean_text_for_pdf(next_course.course_code)} - {clean_text_for_pdf(next_course.course_name)}"],
               ['Profesor:', clean_text_for_pdf(next_course.teacher_name)],
               ['Horario:', f"{clean_text_for_pdf(next_course.day)} {clean_text_for_pdf(next_course.schedule)}"],
               ['Inicio:', next_course.start_date.strftime('%d/%m/%Y')]
           ]
           
           next_table = Table(next_data, colWidths=[80, 400])
           next_table.setStyle(TableStyle([
               ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
               ('FONTSIZE', (0, 0), (-1, -1), 10),
               ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
               ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
           ]))
           elements.append(next_table)

       elements.append(Spacer(1, 20))

   # Pie de página
   elements.append(Paragraph(
       f"Reporte generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}",
       ParagraphStyle(
           'Footer',
           parent=styles['Normal'],
           fontSize=8,
           textColor=colors.grey,
           alignment=TA_CENTER
       )
   ))

   doc.build(elements)
   buffer.seek(0)
   return buffer

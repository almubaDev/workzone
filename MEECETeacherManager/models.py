from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField("Nombre Completo", max_length=200)
    rut = models.CharField("RUT", max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return f"{self.name} - {self.rut}"

# models.py
class TeacherCategory(models.Model):
    name = models.CharField("Nombre", max_length=100)
    description = models.TextField("Descripción", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Docente"
        verbose_name_plural = "Categorías de Docentes"
        ordering = ['name']

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):
    teacher = models.OneToOneField(
        'Teacher',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Docente"
    )
    category = models.ForeignKey(
        TeacherCategory,
        on_delete=models.PROTECT,
        verbose_name="Categoría",
        help_text="Adjunto/Regular/etc."
    )
    institutional_email = models.EmailField(
        "Correo Institucional",
        blank=True
    )
    personal_email = models.EmailField(
        "Correo Personal",
        blank=True
    )
    phone = models.CharField(
        "Celular",
        max_length=20,
        blank=True
    )
    profession = models.CharField(
        "Profesión",
        max_length=200,
        blank=True
    )
    academic_degree = models.CharField(
        "Grado Académico",
        max_length=200,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Docente"
        verbose_name_plural = "Perfiles de Docentes"

    def __str__(self):
        return f"Perfil de {self.teacher.name}"
    
    
#Carga Horaia

class Course(models.Model):
    code = models.CharField("Código Asignatura", max_length=10)
    name = models.CharField("Nombre Asignatura", max_length=200)

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        unique_together = ['code', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class TeacherSchedule(models.Model):
    MODALITY_CHOICES = [
        ('SYNC', 'Online Sincrónica'),
        ('ASYNC', 'Online Asincrónica'),
        ('PRES', 'Presencial'),
    ]

    DAY_CHOICES = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="Docente"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="Asignatura"
    )
    day = models.CharField(
        "Día",
        max_length=10,
        choices=DAY_CHOICES
    )
    start_time = models.TimeField("Hora Inicio")
    end_time = models.TimeField("Hora Término")
    start_date = models.DateField("Fecha de Inicio")
    end_date = models.DateField("Fecha de Término")
    modality = models.CharField(
        "Modalidad",
        max_length=5,
        choices=MODALITY_CHOICES,
        default='SYNC'
    )
    vacancies = models.PositiveIntegerField(
        "Cantidad de Vacantes", 
        default=0
    )
    intake = models.CharField("INTAKE", max_length=100, default="No especificado")
    is_accepted = models.BooleanField("¿El docente aceptó la carga horaria?", default=False)

    class Meta:
        verbose_name = "Carga Horaria"
        verbose_name_plural = "Cargas Horarias"
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.course.code} - {self.teacher.name} - {self.day}"

    @property
    def schedule_display(self):
        return f"{self.start_time.strftime('%H:%M')} a {self.end_time.strftime('%H:%M')}"
    
    
#Links
class GlobalTeacherLink(models.Model):
    name = models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción", blank=True)
    icon = models.CharField(
        "Ícono", 
        max_length=50, 
        default="fa-link",
        help_text="Clase de FontAwesome"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Link Global"
        verbose_name_plural = "Links Globales"
        ordering = ['name']

    def __str__(self):
        return self.name

class TeacherGlobalLinkURL(models.Model):
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        related_name='global_link_urls'
    )
    global_link = models.ForeignKey(
        GlobalTeacherLink,
        on_delete=models.CASCADE,
        related_name='teacher_urls'
    )
    url = models.URLField("URL", blank=True, null=True)
    is_active = models.BooleanField("Activo", default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "URL de Link Global"
        verbose_name_plural = "URLs de Links Globales"
        unique_together = ['teacher', 'global_link']

    def __str__(self):
        return f"{self.global_link.name} - {self.teacher.name}"
    
class TeacherPersonalLink(models.Model):
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        related_name='personal_links'
    )
    name = models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción", blank=True)
    url = models.URLField("URL")
    icon = models.CharField(
        "Ícono", 
        max_length=50, 
        default="fa-link",
        help_text="Clase de FontAwesome"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Link Personal"
        verbose_name_plural = "Links Personales"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.teacher.name}"
    

#Task flow
# models.py
class ComplianceTask(models.Model):
    name = models.CharField("Nombre de la Tarea", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarea de Cumplimiento"
        verbose_name_plural = "Tareas de Cumplimiento"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ComplianceStatus(models.Model):
    task = models.ForeignKey(ComplianceTask, on_delete=models.CASCADE, related_name='statuses')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='compliance_statuses')
    is_checked = models.BooleanField("Completado", default=False)
    is_active = models.BooleanField("Activo", default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estado de Cumplimiento"
        verbose_name_plural = "Estados de Cumplimiento"
        unique_together = ['task', 'teacher']

    def __str__(self):
        return f"{self.task.name} - {self.teacher.name}"
    
    
#MPA MANAGER
# models.py
from django.db import models

class MPA(models.Model):
    # Información básica del documento
    file_name = models.CharField("Nombre del archivo", max_length=255)
    uploaded_at = models.DateTimeField("Fecha de carga", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    # Información de la cabecera
    faculty = models.CharField("Facultad", max_length=200)
    school = models.CharField("Escuela", max_length=200)
    campus = models.CharField("Sede/Campus", max_length=200)
    period = models.CharField("Período", max_length=50)
    program_code = models.CharField("Código de Programa", max_length=50)
    program_name = models.CharField("Nombre de Programa", max_length=255)
    program_version = models.CharField("Versión", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "MPA"
        verbose_name_plural = "MPAs"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.program_code} - {self.program_name} ({self.period})"

class MPASheet(models.Model):
    mpa = models.ForeignKey(
        MPA, 
        on_delete=models.CASCADE,
        related_name='sheets',
        verbose_name="MPA"
    )
    sheet_name = models.CharField("Nombre de la hoja", max_length=100)
    intake = models.CharField("INTAKE", max_length=100)
    
    class Meta:
        verbose_name = "Hoja de MPA"
        verbose_name_plural = "Hojas de MPA"
        ordering = ['sheet_name']
        unique_together = ['mpa', 'sheet_name']

    def __str__(self):
        return f"{self.sheet_name} - {self.intake}"

class MPASchedule(models.Model):
    sheet = models.ForeignKey(
        MPASheet,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="Hoja"
    )
    # Campos de la tabla principal
    period = models.CharField("Período", max_length=50)
    nrc = models.CharField("NRC", max_length=20)
    course_code = models.CharField("Código Asignatura", max_length=20)
    section = models.CharField("Sección", max_length=10)
    course_name = models.CharField("Nombre Asignatura", max_length=255)
    activity = models.CharField("Actividad", max_length=50)
    modality = models.CharField("Modalidad", max_length=100)
    vacancies = models.IntegerField("Cantidad de Vacantes")
    day = models.CharField("Día", max_length=20)
    schedule = models.CharField("Horario (módulo)", max_length=50)
    duration = models.CharField("Duración (semanas)", max_length=20)
    start_date = models.DateField("Fecha de Inicio")
    end_date = models.DateField("Fecha de Término")
    teacher_rut = models.CharField("RUT", max_length=20)
    teacher_name = models.CharField("Nombre Profesor", max_length=200)
    building = models.CharField("Edificio", max_length=100)
    classroom = models.CharField("Sala", max_length=100)
    hourly_rate = models.DecimalField("Valor Hora", max_digits=10, decimal_places=2, null=True, blank=True)
    catalog_hours = models.IntegerField("Horas Catálogo", null=True, blank=True)
    responsibility_percentage = models.DecimalField("% Responsabilidad", max_digits=5, decimal_places=2, null=True, blank=True)
    payable_hours = models.IntegerField("Horas a Pagar", null=True, blank=True)
    installments = models.IntegerField("Cantidad de Cuotas", null=True, blank=True)
    installment_value = models.DecimalField("Valor Cuota", max_digits=10, decimal_places=2, null=True, blank=True)
    total_payment = models.DecimalField("Total a Pagar", max_digits=10, decimal_places=2, null=True, blank=True)
    folio = models.CharField("FOLIO", max_length=50, blank=True, null=True)
    budget = models.CharField("PPTO", max_length=50, blank=True, null=True)
    minimum = models.CharField("Mínimo", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Horario de MPA"
        verbose_name_plural = "Horarios de MPA"
        ordering = ['period', 'course_code', 'section']

    def __str__(self):
        return f"{self.course_code} - {self.teacher_name}"
    
    
    
# Este es el modelo TimelineEvent corregido que debes incluir en MEECETeacherManager/models.py

class TimelineEvent(models.Model):
    EVENT_TYPES = [
        ('GENERAL', 'Evento General'),
        ('COURSE_START', 'Inicio de Curso'),
        ('COURSE_END', 'Término de Curso'),
        ('MILESTONE', 'Hito'),
        ('ALERT', 'Alerta'),
    ]

    ICON_CHOICES = [
        ('fa-star', 'Estrella'),
        ('fa-flag', 'Bandera'),
        ('fa-exclamation-circle', 'Alerta'),
        ('fa-check-circle', 'Check'),
        ('fa-info-circle', 'Info'),
        ('fa-calendar', 'Calendario'),
        ('fa-clock', 'Reloj')
    ]

    title = models.CharField("Título", max_length=200)
    event_type = models.CharField("Tipo", max_length=20, choices=EVENT_TYPES, default='GENERAL')
    event_date = models.DateTimeField("Fecha del Evento")
    color = models.CharField("Color", max_length=7, default="#3498db")
    icon = models.CharField("Ícono", max_length=50, choices=ICON_CHOICES, blank=True)
    mpa = models.ForeignKey(MPA, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_visible = models.BooleanField("Visible", default=True)  # Añadido para controlar la visibilidad
    created_at = models.DateTimeField(auto_now_add=True)  # Añadido para seguimiento de creación
    updated_at = models.DateTimeField(auto_now=True)  # Añadido para seguimiento de actualizaciones

    def __str__(self):
        return f"{self.title} ({self.event_date.strftime('%d/%m/%Y')})"
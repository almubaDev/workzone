# services.py
from django.db.models import Min, Max
from datetime import datetime, timedelta
from .models import MPA, MPASheet, MPASchedule, TimelineEvent

class TimelineService:
    @staticmethod
    def get_intake_timeline_data(mpa_id):
        """
        Obtiene los datos temporales organizados por INTAKE para un MPA específico
        """
        mpa = MPA.objects.get(id=mpa_id)
        timeline_data = []

        for sheet in mpa.sheets.all():
            # Calcular fechas del INTAKE
            schedules = sheet.schedules.all()
            intake_dates = schedules.aggregate(
                start_date=Min('start_date'),
                end_date=Max('end_date')
            )

            # Organizar cursos
            courses = []
            for schedule in schedules:
                courses.append({
                    'id': schedule.id,
                    'course_code': schedule.course_code,
                    'course_name': schedule.course_name,
                    'teacher_name': schedule.teacher_name,
                    'start_date': schedule.start_date,
                    'end_date': schedule.end_date,
                    'schedule': schedule.schedule,
                    'day': schedule.day,
                    'duration': schedule.duration
                })

            # Obtener eventos relacionados
            events = TimelineEvent.objects.filter(
                mpa=mpa,
                event_date__range=(
                    intake_dates['start_date'],
                    intake_dates['end_date']
                ),
                is_visible=True
            )

            timeline_data.append({
                'intake': sheet.intake,
                'start_date': intake_dates['start_date'],
                'end_date': intake_dates['end_date'],
                'courses': sorted(courses, key=lambda x: x['start_date']),
                'events': list(events.values())
            })

        return timeline_data

    @staticmethod
    def get_upcoming_events(days=7):
        """
        Obtiene los eventos próximos para el sidebar
        """
        today = datetime.now().date()
        end_date = today + timedelta(days=days)

        return TimelineEvent.objects.filter(
            event_date__range=(today, end_date),
            is_visible=True
        ).order_by('event_date')

    @staticmethod
    def add_event(data, user):
        """
        Agrega un nuevo evento al timeline
        """
        event = TimelineEvent(
            title=data['title'],
            description=data.get('description', ''),
            event_type=data['event_type'],
            event_date=data['event_date'],
            created_by=user
        )

        if 'mpa_id' in data:
            event.mpa_id = data['mpa_id']
        if 'mpa_schedule_id' in data:
            event.mpa_schedule_id = data['mpa_schedule_id']
        if 'color' in data:
            event.color = data['color']
        if 'icon' in data:
            event.icon = data['icon']
        if 'highlight' in data:
            event.highlight = data['highlight']

        event.save()
        return event
# Migración para actualizar el modelo TimelineEvent
# Archivo a crear: MEECETeacherManager/migrations/0021_update_timelineevent.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEECETeacherManager', '0020_alter_timelineevent_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineevent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='timelineevent',
            name='icon',
            field=models.CharField(blank=True, choices=[('fa-star', 'Estrella'), ('fa-flag', 'Bandera'), ('fa-exclamation-circle', 'Alerta'), ('fa-check-circle', 'Check'), ('fa-info-circle', 'Info'), ('fa-calendar', 'Calendario'), ('fa-clock', 'Reloj')], max_length=50, verbose_name='Ícono'),
        ),
    ]
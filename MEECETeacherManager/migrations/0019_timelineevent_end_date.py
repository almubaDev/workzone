# Generated by Django 5.1.4 on 2025-02-08 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEECETeacherManager', '0018_timelineevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineevent',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Término'),
        ),
    ]

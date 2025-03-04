# Generated by Django 5.1.4 on 2025-02-03 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEECETeacherManager', '0015_teacherschedule_modality_teacherschedule_vacancies'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherschedule',
            name='intake',
            field=models.CharField(default='No especificado', max_length=100, verbose_name='INTAKE'),
        ),
        migrations.AlterField(
            model_name='teacherschedule',
            name='modality',
            field=models.CharField(choices=[('SYNC', 'Online Sincrónica'), ('ASYNC', 'Online Asincrónica'), ('PRES', 'Presencial')], default='SYNC', max_length=5, verbose_name='Modalidad'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-02-01 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEECETeacherManager', '0003_course_teacherschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalTeacherLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('base_url', models.URLField(verbose_name='URL Base')),
                ('url_pattern', models.CharField(help_text='Use {rut} para insertar el RUT del docente. Ejemplo: /folder/{rut}', max_length=255, verbose_name='Patrón URL')),
                ('icon', models.CharField(default='fa-link', help_text='Clase de FontAwesome', max_length=50, verbose_name='Ícono')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Link Global',
                'verbose_name_plural': 'Links Globales',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TeacherPersonalLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('url', models.URLField(verbose_name='URL')),
                ('icon', models.CharField(default='fa-link', help_text='Clase de FontAwesome', max_length=50, verbose_name='Ícono')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_links', to='MEECETeacherManager.teacher')),
            ],
            options={
                'verbose_name': 'Link Personal',
                'verbose_name_plural': 'Links Personales',
                'ordering': ['name'],
            },
        ),
    ]

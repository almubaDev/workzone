# Generated by Django 5.1.4 on 2025-03-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEECETeacherManager', '0021_update_timelineevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineevent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='timelineevent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

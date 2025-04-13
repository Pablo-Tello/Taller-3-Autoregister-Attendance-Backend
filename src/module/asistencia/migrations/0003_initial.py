# Generated by Django 5.2 on 2025-04-13 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asistencia', '0002_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='str_idDocente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='usuarios.docente'),
        ),
        migrations.AddConstraint(
            model_name='asistencia',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('int_idAlumnoSeccion__isnull', False), ('str_tipo', 'A')), models.Q(('str_idDocente__isnull', False), ('str_tipo', 'D')), _connector='OR'), name='check_tipo_asistencia'),
        ),
    ]

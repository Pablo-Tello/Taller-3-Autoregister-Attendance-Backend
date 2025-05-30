# Generated by Django 5.2 on 2025-04-13 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academico', '0001_initial'),
        ('inscripciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='int_idDocenteSeccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='inscripciones.docenteseccion'),
        ),
        migrations.AddField(
            model_name='seccion',
            name='str_idCicloAcademico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.cicloacademico'),
        ),
        migrations.AddField(
            model_name='seccion',
            name='str_idCurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secciones', to='academico.curso'),
        ),
        migrations.AddField(
            model_name='sesionclase',
            name='int_idCalendario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sesiones', to='academico.calendario'),
        ),
        migrations.AddField(
            model_name='sesionclase',
            name='int_idHorario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sesiones', to='academico.horario'),
        ),
        migrations.AddField(
            model_name='sesionclase',
            name='str_idCicloAcademico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.cicloacademico'),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='str_idCicloAcademico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.cicloacademico'),
        ),
        migrations.AddField(
            model_name='syllabus',
            name='str_idCurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus', to='academico.curso'),
        ),
        migrations.AlterUniqueTogether(
            name='calendario',
            unique_together={('str_idCicloAcademico', 'dt_fecha')},
        ),
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together={('int_idDocenteSeccion', 'str_dia_semana', 'dt_hora_inicio')},
        ),
        migrations.AlterUniqueTogether(
            name='seccion',
            unique_together={('str_idCurso', 'str_idCicloAcademico', 'str_numero')},
        ),
        migrations.AlterUniqueTogether(
            name='sesionclase',
            unique_together={('int_idHorario', 'dt_fecha')},
        ),
        migrations.AlterUniqueTogether(
            name='syllabus',
            unique_together={('str_idCurso', 'str_idCicloAcademico', 'str_version')},
        ),
    ]

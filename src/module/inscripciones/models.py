from django.db import models
from src.module.academico.models import Seccion
from src.module.usuarios.models import Alumno, Docente

class AlumnoSeccion(models.Model):
    int_idAlumnoSeccion = models.AutoField(primary_key=True)
    str_idAlumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones', to_field='str_idAlumno')
    int_idSeccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='alumnos', to_field='int_idSeccion')
    str_idCicloAcademico = models.ForeignKey('academico.CicloAcademico', on_delete=models.CASCADE, to_field='str_idCicloAcademico')
    dt_fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Inscripcion {self.int_idAlumnoSeccion} - {self.str_idAlumno} - {self.int_idSeccion}"

    class Meta:
        db_table = 'alumno_seccion'
        verbose_name = 'Inscripción de Alumno'
        verbose_name_plural = 'Inscripciones de Alumnos'
        unique_together = ('str_idAlumno', 'int_idSeccion', 'str_idCicloAcademico')

class DocenteSeccion(models.Model):
    TIPOS_DOCENTE = [
        ('P', 'Principal'),
        ('A', 'Auxiliar'),
        ('J', 'Jefe de Práctica'),
    ]

    int_idDocenteSeccion = models.AutoField(primary_key=True)
    str_idDocente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='asignaciones', to_field='str_idDocente')
    int_idSeccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='docentes', to_field='int_idSeccion')
    str_idCicloAcademico = models.ForeignKey('academico.CicloAcademico', on_delete=models.CASCADE, to_field='str_idCicloAcademico')
    str_tipo = models.CharField(max_length=1, choices=TIPOS_DOCENTE, default='P')
    dt_fecha_asignacion = models.DateTimeField(auto_now_add=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Asignacion {self.int_idDocenteSeccion} - {self.str_idDocente} - {self.int_idSeccion} ({self.get_str_tipo_display()})"

    class Meta:
        db_table = 'docente_seccion'
        verbose_name = 'Asignación de Docente'
        verbose_name_plural = 'Asignaciones de Docentes'
        unique_together = ('str_idDocente', 'int_idSeccion', 'str_tipo', 'str_idCicloAcademico')

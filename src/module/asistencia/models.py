from django.db import models
from src.module.academico.models import SesionClase
from src.module.inscripciones.models import AlumnoSeccion
from src.module.usuarios.models import Docente

class Asistencia(models.Model):
    TIPOS = [
        ('A', 'Alumno'),
        ('D', 'Docente'),
    ]

    ESTADOS = [
        ('P', 'Presente'),
        ('T', 'Tardanza'),
        ('F', 'Falta'),
        ('J', 'Justificada'),
    ]

    int_idAsistencia = models.AutoField(primary_key=True)
    int_idSesionClase = models.ForeignKey(SesionClase, on_delete=models.CASCADE, related_name='asistencias', to_field='int_idSesionClase')
    str_tipo = models.CharField(max_length=1, choices=TIPOS, default='A')
    int_idAlumnoSeccion = models.ForeignKey(AlumnoSeccion, on_delete=models.CASCADE, related_name='asistencias', to_field='int_idAlumnoSeccion', null=True, blank=True)
    str_idDocente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='asistencias', to_field='str_idDocente', null=True, blank=True)
    dt_fecha = models.DateField()
    str_estado = models.CharField(max_length=1, choices=ESTADOS, default='F')
    str_observacion = models.TextField(blank=True, null=True)
    dt_hora_registro = models.TimeField(auto_now_add=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        if self.str_tipo == 'A':
            return f"Asistencia Alumno {self.int_idAsistencia} - {self.int_idAlumnoSeccion} - {self.dt_fecha} - {self.get_str_estado_display()}"
        else:
            return f"Asistencia Docente {self.int_idAsistencia} - {self.str_idDocente} - {self.dt_fecha} - {self.get_str_estado_display()}"

    class Meta:
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        constraints = [
            models.CheckConstraint(
                check=models.Q(str_tipo='A', int_idAlumnoSeccion__isnull=False) | models.Q(str_tipo='D', str_idDocente__isnull=False),
                name='check_tipo_asistencia'
            )
        ]

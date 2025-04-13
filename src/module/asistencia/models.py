from django.db import models
from src.module.academico.models import SesionClase
from src.module.inscripciones.models import AlumnoSeccion

class Asistencia(models.Model):
    ESTADOS = [
        ('P', 'Presente'),
        ('T', 'Tardanza'),
        ('F', 'Falta'),
        ('J', 'Justificada'),
    ]

    int_idAsistencia = models.AutoField(primary_key=True)
    int_idAlumnoSeccion = models.ForeignKey(AlumnoSeccion, on_delete=models.CASCADE, related_name='asistencias', to_field='int_idAlumnoSeccion')
    int_idSesionClase = models.ForeignKey(SesionClase, on_delete=models.CASCADE, related_name='asistencias', to_field='int_idSesionClase')
    dt_fecha = models.DateField()
    str_estado = models.CharField(max_length=1, choices=ESTADOS, default='F')
    str_observacion = models.TextField(blank=True, null=True)
    dt_hora_registro = models.TimeField(auto_now_add=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Asistencia {self.int_idAsistencia} - {self.dt_fecha} - {self.get_str_estado_display()}"

    class Meta:
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ('int_idAlumnoSeccion', 'int_idSesionClase', 'dt_fecha')

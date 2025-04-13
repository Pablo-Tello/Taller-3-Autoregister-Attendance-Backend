from django.db import models

class CicloAcademico(models.Model):
    str_idCicloAcademico = models.CharField(primary_key=True, max_length=20)  # Ejemplo: "2024-1", "2024-2"
    str_nombre = models.CharField(max_length=100)
    dt_fecha_inicio = models.DateField()
    dt_fecha_fin = models.DateField()
    int_duracion_semanas = models.PositiveSmallIntegerField()
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.str_idCicloAcademico

    class Meta:
        db_table = 'ciclo_academico'
        verbose_name = 'Ciclo Académico'
        verbose_name_plural = 'Ciclos Académicos'

class Calendario(models.Model):
    TIPO_DIA = [
        ('L', 'Laboral'),
        ('F', 'Feriado'),
        ('V', 'Vacaciones'),
        ('S', 'Fin de Semana'),
    ]

    int_idCalendario = models.AutoField(primary_key=True)
    dt_fecha = models.DateField()
    str_tipo_dia = models.CharField(max_length=1, choices=TIPO_DIA, default='L')
    str_descripcion = models.CharField(max_length=200, blank=True, null=True)
    bool_laborable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dt_fecha} - {self.get_str_tipo_dia_display()}"

    class Meta:
        db_table = 'calendario'
        verbose_name = 'Calendario'
        verbose_name_plural = 'Calendarios'
        constraints = [
            models.UniqueConstraint(fields=['dt_fecha'], name='unique_fecha_calendario')
        ]

class Curso(models.Model):
    str_idCurso = models.CharField(primary_key=True, max_length=20)  # Ejemplo: "CS1100", "MA2001"
    str_nombre = models.CharField(max_length=200)
    int_creditos = models.PositiveSmallIntegerField()
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.str_idCurso} - {self.str_nombre}"

    class Meta:
        db_table = 'curso'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Syllabus(models.Model):
    int_idSyllabus = models.AutoField(primary_key=True)
    str_idCurso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='syllabus', to_field='str_idCurso')
    str_idCicloAcademico = models.ForeignKey(CicloAcademico, on_delete=models.CASCADE, to_field='str_idCicloAcademico')
    str_version = models.CharField(max_length=20)
    str_contenido = models.TextField()
    dt_fecha_creacion = models.DateField(auto_now_add=True)
    dt_fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"Syllabus {self.str_idCurso} - {self.str_version}"

    class Meta:
        db_table = 'syllabus'
        verbose_name = 'Syllabus'
        verbose_name_plural = 'Syllabus'
        unique_together = ('str_idCurso', 'str_idCicloAcademico', 'str_version')

class Seccion(models.Model):
    int_idSeccion = models.AutoField(primary_key=True)
    str_idCurso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='secciones', to_field='str_idCurso')
    str_idCicloAcademico = models.ForeignKey(CicloAcademico, on_delete=models.CASCADE, to_field='str_idCicloAcademico')
    str_numero = models.CharField(max_length=10)  # Ejemplo: "A", "B", "C"
    int_capacidad_maxima = models.PositiveSmallIntegerField()
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.str_idCurso} - Sección {self.str_numero}"

    class Meta:
        db_table = 'seccion'
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
        unique_together = ('str_idCurso', 'str_idCicloAcademico', 'str_numero')

class Horario(models.Model):
    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    int_idHorario = models.AutoField(primary_key=True)
    int_idDocenteSeccion = models.ForeignKey('inscripciones.DocenteSeccion', on_delete=models.CASCADE, related_name='horarios', to_field='int_idDocenteSeccion')
    str_dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    dt_hora_inicio = models.TimeField()
    dt_hora_fin = models.TimeField()
    str_aula = models.CharField(max_length=50, blank=True, null=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Horario {self.int_idHorario} - {self.get_str_dia_semana_display()} {self.dt_hora_inicio}-{self.dt_hora_fin}"

    class Meta:
        db_table = 'horario'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ('int_idDocenteSeccion', 'str_dia_semana', 'dt_hora_inicio')

class SesionClase(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('R', 'Realizada'),
        ('C', 'Cancelada'),
    ]

    int_idSesionClase = models.AutoField(primary_key=True)
    int_idHorario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='sesiones', to_field='int_idHorario')
    str_idCicloAcademico = models.ForeignKey(CicloAcademico, on_delete=models.CASCADE, to_field='str_idCicloAcademico')
    int_idCalendario = models.ForeignKey(Calendario, on_delete=models.CASCADE, related_name='sesiones', to_field='int_idCalendario')
    dt_fecha = models.DateField()
    str_estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    str_tema = models.CharField(max_length=200, blank=True, null=True)
    str_observacion = models.TextField(blank=True, null=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Sesion {self.int_idSesionClase} - {self.dt_fecha} - {self.get_str_estado_display()}"

    class Meta:
        db_table = 'sesion_clase'
        verbose_name = 'Sesión de Clase'
        verbose_name_plural = 'Sesiones de Clase'
        unique_together = ('int_idHorario', 'dt_fecha')

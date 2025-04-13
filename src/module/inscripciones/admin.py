from django.contrib import admin
from .models import AlumnoSeccion, DocenteSeccion

@admin.register(AlumnoSeccion)
class AlumnoSeccionAdmin(admin.ModelAdmin):
    list_display = ('int_idAlumnoSeccion', 'str_idAlumno', 'int_idSeccion', 'str_idCicloAcademico', 'dt_fecha_inscripcion', 'bool_activo')
    search_fields = ('str_idAlumno__str_nombres', 'str_idAlumno__str_apellidos', 'int_idSeccion__str_codigo')
    list_filter = ('bool_activo', 'str_idCicloAcademico', 'dt_fecha_inscripcion')
    date_hierarchy = 'dt_fecha_inscripcion'

@admin.register(DocenteSeccion)
class DocenteSeccionAdmin(admin.ModelAdmin):
    list_display = ('int_idDocenteSeccion', 'str_idDocente', 'int_idSeccion', 'str_idCicloAcademico', 'str_tipo', 'dt_fecha_asignacion', 'bool_activo')
    search_fields = ('str_idDocente__str_nombres', 'str_idDocente__str_apellidos', 'int_idSeccion__str_codigo')
    list_filter = ('bool_activo', 'str_idCicloAcademico', 'str_tipo', 'dt_fecha_asignacion')
    date_hierarchy = 'dt_fecha_asignacion'

from django.contrib import admin
from .models import CicloAcademico, Calendario, Curso, Syllabus, Seccion, SesionClase, Horario

@admin.register(CicloAcademico)
class CicloAcademicoAdmin(admin.ModelAdmin):
    list_display = ('str_idCicloAcademico', 'str_nombre', 'dt_fecha_inicio', 'dt_fecha_fin', 'bool_activo')
    search_fields = ('str_idCicloAcademico', 'str_nombre')
    list_filter = ('bool_activo',)

@admin.register(Calendario)
class CalendarioAdmin(admin.ModelAdmin):
    list_display = ('int_idCalendario', 'dt_fecha', 'str_tipo_dia', 'bool_laborable')
    search_fields = ('dt_fecha', 'str_descripcion')
    list_filter = ('bool_laborable', 'str_tipo_dia')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('str_idCurso', 'str_nombre', 'int_creditos', 'bool_activo')
    search_fields = ('str_idCurso', 'str_nombre')
    list_filter = ('bool_activo',)

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('int_idSyllabus', 'str_idCurso', 'str_idCicloAcademico', 'str_version', 'dt_fecha_creacion')
    search_fields = ('str_idCurso__str_nombre', 'str_idCicloAcademico__str_nombre')
    list_filter = ('str_idCicloAcademico',)

@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ('int_idSeccion', 'str_idCurso', 'str_numero', 'int_capacidad_maxima', 'bool_activo')
    search_fields = ('str_numero', 'str_idCurso__str_nombre')
    list_filter = ('bool_activo', 'str_idCurso')

@admin.register(SesionClase)
class SesionClaseAdmin(admin.ModelAdmin):
    list_display = ('int_idSesionClase', 'int_idHorario', 'dt_fecha', 'str_tema', 'str_estado', 'bool_activo')
    search_fields = ('str_tema', 'int_idHorario__int_idDocenteSeccion__int_idSeccion__str_numero')
    list_filter = ('bool_activo', 'dt_fecha', 'str_estado')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('int_idHorario', 'int_idDocenteSeccion', 'str_dia_semana', 'dt_hora_inicio', 'dt_hora_fin', 'str_aula', 'bool_activo')
    search_fields = ('str_aula',)
    list_filter = ('bool_activo', 'str_dia_semana')

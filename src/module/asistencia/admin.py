from django.contrib import admin
from .models import Asistencia, CodigoQR

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('int_idAsistencia', 'int_idSesionClase', 'str_tipo', 'dt_fecha', 'str_estado', 'dt_hora_registro', 'bool_activo')
    search_fields = ('int_idAlumnoSeccion__str_idAlumno__str_nombres', 'int_idAlumnoSeccion__str_idAlumno__str_apellidos', 'str_idDocente__str_nombres', 'str_idDocente__str_apellidos')
    list_filter = ('bool_activo', 'str_tipo', 'str_estado', 'dt_fecha')
    date_hierarchy = 'dt_fecha'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


@admin.register(CodigoQR)
class CodigoQRAdmin(admin.ModelAdmin):
    list_display = ('int_idCodigoQR', 'int_idSesionClase', 'str_idDocente', 'str_codigo', 'dt_fecha_creacion', 'dt_fecha_expiracion', 'bool_activo')
    search_fields = ('str_codigo', 'str_idDocente__str_nombres', 'str_idDocente__str_apellidos')
    list_filter = ('bool_activo', 'dt_fecha_creacion')
    date_hierarchy = 'dt_fecha_creacion'

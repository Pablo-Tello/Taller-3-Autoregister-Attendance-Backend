from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Docente, Alumno

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('str_email', 'int_idUser', 'is_staff', 'is_superuser', 'bool_activo')
    search_fields = ('str_email', 'str_username')
    list_filter = ('is_staff', 'is_superuser', 'bool_activo')
    ordering = ('str_email',)
    
    fieldsets = (
        (None, {'fields': ('str_email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'str_username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Estado'), {'fields': ('bool_activo',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('str_email', 'password1', 'password2'),
        }),
    )

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('str_idDocente', 'str_nombres', 'str_apellidos', 'str_especialidad', 'bool_activo')
    search_fields = ('str_idDocente', 'str_nombres', 'str_apellidos', 'int_idUser__str_email')
    list_filter = ('bool_activo', 'str_especialidad')

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('str_idAlumno', 'str_nombres', 'str_apellidos', 'dt_fecha_nacimiento', 'bool_activo')
    search_fields = ('str_idAlumno', 'str_nombres', 'str_apellidos', 'int_idUser__str_email')
    list_filter = ('bool_activo',)

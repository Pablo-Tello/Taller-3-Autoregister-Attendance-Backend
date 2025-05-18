from rest_framework import serializers
from .models import AlumnoSeccion, DocenteSeccion
from src.module.usuarios.serializers import AlumnoSerializer, DocenteSerializer
from src.module.academico.serializers import SeccionSerializer
from src.module.academico.models import Curso, Horario, Seccion

class AlumnoSeccionSerializer(serializers.ModelSerializer):
    # Add nested serialization for str_idAlumno to include student name and surname
    str_idAlumno = serializers.SerializerMethodField()

    class Meta:
        model = AlumnoSeccion
        fields = '__all__'

    def get_str_idAlumno(self, obj):
        # Return a dictionary with the student ID, name and surname
        if obj.str_idAlumno:
            return {
                'str_idAlumno': obj.str_idAlumno.str_idAlumno,
                'str_nombres': obj.str_idAlumno.str_nombres,
                'str_apellidos': obj.str_idAlumno.str_apellidos
            }
        return obj.str_idAlumno

class AlumnoSeccionDetalleSerializer(serializers.ModelSerializer):
    str_idAlumno = AlumnoSerializer(read_only=True)
    int_idSeccion = SeccionSerializer(read_only=True)

    class Meta:
        model = AlumnoSeccion
        fields = '__all__'

class DocenteSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocenteSeccion
        fields = '__all__'

class DocenteSeccionDetalleSerializer(serializers.ModelSerializer):
    str_idDocente = DocenteSerializer(read_only=True)
    int_idSeccion = SeccionSerializer(read_only=True)

    class Meta:
        model = DocenteSeccion
        fields = '__all__'

class DocenteCursoSerializer(serializers.ModelSerializer):
    # Información básica de la sección
    int_idSeccion = serializers.IntegerField(source='int_idSeccion.int_idSeccion')
    str_numero = serializers.CharField(source='int_idSeccion.str_numero')

    # Información del curso
    str_idCurso = serializers.CharField(source='int_idSeccion.str_idCurso.str_idCurso')
    str_nombreCurso = serializers.CharField(source='int_idSeccion.str_idCurso.str_nombre')
    int_creditos = serializers.IntegerField(source='int_idSeccion.str_idCurso.int_creditos')

    # Información del ciclo académico
    str_idCicloAcademico = serializers.CharField(source='str_idCicloAcademico.str_idCicloAcademico')
    str_nombreCiclo = serializers.CharField(source='str_idCicloAcademico.str_nombre')

    # Información del horario (puede ser múltiple, tomamos el primero como ejemplo)
    str_horario = serializers.SerializerMethodField()
    str_aula = serializers.SerializerMethodField()

    class Meta:
        model = DocenteSeccion
        fields = [
            'int_idDocenteSeccion', 'str_idDocente', 'int_idSeccion',
            'str_numero', 'str_idCurso', 'str_nombreCurso', 'int_creditos',
            'str_idCicloAcademico', 'str_nombreCiclo', 'str_horario', 'str_aula',
            'str_tipo', 'bool_activo'
        ]

    def get_str_horario(self, obj):
        # Obtener el primer horario asociado a esta asignación docente-sección
        horario = Horario.objects.filter(int_idDocenteSeccion=obj.int_idDocenteSeccion, bool_activo=True).first()
        if horario:
            dia = dict(Horario.DIAS_SEMANA).get(horario.str_dia_semana, '')
            return f"{dia} {horario.dt_hora_inicio.strftime('%H:%M')} - {horario.dt_hora_fin.strftime('%H:%M')}"
        return "No disponible"

    def get_str_aula(self, obj):
        # Obtener el primer horario asociado a esta asignación docente-sección
        horario = Horario.objects.filter(int_idDocenteSeccion=obj.int_idDocenteSeccion, bool_activo=True).first()
        if horario and horario.str_aula:
            return horario.str_aula
        return "No disponible"


class AlumnoCursoSerializer(serializers.ModelSerializer):
    # Información básica de la sección
    int_idSeccion = serializers.IntegerField(source='int_idSeccion.int_idSeccion')
    str_numero = serializers.CharField(source='int_idSeccion.str_numero')

    # Información del curso
    str_idCurso = serializers.CharField(source='int_idSeccion.str_idCurso.str_idCurso')
    str_nombreCurso = serializers.CharField(source='int_idSeccion.str_idCurso.str_nombre')
    int_creditos = serializers.IntegerField(source='int_idSeccion.str_idCurso.int_creditos')

    # Información del ciclo académico
    str_idCicloAcademico = serializers.CharField(source='str_idCicloAcademico.str_idCicloAcademico')
    str_nombreCiclo = serializers.CharField(source='str_idCicloAcademico.str_nombre')

    class Meta:
        model = AlumnoSeccion
        fields = [
            'int_idAlumnoSeccion', 'str_idAlumno', 'int_idSeccion',
            'str_numero', 'str_idCurso', 'str_nombreCurso', 'int_creditos',
            'str_idCicloAcademico', 'str_nombreCiclo', 'bool_activo'
        ]

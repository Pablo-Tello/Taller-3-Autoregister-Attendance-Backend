from rest_framework import serializers
from .models import CicloAcademico, Calendario, Curso, Syllabus, Seccion, SesionClase, Horario

class CicloAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloAcademico
        fields = '__all__'

class CalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class SesionClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionClase
        fields = '__all__'

class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = '__all__'

class SeccionDetalleSerializer(serializers.ModelSerializer):
    sesiones = SesionClaseSerializer(many=True, read_only=True)
    curso = CursoSerializer(read_only=True)
    ciclo_academico = CicloAcademicoSerializer(read_only=True)

    class Meta:
        model = Seccion
        fields = '__all__'

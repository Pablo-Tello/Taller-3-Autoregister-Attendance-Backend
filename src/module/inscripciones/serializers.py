from rest_framework import serializers
from .models import AlumnoSeccion, DocenteSeccion
from src.module.usuarios.serializers import AlumnoSerializer, DocenteSerializer
from src.module.academico.serializers import SeccionSerializer

class AlumnoSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoSeccion
        fields = '__all__'

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

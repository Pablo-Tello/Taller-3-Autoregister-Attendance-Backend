from rest_framework import serializers
from .models import Asistencia, CodigoQR
from src.module.inscripciones.serializers import AlumnoSeccionSerializer
from src.module.academico.serializers import SesionClaseSerializer
from src.module.usuarios.serializers import DocenteSerializer

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

class AsistenciaDetalleSerializer(serializers.ModelSerializer):
    int_idAlumnoSeccion = AlumnoSeccionSerializer(read_only=True)
    int_idSesionClase = SesionClaseSerializer(read_only=True)

    class Meta:
        model = Asistencia
        fields = '__all__'


class CodigoQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoQR
        fields = '__all__'


class CodigoQRCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoQR
        fields = ['int_idSesionClase', 'str_idDocente', 'str_codigo', 'dt_fecha_expiracion']


class CodigoQRDetalleSerializer(serializers.ModelSerializer):
    int_idSesionClase = SesionClaseSerializer(read_only=True)
    str_idDocente = DocenteSerializer(read_only=True)

    class Meta:
        model = CodigoQR
        fields = '__all__'


class VerificarCodigoQRSerializer(serializers.Serializer):
    str_codigo = serializers.CharField(max_length=255)
    str_idAlumno = serializers.CharField(max_length=20)


class VerificarCodigoQRJWTSerializer(serializers.Serializer):
    token = serializers.CharField()
    str_idAlumno = serializers.CharField(max_length=20)

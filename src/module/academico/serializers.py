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
    int_idCalendario = serializers.PrimaryKeyRelatedField(
        queryset=Calendario.objects.all(),
        required=False  # Hacemos que int_idCalendario no sea requerido
    )

    class Meta:
        model = SesionClase
        fields = '__all__'

    def _get_calendario_by_fecha(self, fecha):
        """Método auxiliar para obtener el calendario por fecha"""
        try:
            return Calendario.objects.get(dt_fecha=fecha)
        except Calendario.DoesNotExist:
            raise serializers.ValidationError({
                'dt_fecha': f"No se encontró un registro en el calendario para la fecha {fecha}"
            })

    def validate(self, data):
        """Validación personalizada para asignar automáticamente int_idCalendario"""
        # Verificar que dt_fecha esté presente
        if 'dt_fecha' not in data:
            raise serializers.ValidationError({
                'dt_fecha': "El campo dt_fecha es obligatorio para crear una sesión de clase"
            })

        # Buscar el calendario por fecha
        calendario = self._get_calendario_by_fecha(data['dt_fecha'])

        # Asignar el calendario encontrado
        data['int_idCalendario'] = calendario

        return data

    def create(self, validated_data):
        # El calendario ya ha sido asignado en validate()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # El calendario ya ha sido asignado en validate() si se actualizó dt_fecha
        return super().update(instance, validated_data)

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

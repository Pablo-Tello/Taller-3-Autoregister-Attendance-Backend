from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import Docente, Alumno

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    str_email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data['str_email'], password=data['password'])
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Credenciales incorrectas o usuario inactivo")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['int_idUser', 'str_email', 'first_name', 'last_name', 'is_active', 'bool_activo']
        read_only_fields = ['int_idUser']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['int_idUser', 'str_email', 'password', 'first_name', 'last_name', 'bool_activo']
        read_only_fields = ['int_idUser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Establecer username igual al email para evitar valores vacíos
        validated_data['username'] = validated_data['str_email']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class DocenteSerializer(serializers.ModelSerializer):
    str_email = serializers.EmailField(source='int_idUser.str_email', read_only=True)

    class Meta:
        model = Docente
        fields = ['str_idDocente', 'str_nombres', 'str_apellidos', 'str_especialidad', 'bool_activo', 'str_email']
        read_only_fields = ['str_idDocente']

class DocenteCreateSerializer(serializers.ModelSerializer):
    str_email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Docente
        fields = ['str_idDocente', 'str_nombres', 'str_apellidos', 'str_especialidad', 'bool_activo', 'str_email', 'password']
        read_only_fields = ['str_idDocente']

    def create(self, validated_data):
        str_email = validated_data.pop('str_email')
        password = validated_data.pop('password')

        user = User(str_email=str_email, username=str_email)
        user.set_password(password)
        user.save()

        # Generar ID de docente automáticamente (D001, D002, etc.)
        last_docente = Docente.objects.order_by('-str_idDocente').first()
        if last_docente:
            # Extraer el número del último ID y aumentarlo en 1
            last_id = last_docente.str_idDocente
            if last_id.startswith('D'):
                try:
                    num = int(last_id[1:]) + 1
                    new_id = f'D{num:03d}'
                except ValueError:
                    new_id = 'D001'
            else:
                new_id = 'D001'
        else:
            new_id = 'D001'

        docente = Docente.objects.create(str_idDocente=new_id, int_idUser=user, **validated_data)
        return docente

class AlumnoSerializer(serializers.ModelSerializer):
    str_email = serializers.EmailField(source='int_idUser.str_email', read_only=True)

    class Meta:
        model = Alumno
        fields = ['str_idAlumno', 'str_nombres', 'str_apellidos', 'dt_fecha_nacimiento', 'bool_activo', 'str_email']
        read_only_fields = ['str_idAlumno']

class AlumnoCreateSerializer(serializers.ModelSerializer):
    str_email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Alumno
        fields = ['str_idAlumno', 'str_nombres', 'str_apellidos', 'dt_fecha_nacimiento', 'bool_activo', 'str_email', 'password']
        read_only_fields = ['str_idAlumno']

    def create(self, validated_data):
        str_email = validated_data.pop('str_email')
        password = validated_data.pop('password')

        user = User(str_email=str_email, username=str_email)
        user.set_password(password)
        user.save()

        # Generar ID de alumno automáticamente (A001, A002, etc.)
        last_alumno = Alumno.objects.order_by('-str_idAlumno').first()
        if last_alumno:
            # Extraer el número del último ID y aumentarlo en 1
            last_id = last_alumno.str_idAlumno
            if last_id.startswith('A'):
                try:
                    num = int(last_id[1:]) + 1
                    new_id = f'A{num:03d}'
                except ValueError:
                    new_id = 'A001'
            else:
                new_id = 'A001'
        else:
            new_id = 'A001'

        alumno = Alumno.objects.create(str_idAlumno=new_id, int_idUser=user, **validated_data)
        return alumno

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Docente, Alumno

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class DocenteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Docente
        fields = ['id', 'codigo', 'nombres', 'apellidos', 'especialidad', 'activo', 'email']
        read_only_fields = ['id']

class DocenteCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Docente
        fields = ['id', 'codigo', 'nombres', 'apellidos', 'especialidad', 'activo', 'email', 'password']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        user = User(email=email)
        user.set_password(password)
        user.save()
        
        docente = Docente.objects.create(user=user, **validated_data)
        return docente

class AlumnoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Alumno
        fields = ['id', 'codigo', 'nombres', 'apellidos', 'fecha_nacimiento', 'activo', 'email']
        read_only_fields = ['id']

class AlumnoCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Alumno
        fields = ['id', 'codigo', 'nombres', 'apellidos', 'fecha_nacimiento', 'activo', 'email', 'password']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        user = User(email=email)
        user.set_password(password)
        user.save()
        
        alumno = Alumno.objects.create(user=user, **validated_data)
        return alumno

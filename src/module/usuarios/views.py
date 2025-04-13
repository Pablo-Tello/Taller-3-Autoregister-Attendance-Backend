from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Docente, Alumno
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    DocenteSerializer, 
    DocenteCreateSerializer, 
    AlumnoSerializer, 
    AlumnoCreateSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DocenteCreateSerializer
        return DocenteSerializer
    
    def get_queryset(self):
        queryset = Docente.objects.all()
        activo = self.request.query_params.get('activo', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
            
        return queryset

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AlumnoCreateSerializer
        return AlumnoSerializer
    
    def get_queryset(self):
        queryset = Alumno.objects.all()
        activo = self.request.query_params.get('activo', None)
        
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
            
        return queryset

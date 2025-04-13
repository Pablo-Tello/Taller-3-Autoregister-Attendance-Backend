from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlumnoSeccionViewSet, DocenteSeccionViewSet

router = DefaultRouter()
router.register('alumnos-secciones', AlumnoSeccionViewSet)
router.register('docentes-secciones', DocenteSeccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

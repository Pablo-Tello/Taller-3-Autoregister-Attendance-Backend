from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CicloAcademicoViewSet,
    CalendarioViewSet,
    CursoViewSet,
    SyllabusViewSet,
    SeccionViewSet,
    SesionClaseViewSet,
    HorarioViewSet
)

router = DefaultRouter()
router.register('ciclos', CicloAcademicoViewSet)
router.register('calendarios', CalendarioViewSet)
router.register('cursos', CursoViewSet)
router.register('syllabus', SyllabusViewSet)
router.register('secciones', SeccionViewSet)
router.register('horarios', HorarioViewSet)
router.register('sesiones', SesionClaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

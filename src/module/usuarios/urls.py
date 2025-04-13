from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DocenteViewSet, AlumnoViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('docentes', DocenteViewSet)
router.register('alumnos', AlumnoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

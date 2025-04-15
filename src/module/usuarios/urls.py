from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DocenteViewSet, AlumnoViewSet, login_view, logout_view

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('docentes', DocenteViewSet)
router.register('alumnos', AlumnoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

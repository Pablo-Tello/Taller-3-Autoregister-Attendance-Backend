from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsistenciaViewSet, CodigoQRViewSet

router = DefaultRouter()
router.register('asistencias', AsistenciaViewSet)
router.register('codigos-qr', CodigoQRViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

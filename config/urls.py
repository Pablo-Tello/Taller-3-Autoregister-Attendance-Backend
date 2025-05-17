from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Asistencia UNI API Documentation",
        default_version="v0.1",
        description="Endpoints for API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    path('admin/', admin.site.urls),
    path('api/academico/', include('src.module.academico.urls')),
    path('api/usuarios/', include('src.module.usuarios.urls')),
    path('api/inscripciones/', include('src.module.inscripciones.urls')),
    path('api/asistencia/', include('src.module.asistencia.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('docs/', include_docs_urls(title='API Documentation')),

    # URLs de Swagger
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(
            r'^static/(?P<path>.*)$',
            serve,
            {'document_root': settings.STATIC_ROOT}
        ),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

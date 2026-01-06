from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="PTJobs API",
        default_version='v1',
        description="APIs for PTJobs App",
        contact=openapi.Contact(email="nganthanhphu@ou.edu.vn"),
        license=openapi.License(name="Ngàn Thành Phú@2025"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('', include('ptjobs.urls')),
    path('admin/', admin_site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path('o/', include('oauth2_provider.urls',
                       namespace='oauth2_provider')),

]
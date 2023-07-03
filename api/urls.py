from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from api.swagger import schema_view

urlpatterns = [
    path(
        'v1/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'v1/redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

urlpatterns += staticfiles_urlpatterns()

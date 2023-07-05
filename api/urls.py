from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers

from api.swagger import schema_view

from api.views import UsersViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
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

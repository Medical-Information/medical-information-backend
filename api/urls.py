from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.views import (
    AnnotatedUserViewSet,
    ArticleViewSet,
    TagViewSet,
    TokenCreateView,
    TokenDestroyView,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', AnnotatedUserViewSet, basename='users')
router_v1.register(r'articles', ArticleViewSet, basename='articles')
router_v1.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/login/', TokenCreateView.as_view(), name='login'),
    path('v1/auth/logout/', TokenDestroyView.as_view(), name='logout'),
    path('v1/schema/', SpectacularAPIView.as_view(), name='openapi-schema'),
    path(
        'v1/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='api:openapi-schema'),
        name='swagger-ui',
    ),
    path(
        'v1/schema/redoc/',
        SpectacularRedocView.as_view(url_name='api:openapi-schema'),
        name='redoc',
    ),
]

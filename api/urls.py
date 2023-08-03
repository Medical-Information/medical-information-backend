from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.views import (
    ArticleViewSet,
    CommentViewSet,
    TagViewSet,
    TokenCreateView,
    TokenDestroyView,
    UserViewSet,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'articles', ArticleViewSet, basename='articles')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(
    r'articles\/(?P<acticle_id>'
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    r'\/comments',
    CommentViewSet, basename='comments'
)

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

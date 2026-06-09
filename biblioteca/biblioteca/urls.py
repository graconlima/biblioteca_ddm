from django.contrib import admin 
from django.urls import path, include 
from rest_framework import routers 
from livros.views import AutorViewSet, LivroViewSet, registrar_token, enviar_notificacao
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi 
from rest_framework import permissions 

router = routers.DefaultRouter() 
router.register(r'autores', AutorViewSet) 
router.register(r'livros', LivroViewSet) 
schema_view = get_schema_view( 
    openapi.Info( 
        title="API Biblioteca", 
        default_version='v1', 
        description="Documentação da API de Biblioteca Digital", 
        contact=openapi.Contact(email="contato@exemplo.com"), 
        license=openapi.License(name="MIT"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
) 

urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'), 
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'), 
    path('registrar_token_firebase/', registrar_token_firebase),
    path('notificar_firebase/', notificar_firebase),
]

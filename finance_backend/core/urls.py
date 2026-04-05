from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Generates the raw JSON blueprint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Renders the Swagger UI using the JSON above
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Auth endpoints (Login / Refresh)
    path('api/auth/', include('accounts.urls')),
    
    # Finance endpoints
    path('api/finance/', include('finance.urls')),
]
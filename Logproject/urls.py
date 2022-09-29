from django.contrib import admin
from django.urls import path
from logapp import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view

from django.urls import re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_swagger_view(title="Swagger Docs")

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('log/', views.LogCreateAPIView.as_view(), name='log'),
    path('findindex/', views.FindindexAPIView.as_view(), name='findindex'),
    path('email-send/', views.EmailSendAPIView.as_view(), name='email-send'),
    path('new_log/', views.NewLogLogCreatePost.as_view(), name='new-log'),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

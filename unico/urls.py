
from django.contrib import admin
from django.urls import path, include
from core import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

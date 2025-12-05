from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes import views as recipe_views
from accounts import views as account_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),               
    path('accounts/', include('accounts.urls')),     
    path('feedback/', include('feedback.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


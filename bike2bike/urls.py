from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from social import views as social_views  # importa as views do app 'social'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    
    path('', include('social.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


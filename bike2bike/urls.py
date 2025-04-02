from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bike2bike.view import HomepageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('social/', include('social.urls')),
    path('', HomepageView.as_view(), name='homepage'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


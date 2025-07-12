from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import non_logged_home
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
     path('', non_logged_home, name='non_logged_home'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('user/', include('user.urls')),
]+debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
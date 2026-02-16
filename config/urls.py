from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name='home'),
    path('', include('website.urls')),
    path("book/", include("bookings.urls")),
    path("tracking/", include("tracking.urls")),
    path("blog/", include("blog.urls")),



]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

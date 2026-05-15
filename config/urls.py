from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView
from core.views import home
from .sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name='home'),
    path('', include('website.urls')),
    path("book/", include("bookings.urls")),
    path("tracking/", include("tracking.urls")),
    path("blog/", include("blog.urls")),
    path('invites/', include('invites.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),




]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

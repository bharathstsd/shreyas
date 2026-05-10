from django.conf import settings
from django.templatetags.static import static

from .models import SiteSetting


def brand(request):
    brand_data = settings.BRAND.copy()
    site_settings = SiteSetting.objects.first()

    if site_settings:
        brand_data["name"] = site_settings.site_name
        brand_data["short_name"] = site_settings.short_name
        if site_settings.logo:
            brand_data["logo_url"] = site_settings.logo.url

    brand_data.setdefault("logo_url", static(brand_data["logo"]))

    main_menu = [
        {"label": "Home", "url": "/"},
        {"label": "Programs", "url": "/programs/"},
        {"label": "Transformations", "url": "/transformations/"},
        {"label": "Team", "url": "/team/"},
        {"label": "Gallery", "url": "/gallery/"},
        {"label": "About", "url": "/about/"},
        {"label": "Blog", "url": "/blog/"},
        {"label": "Contact", "url": "/contact/"},
    ]

    return {
        "brand": brand_data,
        "site_settings": site_settings,
        "main_menu": main_menu,
    }

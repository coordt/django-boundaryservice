from django.conf import settings
from django.db.utils import DatabaseError

def get_site_url_root():
    try:
        from django.contrib.sites.models import Site
        if 'django.contrib.sites' not in settings.INSTALLED_APPS:
            raise ImportError
        CURRENT_SITE = Site.objects.get(pk=settings.SITE_ID).values_list('domain', flat=True)[0]
    except (ImportError, DatabaseError):
        CURRENT_SITE = "localhost"
    domain = CURRENT_SITE
    protocol = getattr(settings, 'DEFAULT_PROTOCOL', 'http')
    url = f'{protocol}://{domain}'
    if port := getattr(settings, 'DEFAULT_PORT', ''):
        url += f':{port}'
    return url
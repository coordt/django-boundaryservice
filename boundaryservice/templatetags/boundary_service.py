from django import template

register = template.Library()

@register.simple_tag
def boundary_svc_api_prefix():
    """
    Return the boundary service api prefix
    """
    from boundaryservice.settings import DEFAULT_SETTINGS
    return f"{DEFAULT_SETTINGS['API_DOMAIN']}{DEFAULT_SETTINGS['API_PREFIX']}"
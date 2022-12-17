import time

from django.core.cache import cache
from tastypie.throttle import CacheThrottle

class AnonymousThrottle(CacheThrottle):
    """
    Anonymous users are throttled, but those with a valid API key are not.
    """
    def should_be_throttled(self, identifier, **kwargs):
        return (
            super(AnonymousThrottle, self).should_be_throttled(
                identifier, **kwargs
            )
            if identifier.startswith('anonymous_')
            else False
        )

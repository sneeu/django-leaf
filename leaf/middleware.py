from views import page_detail
from django.http import Http404, HttpResponsePermanentRedirect
from django.conf import settings


class LeafPageFallbackMiddleware(object):
    """
    Very similar to Django's own FlatpageFallbackMiddleware.
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            path = request.path_info.lstrip('/')
            if path[-1] != '/':
                return HttpResponsePermanentRedirect(path + '/')
            return page_detail(request, path)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
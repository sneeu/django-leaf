from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from models import Page


def page_detail(request, url):
    page = get_object_or_404(Page, url=url)
    context = {'page': page}
    return render_to_response('leaf/page_detail.html', RequestContext(
        request, context))

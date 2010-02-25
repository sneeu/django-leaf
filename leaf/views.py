from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader

from models import Page


def page_detail(request, url):
    if len(url) <= 0 or not url[0] == '/':
        url = '/%s' % url

    page = get_object_or_404(Page, url=url)

    if page.container_only:
        children = page.children.all()
        if len(children) > 0:
            return HttpResponseRedirect(children[0].get_absolute_url())

    template = loader.select_template([
            'leaf%s.html' % url.rstrip('/'),
            'leaf/page_detail.html'])

    context = {
        'description': page.description,
        'keywords': page.keywords,
        'page': page,
        'title': page.title,
    }

    return HttpResponse(template.render(RequestContext(request, context)))

from django.core.urlresolvers import resolve
from django.http import Http404

from leaf.models import Page


def navigation(page):
    if type(page) is str:
        page = Page.objects.get(url=page)

    navigation = (
            [('/', 'Home', None, page is None)] +
            [
                (p.url, p.title, _children(p), )
                for p in Page.objects.filter(parent__isnull=True).exclude(url__exact='/')
            ],
        )

    return navigation


def _children(page):
    if type(page) is str:
        page = Page.objects.get(url=page)

    children = page.children.all()

    children_nav = tuple()
    if children:
        children_nav = ([(p.url, p.title, _children(p), )
            for p in page.children.all()], )

    try:
        view, _, _ = resolve(page.url)
    except Http404:
        return children_nav

    view_nav = getattr(view, 'navigation', tuple())
    if view_nav:
        if callable(view_nav):
            return children_nav + view_nav()
    return children_nav

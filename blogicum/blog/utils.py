from django.core.paginator import Paginator

from .constants import POSTS_ON_PAGE


def formation_pagination(request, posts):
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

from django.shortcuts import render
from custom.models import Section, Page, AlbumBlock, FileSetBlock


def constructor(request, url):

    page = Page.objects.get(url=url)

    context = {
        'title': page.title,
        'albums': AlbumBlock.objects.filter(page__url=url),
        'filesets': FileSetBlock.objects.filter(page__url=url),
        'current_page': page,
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None)
    }
    return render(request, 'custom/page.html', context)

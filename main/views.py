from django.shortcuts import render
from custom.models import Page, Section


def index(request):
    context = {
        'title': 'Главная',
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None)
    }

    return render(request, 'main/index.html', context)


def reviews(request):
    context = {
        'title': 'Отзывы',
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None)
    }

    return render(request, 'main/reviews.html', context)


def faq(request):
    context = {
        'title': 'Вопрос - ответ',
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None)
    }

    return render(request, 'main/faq.html', context)


def consultation(request):
    context = {
        'title': 'Интерактивная консультация',
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None)
    }

    return render(request, 'main/consultation.html', context)


def geography(request):
    context = {
        'title': 'География ранней помощи',
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None)
    }

    return render(request, 'main/geography.html', context)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from authentication.models import User
from .models import Article, ArticleFile, ArticleApprovalApplication


@login_required
def account(request):

    not_treated = ArticleApprovalApplication.objects.filter(article__author__pk=request.user.pk, treated=False)
    rejected = ArticleApprovalApplication.objects.filter(article__author__pk=request.user.pk, treated=True, response=False)

    context = {
        'title': 'Личный кабинет',
        'not_treated': not_treated,
        'rejected': rejected,
    }

    return render(request, 'specialists/account.html', context)


def profile(request, pk):

    specialist = User.objects.get(pk=pk)

    context = {
        'title': f'{specialist}',
        'specialist': specialist
    }

    return render(request, 'specialists/profile.html', context)


def article(request, pk):

    art = Article.objects.get(pk=pk)

    context = {
        'title': f'{art}',
        'article': art,
        'files': len(art.get_files) > 0
    }

    return render(request, 'specialists/article.html', context)


class SpecialistsList(ListView):
    model = User
    template_name = 'specialists/specialists.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Специалисты ранней помощи'

        return context

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, approved=True)


@login_required
def create_article_page(request):

    context = {
        'title': 'Новый материал',
    }

    return render(request, 'specialists/create_article_page.html', context)


@login_required
def create_article(request):
    theme = request.POST.get('theme')
    title = request.POST.get('title')
    text = request.POST.get('text')

    if request.recaptcha_is_valid:
        if theme and title and text:
            try:
                art = Article.objects.create(author=request.user, theme=theme, title=title, text=text)
                ArticleApprovalApplication.objects.create(article=art)
                for pk_name, file in request.FILES.items():
                    name = pk_name[pk_name.index('-') + 1:]
                    ArticleFile.objects.create(file=file, article=art, name=name)
                return JsonResponse({'result': 'ok'})
            except:
                pass
    else:
        return JsonResponse({'result': 'captcha'})

    return JsonResponse({'result': 'failed'})


@login_required
def edit_article_page(request, pk):

    art = Article.objects.get(pk=pk)

    context = {
        'title': 'Редактирование материала',
        'article': art if not art.approved else None
    }

    return render(request, 'specialists/edit_article_page.html', context)


@login_required
def edit_article(request):

    pk = int(request.POST.get('pk'))
    theme = request.POST.get('theme')
    title = request.POST.get('title')
    text = request.POST.get('text')
    kept_files = [int(i) for i in request.POST.get('kept_files').split(',')]

    if request.recaptcha_is_valid:
        art = Article.objects.get(pk=pk)
        if not art.approved:
            try:
                art.theme = theme
                art.title = title
                art.text = text
                art.save()
                current_files = art.get_files
                for file in current_files:
                    if file.pk not in kept_files:
                        ArticleFile.objects.get(pk=file.pk).delete()
                for pk_name, file in request.FILES.items():
                    name = pk_name[pk_name.index('-') + 1:]
                    ArticleFile.objects.create(file=file, article=art, name=name)
                return JsonResponse({'result': 'ok'})
            except:
                pass
    else:
        return JsonResponse({'result': 'captcha'})

    return JsonResponse({'result': 'failed'})


@login_required
def delete_article(request):
    pk = int(request.POST.get('pk'))
    Article.objects.get(pk=pk).delete()
    return JsonResponse({'result': 'ok'})


@login_required
def delete_application(request):
    pk = int(request.POST.get('pk'))
    ArticleApprovalApplication.objects.get(pk=pk).article.delete()
    return JsonResponse({'result': 'ok'})


@login_required
def hide_article(request):
    pk = int(request.POST.get('pk'))
    art = Article.objects.get(pk=pk)
    art.hidden = not art.hidden
    art.save()
    return JsonResponse({'result': 'ok'})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import UserLoginForm, UserRegisterForm, UserPasswordChangeForm
from .models import UserApprovalApplication, FieldOfActivity, UserEditApplication, User
import os
from custom.models import Section, Page
from main.models import SiteContent
from PIL import Image
from MedProject.settings import BASE_DIR


def login(request):
    login_form = UserLoginForm(data=request.POST)
    if 'next' in request.GET.keys():
        next_value = request.GET['next']
    else:
        next_value = ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
            elif 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('specialists:account'))
    context = {
        'title': 'Авторизация',
        'login_form': login_form,
        'next': next_value,
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None),
        'header_content': [SiteContent.objects.get(name='email').content,
                                     SiteContent.objects.get(name='phone').content,
                                     SiteContent.objects.get(name='phone').content.translate(
                                         str.maketrans({' ': '', '-': '', '(': '', ')': ''}))]
    }
    return render(request, 'authentication/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            user.username = user.email
            user.save()
            UserApprovalApplication.objects.create(user=user)
            user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password1'))
            if user:
                auth.login(request, user)
            return HttpResponseRedirect(reverse('specialists:account'))
    else:
        register_form = UserRegisterForm()

    register_list = list(register_form)
    context = {
        'title': 'Регистрация',
        'first_block': register_list[0:7],
        'second_block': register_list[7:14],
        'third_block': register_list[-2:],
        'menu_sections': Section.objects.all(),
        'menu_pages': Page.objects.filter(section=None),
        'header_content': [SiteContent.objects.get(name='email').content,
                                     SiteContent.objects.get(name='phone').content,
                                     SiteContent.objects.get(name='phone').content.translate(
                                         str.maketrans({' ': '', '-': '', '(': '', ')': ''}))]
    }
    return render(request, 'authentication/register.html', context)


@login_required
def edit_profile_page(request):

    context = {
        'title': 'Редактирование профиля',
        'fields_of_activity': FieldOfActivity.objects.all(),
        'header_content': [SiteContent.objects.get(name='email').content,
                                     SiteContent.objects.get(name='phone').content,
                                     SiteContent.objects.get(name='phone').content.translate(
                                         str.maketrans({' ': '', '-': '', '(': '', ')': ''}))]
    }
    return render(request, 'authentication/edit_profile.html', context)


@login_required
def edit_profile(request):

    field = request.POST.get('field')
    new_value = request.POST.get('new_value')

    if request.recaptcha_is_valid:
        if field in ['first_name', 'patronymic', 'last_name', 'birthdate',
                     'field_of_activity', 'profession', 'city', 'workplace_address', 'workplace_name',
                     'phone_number', 'email', 'photo', 'description']:

            old_value = str(getattr(request.user, field))
            if field == 'birthdate':
                old_value = f'{old_value[8:]}-{old_value[5:7]}-{old_value[:4]}'

            if old_value == new_value:
                return JsonResponse({'result': 'ok'})

            if field == 'photo':
                file = request.FILES.get('photo')
                img = Image.open(file)
                file_name = '.'.join([*file.name.split('.')[:-1], 'jpg']).split('/')[-1]
                new_file_path = os.path.join(BASE_DIR, 'media', 'profile_photos', file_name)
                width = img.size[0]
                height = img.size[1]
                ratio = width / height
                if ratio > 1 and width > 1024:
                    sizes = [1024, int(1024 / ratio)]
                    img = img.resize(sizes)
                elif height > 1024:
                    sizes = [int(1024 * ratio), 1024]
                    img = img.resize(sizes)
                try:
                    img.save(new_file_path, quality=90, optimize=True)
                except OSError:
                    img = img.convert("RGB")
                    img.save(new_file_path, quality=90, optimize=True)
                new_value = 'profile_photos/' + file_name
                old = UserEditApplication.objects.filter(field=field, user__pk=request.user.pk)
                if old.exists():
                    try:
                        os.remove(os.path.join(BASE_DIR, 'media', *old.last().new_value.split('/')))
                    except FileNotFoundError:
                        pass
            elif field == 'email' and User.objects.filter(email=new_value).exists():
                return JsonResponse({'result': 'email'})

            if field == 'field_of_activity' and not FieldOfActivity.objects.filter(pk=int(new_value)).exists():
                return JsonResponse({'result': 'failed'})
            elif field == 'field_of_activity':
                new_value = f'id:{new_value}|{FieldOfActivity.objects.get(pk=int(new_value)).name}'

            verbose_field = User._meta.get_field(field).verbose_name

            UserEditApplication.objects.filter(field=field, user__pk=request.user.pk).delete()
            application = UserEditApplication.objects.create(user=request.user, field=field, new_value=new_value,
                                                             old_value=old_value, verbose_field=verbose_field)

            return JsonResponse({'result': 'ok', 'pk': application.pk, 'verbose_field': verbose_field,
                                 'new_value': new_value})
        else:
            pass
    else:
        return JsonResponse({'result': 'captcha'})

    return JsonResponse({'result': 'failed'})


@login_required
def delete_application(request):
    pk = request.POST.get('pk')
    try:
        app = UserEditApplication.objects.get(pk=int(pk))
        if app.field == 'photo':
            os.remove(os.path.join(BASE_DIR, 'media', *app.new_value.split('/')))
        app.delete()
    except:
        pass
    return JsonResponse({'result': 'ok'})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('specialists:account'))
    else:
        form = UserPasswordChangeForm(request.user)

    context = {
        'title': 'Смена пароля',
        'form': form,
        'header_content': [SiteContent.objects.get(name='email').content,
                                     SiteContent.objects.get(name='phone').content,
                                     SiteContent.objects.get(name='phone').content.translate(
                                         str.maketrans({' ': '', '-': '', '(': '', ')': ''}))]
    }

    return render(request, 'authentication/change_password.html', context=context)

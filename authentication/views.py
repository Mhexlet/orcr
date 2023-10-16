from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import UserLoginForm, UserRegisterForm
from .models import UserApprovalApplication, FieldOfActivity, UserEditApplication, User
from django.core.files.storage import default_storage, FileSystemStorage
from MedProject.settings import MEDIA_ROOT
import os


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
        'next': next_value
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
        'third_block': register_list[-2:]
    }
    return render(request, 'authentication/register.html', context)


@login_required
def edit_profile_page(request):

    context = {
        'title': 'Редактирование профиля',
        'fields_of_activity': FieldOfActivity.objects.all()
    }
    return render(request, 'authentication/edit_profile.html', context)


@login_required
def edit_profile(request):

    field = request.POST.get('field')
    new_value = request.POST.get('new_value')

    if request.recaptcha_is_valid:
        if field in ['first_name', 'patronymic', 'last_name', 'birthdate',
                     'field_of_activity', 'profession', 'city', 'workplace_address', 'workplace_name',
                     'phone_number', 'email', 'photo', 'description'] and field != getattr(request.user, field):
            
            if field == 'photo':
                file = request.FILES.get('photo')
                fs = FileSystemStorage(location=os.path.join(MEDIA_ROOT, 'profile_photos'))
                filename = fs.save(file.name, file)
                new_value = 'profile_photos/' + filename
            elif field == 'email' and User.objects.filter(email=new_value).exists():
                return JsonResponse({'result': 'email'})

            if field == 'field_of_activity' and not FieldOfActivity.objects.filter(pk=int(new_value)).exists():
                return JsonResponse({'result': 'failed'})
            elif field == 'field_of_activity':
                new_value = f'id:{new_value}|{FieldOfActivity.objects.get(pk=int(new_value)).name}'

            old_value = str(getattr(request.user, field))
            if field == 'birthdate':
                old_value = f'{old_value[8:]}-{old_value[5:7]}-{old_value[:4]}'

            UserEditApplication.objects.create(user=request.user, field=field, new_value=new_value,
                                               old_value=old_value)
            return JsonResponse({'result': 'ok'})
        else:
            pass
    else:
        return JsonResponse({'result': 'captcha'})

    return JsonResponse({'result': 'failed'})




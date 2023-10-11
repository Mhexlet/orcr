from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserLoginForm, UserRegisterForm, UserEditForm
from .models import UserApprovalApplication


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
def edit_profile(request):

    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('specialists:account'))
    else:
        edit_form = UserEditForm(initial={
            'email': request.user.email,
            'last_name': request.user.last_name,
            'first_name': request.user.first_name,
            'patronymic': request.user.patronymic,
            'birthdate': request.user.birthdate,
            'phone_number': request.user.phone_number,
            'field_of_activity': request.user.field_of_activity,
            'profession': request.user.profession,
            'city': request.user.city,
            'workplace_address': request.user.workplace_address,
            'workplace_name': request.user.workplace_name,
            # 'photo': request.user.photo,
            'description': request.user.description})

    edit_list = list(edit_form)
    context = {
        'title': 'Редактирование профиля',
        'first_block': edit_list[0:6],
        'second_block': edit_list[6:12],
        'third_block': edit_list[-3:]
    }
    return render(request, 'authentication/edit_profile.html', context)

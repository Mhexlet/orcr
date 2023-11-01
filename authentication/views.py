from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .admin import compress_img
from .forms import UserLoginForm, UserRegisterForm, UserPasswordChangeForm
from .models import UserApprovalApplication, FieldOfActivity, UserEditApplication, User
import os
from custom.models import Section, Page
from PIL import Image
from MedProject.settings import BASE_DIR
from django.conf import settings
from django.core.mail import send_mail
from main.models import SiteContent
from datetime import datetime
import pytz
import hashlib
import calendar
import time
from uuid import uuid4


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
            send_verify_email(user)
            compress_img(user, 'photo', 'profile_photos')
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


def verify(request, email, key):
    user = get_object_or_404(User, email=email)
    if user:
        if key == user.verification_key and not user.is_verification_key_expired:
            user.email_verified = True
            user.verification_key = None
            user.verification_key_expires = None
            user.save()
            auth.login(request, user)
            return render(request, 'authentication/notification.html',
                          context={'notification': 'Почта успешно подтверждена!'})
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Что-то пошло не так! Попробуйте отправить письмо повторно '
                                           'или обновить ключ подтверждения через личный кабинет.'})


def send_verify_email(user):
    verify_link = reverse('authentication:verify', args=[user.email, user.verification_key])
    full_link = f'{settings.BASE_URL}{verify_link}'
    try:
        message_beginning = SiteContent.objects.get(name='email_verification_message_beginning').content
    except ObjectDoesNotExist:
        message_beginning = 'Здравствуйте,\n\nПерейдите по ссылке, чтобы подтвердить свой адрес электронной почты:'
    try:
        message_ending = SiteContent.objects.get(name='email_verification_message_ending').content
    except ObjectDoesNotExist:
        message_ending = '\n\nС уважением'

    message = f'{message_beginning} {full_link} {message_ending}'
    return send_mail(
        'Подтверждение почты',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


@login_required
def send_verify_email_page(request):
    send_verify_email(request.user)
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Письмо со ссылкой для подтверждения адреса электронной почты '
                                           'было успешно отправлено!'})


@login_required
def renew_verification_key(request):
    user = request.user
    user.verification_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
    user.verification_key_expires = datetime.now(pytz.timezone(settings.TIME_ZONE))
    user.save()
    send_verify_email(request.user)
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Письмо со ссылкой для подтверждения адреса электронной почты '
                                           'было успешно отправлено!'})


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
                current_gmt = time.gmtime()
                time_stamp = calendar.timegm(current_gmt)
                file_name = f'{time_stamp}-{uuid4().hex}.jpg'
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
                previous = UserEditApplication.objects.filter(field=field, user__pk=request.user.pk)
                if previous.exists() and not previous.last().response:
                    try:
                        os.remove(os.path.join(BASE_DIR, 'media', *previous.last().new_value.split('/')))
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


@login_required
def send_application(request):
    UserApprovalApplication.objects.create(user=request.user)
    return render(request, 'authentication/notification.html',
                  context={'notification': 'Новая заявка на одобрение профиля успешно отправлена!'})

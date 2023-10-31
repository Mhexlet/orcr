from django.urls import path
import authentication.views as auth
from main.decorators import check_recaptcha
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

app_name = 'authentication'

urlpatterns = [
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('register/', auth.register, name='register'),
    path('edit_profile_page/', auth.edit_profile_page, name='edit_profile_page'),
    path('edit_profile/', check_recaptcha(auth.edit_profile), name='edit_profile'),
    path('delete_application/', auth.delete_application, name='delete_application'),
    path('change_password/', auth.change_password, name='change_password'),
    path('verify/<str:email>/<str:key>/', auth.verify, name='verify'),
    path('send_verify_email_page/', auth.send_verify_email_page, name='send_verify_email_page'),
    path('renew_verification_key/', auth.renew_verification_key, name='renew_verification_key'),
    path('send_application/', auth.send_application, name='send_application'),
    path('password-reset/', PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
]

from django.urls import path
import authentication.views as auth
from main.decorators import check_recaptcha

app_name = 'authentication'

urlpatterns = [
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('register/', auth.register, name='register'),
    path('edit_profile_page/', auth.edit_profile_page, name='edit_profile_page'),
    path('edit_profile/', check_recaptcha(auth.edit_profile), name='edit_profile'),
]

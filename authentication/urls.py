from django.urls import path
import authentication.views as auth

app_name = 'authentication'

urlpatterns = [
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('register/', auth.register, name='register'),
    path('edit_profile/', auth.edit_profile, name='edit_profile'),
]

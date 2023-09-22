from django.urls import path
import custom.views as custom

app_name = 'custom'

urlpatterns = [
    path('<str:url>/', custom.constructor, name='constructor'),
]
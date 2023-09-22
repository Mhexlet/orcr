"""
URL configuration for MedProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from MedProject import settings
import main.views as main

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', main.index, name='index'),
    path('reviews/', main.reviews, name='reviews'),
    path('faq/', main.faq, name='faq'),
    path('consultation/', main.consultation, name='consultation'),
    path('geography/', main.geography, name='geography'),

    path('custom/', include('custom.urls', namespace='custom')),
    path('authentication/', include('authentication.urls', namespace='authentication')),
    path('specialists/', include('specialists.urls', namespace='specialists')),

    path('editor/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

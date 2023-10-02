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
from main.decorators import check_recaptcha

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', main.index, name='index'),
    path('reviews/', main.ReviewsList.as_view(), name='reviews'),
    path('reviews/<int:page>/', main.ReviewsList.as_view(), name='reviews_page'),
    path('create_review/', check_recaptcha(main.create_review), name='create_review'),
    path('faq/', main.FaqView.as_view(), name='faq'),
    path('faq/<int:page>/', main.FaqView.as_view(), name='faq_page'),
    path('create_question/', check_recaptcha(main.create_question), name='create_question'),
    path('consultation/', main.consultation, name='consultation'),
    path('create_application/', check_recaptcha(main.create_application), name='create_application'),
    path('geography/', main.geography, name='geography'),
    path('news/', main.news, name='news'),
    path('news/<int:pk>/', main.single_news, name='single_news'),

    path('custom/', include('custom.urls', namespace='custom')),
    path('authentication/', include('authentication.urls', namespace='authentication')),
    path('specialists/', include('specialists.urls', namespace='specialists')),

    path('editor/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

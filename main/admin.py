import re

from django.contrib import admin
from .models import QuestionAnswer, Review, MainSliderImage, Application, Place, News
from django_summernote.admin import SummernoteModelAdmin


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuestionAnswer._meta.get_fields()]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Review._meta.get_fields()]


@admin.register(MainSliderImage)
class MainSliderImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MainSliderImage._meta.get_fields()]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Application._meta.get_fields()]


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Place._meta.get_fields()]

    def save_model(self, request, obj, form, change):
        if obj.src.startswith('<'):
            obj.src = re.search(r'src="[^ ]+', obj.src).group(0)[5:-1]
        obj.save()
        return super().save_model(request, obj, form, change)


@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = [field.name for field in News._meta.get_fields()]
    summernote_fields = ('content',)

import re

from django.contrib import admin
from .models import QuestionAnswer, Review, MainSliderImage, Application, Place, News
from django_summernote.admin import SummernoteModelAdmin


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_question', 'short_answer', 'approved']

    def short_question(self, obj):
        return obj.question[:50] + '...'

    short_question.short_description = 'Вопрос'

    def short_answer(self, obj):
        return obj.answer[:50] + '...'

    short_answer.short_description = 'Ответ'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name if field.name != 'text' else 'short_text' for field in Review._meta.get_fields()]

    def short_text(self, obj):
        return obj.text[:50] + '...'

    short_text.short_description = 'Текст'


@admin.register(MainSliderImage)
class MainSliderImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MainSliderImage._meta.get_fields()]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name if field.name != 'text' else 'short_text' for field in Application._meta.get_fields()]

    def short_text(self, obj):
        return obj.text[:50] + '...'

    short_text.short_description = 'Текст обращения'


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
    list_display = [field.name if field.name != 'content' else 'short_content' for field in News._meta.get_fields()]
    summernote_fields = ('content',)

    def short_content(self, obj):
        return obj.content[:50] + '...'

    short_content.short_description = 'Содержимое'

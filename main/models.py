import os

from django.db import models
from django.dispatch import receiver

from MedProject.settings import BASE_DIR


class QuestionAnswer(models.Model):

    name = models.CharField(max_length=64, verbose_name='Имя задавшего вопрос')
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(blank=True, null=True, verbose_name='Ответ')
    treated = models.BooleanField(default=False, verbose_name='Обработано')
    approved = models.BooleanField(default=False, verbose_name='Одобрено')

    class Meta:
        verbose_name = 'Вопрос - ответ'
        verbose_name_plural = 'Вопросы - ответы'

    def __str__(self):
        return self.question


class Review(models.Model):

    name = models.CharField(max_length=64, verbose_name='Имя оставившего отзыв')
    text = models.TextField(verbose_name='Отзыв')
    treated = models.BooleanField(default=False, verbose_name='Обработано')
    approved = models.BooleanField(default=False, verbose_name='Одобрено')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name}: {self.text[0:20]}...'


class MainSliderImage(models.Model):

    image = models.ImageField(upload_to='tmp/', verbose_name='Изображение')
    link = models.TextField(null=True, blank=True, verbose_name='Ссылка при клике (необязательно)')

    class Meta:
        verbose_name = 'Слайд с главной'
        verbose_name_plural = 'Слайды с главной'


class Banner(models.Model):

    image = models.ImageField(upload_to='tmp/', verbose_name='Изображение')
    name = models.CharField(max_length=128, verbose_name='Название')
    link = models.TextField(verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Баннер-ссылка'
        verbose_name_plural = 'Баннеры-ссылки'

    def __str__(self):
        return f'{self.name}'


class Application(models.Model):

    first_name = models.CharField(max_length=64, verbose_name='Имя')
    patronymic = models.CharField(max_length=64, verbose_name='Отчество')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    address = models.TextField(verbose_name='Адрес')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=16, verbose_name='Номер телефона')
    text = models.TextField(verbose_name='Текст обращения')
    answer = models.TextField(null=True, blank=True, verbose_name='Ответ')
    answering = models.CharField(max_length=64, null=True, blank=True, verbose_name='Имя ответившего')
    treated = models.BooleanField(default=False, verbose_name='Обработано')

    class Meta:
        verbose_name = 'Заявка на консультацию'
        verbose_name_plural = 'Заявки на консультацию'

    def __str__(self):
        return f'{self.first_name}: {self.text[0:20]}...'


class Place(models.Model):

    src = models.TextField(verbose_name='Ссылка на карту')
    name = models.CharField(max_length=64, verbose_name='Название места')

    class Meta:
        verbose_name = 'Место из географии ранней помощи'
        verbose_name_plural = 'Места из географии ранней помощи'

    def __str__(self):
        return self.name


class News(models.Model):

    title = models.CharField(max_length=64, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='tmp/', verbose_name='Изображение')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class SiteContent(models.Model):

    name = models.CharField(unique=True, max_length=64, verbose_name='Название')
    content = models.TextField(verbose_name='Содержимое')

    class Meta:
        verbose_name = 'Наполнение сайта'
        verbose_name_plural = 'Наполнения сайта'

    def __str__(self):
        return self.content


@receiver(models.signals.pre_delete, sender=MainSliderImage)
def delete_slider_img(sender, instance, using, origin, **kwargs):
    try:
        os.remove(os.path.join(BASE_DIR, 'media', instance.image.name))
    except FileNotFoundError:
        pass


@receiver(models.signals.pre_delete, sender=Banner)
def delete_banner_img(sender, instance, using, origin, **kwargs):
    try:
        os.remove(os.path.join(BASE_DIR, 'media', instance.image.name))
    except FileNotFoundError:
        pass


@receiver(models.signals.pre_delete, sender=News)
def delete_news_img(sender, instance, using, origin, **kwargs):
    try:
        os.remove(os.path.join(BASE_DIR, 'media', instance.image.name))
    except FileNotFoundError:
        pass
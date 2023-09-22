from django.db import models


class QuestionAnswer(models.Model):

    name = models.CharField(max_length=64, verbose_name='Имя задавшего вопрос')
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Вопрос - ответ'
        verbose_name_plural = 'Вопросы - ответы'

    def __str__(self):
        return self.question


class Review(models.Model):

    name = models.CharField(max_length=64, verbose_name='Имя оставившего отзыв')
    text = models.TextField(verbose_name='Отзыв')
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name}: {self.text[0:20]}...'


class MainSliderImage(models.Model):

    image = models.ImageField(upload_to='images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Слайд с главной'
        verbose_name_plural = 'Слайды с главной'


class Application(models.Model):

    first_name = models.CharField(max_length=64, verbose_name='Имя')
    patronymic = models.CharField(max_length=64, verbose_name='Отчество')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    address = models.TextField(verbose_name='Адрес')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=16, verbose_name='Номер телефона')
    text = models.TextField(verbose_name='Текст обращения')

    verbose_name = 'Заявки на консультацию'
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

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

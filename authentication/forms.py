from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import DateField
from django.contrib.admin import widgets
from authentication.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'med-input'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = ''


class UserRegisterForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    birthdate = DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y'], label='Дата рождения')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'last_name', 'first_name', 'patronymic', 'birthdate',
                  'field_of_activity', 'profession', 'city', 'workplace_address', 'workplace_name',
                  'phone_number', 'photo', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'med-input'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = ''
        self.fields['field_of_activity'].widget.attrs['class'] = 'register-field-of-activity'
        self.fields['birthdate'].widget.attrs['class'] = 'med-input datepicker'


class UserEditForm(UserChangeForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    birthdate = DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y'], label='Дата рождения')

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'birthdate', 'phone_number',
                  'field_of_activity', 'profession', 'city', 'workplace_address', 'workplace_name',
                  'photo', 'description', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'med-input'
            field.widget.attrs['placeholder'] = field.label
            field.help_text = ''
        self.fields['field_of_activity'].widget.attrs['class'] = 'register-field-of-activity'
        self.fields['birthdate'].widget.attrs['class'] = 'med-input datepicker'

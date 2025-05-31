from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User


class UserRegisterForm(UserCreationForm):

    usable_password = None

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'country', 'phone', 'password1', 'password2')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите свой Email",
        })
        self.fields['email'].help_text = None

        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите имя",
        })
        self.fields["first_name"].label = "Ваше имя"

        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите фамилию",
        })
        self.fields["last_name"].label = "Ваша фамилия"

        self.fields["avatar"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Загрузите свой аватар",
        })
        self.fields['avatar'].help_text = None

        self.fields["country"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите свою страну",
        })
        self.fields['country'].help_text = None

        self.fields["phone"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите номер телефона",
        })
        self.fields['phone'].help_text = None

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите пароль",
        })
        self.fields["password1"].label = "Пароль:"

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Повторите ввод пароля",
        })
        self.fields["password2"].label = "Подтверждение пароля:"


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
        self.fields['password'].label = "Пароль"


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'country', 'phone')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите имя",
        })
        self.fields["first_name"].label = "Ваше имя"

        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите фамилию",
        })
        self.fields["last_name"].label = "Ваша фамилия"

        self.fields["avatar"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Загрузите свой аватар",
        })
        self.fields['avatar'].help_text = None

        self.fields["country"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите свою страну",
        })
        self.fields['country'].help_text = None

        self.fields["phone"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите номер телефона",
        })
        self.fields['phone'].help_text = None

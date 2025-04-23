from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Deal, Client, Message
from PIL import Image
import os
from .models import ClientReview
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import CustomUser

# CustomUser моделін алу
User = get_user_model()

# ➤ Регистрация формасы
class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        }),
        required=True
    )

    user_type = forms.ChoiceField(
        label=_('Тип пользователя'),
        choices=[('admin', 'Administrator'), ('manager', 'Manager')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2', 'captcha')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_("Этот email уже зарегистрирован"))
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Электронный адрес или номер телефона",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email или номер телефона'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


# ➤ Сделка формасы
class DealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all()
        self.fields['document'].required = False
        self.fields['image'].required = False

    class Meta:
        model = Deal
        fields = ['client', 'title', 'description', 'amount', 'status', 'document', 'image']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.xls,.xlsx'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png,image/gif'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 100:
            raise ValidationError(_("Максимальная длина названия - 100 символов"))
        return title

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError(_("Сумма должна быть положительной"))
        return amount

    def clean_document(self):
        document = self.cleaned_data.get('document')
        if document:
            ext = os.path.splitext(document.name)[1].lower()
            valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
            if ext not in valid_extensions:
                raise ValidationError(_("Неподдерживаемый формат документа: %(formats)s") % {'formats': ', '.join(valid_extensions)})
            mime_type = getattr(document, 'content_type', '').lower()
            valid_mime_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ]
            if mime_type and mime_type not in valid_mime_types:
                raise ValidationError(_("Неверный тип файла документа"))
            if document.size > 5 * 1024 * 1024:
                raise ValidationError(_("Максимальный размер документа - 5MB"))
            if document.name.split('.')[-1].lower() in ['exe', 'bat', 'cmd', 'sh']:
                raise ValidationError(_("Загрузка исполняемых файлов запрещена"))
        return document

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if ext not in valid_extensions:
                raise ValidationError(_("Неподдерживаемый формат изображения: %(formats)s") % {'formats': ', '.join(valid_extensions)})
            mime_type = getattr(image, 'content_type', '').lower()
            valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
            if mime_type and mime_type not in valid_mime_types:
                raise ValidationError(_("Неверный тип файла изображения"))
            if image.size > 2 * 1024 * 1024:
                raise ValidationError(_("Максимальный размер изображения - 2MB"))
            try:
                img = Image.open(image)
                img.verify()
            except Exception:
                raise ValidationError(_("Поврежденный файл изображения"))
        return image

    def save(self, commit=True):
        deal = super().save(commit=False)
        if self.user:
            deal.created_by = self.user
        if commit:
            deal.save()
        return deal
class SomeForm(forms.Form):
    field1 = forms.CharField(max_length=100)
    field2 = forms.IntegerField()
    field3 = forms.DateField()

# ➤ Клиент формасы
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '200'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'\+?[0-9\s\-\(\)]+', 'title': _('Формат: +7 (XXX) XXX-XX-XX')}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'maxlength': '500'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) < 10:
            raise ValidationError(_("Номер телефона должен содержать минимум 10 цифр"))
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError(_("Клиент с таким email уже существует"))
        return email

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('phone') and not cleaned_data.get('email'):
            raise ValidationError(_("Необходимо указать телефон или email"))
        return cleaned_data


class ClientReviewForm(forms.ModelForm):
    class Meta:
        model = ClientReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# ➤ Сообщение форма
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']  # Добавляем поле для получателя
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите ваше сообщение...',
                'rows': 4,
            }),
            'receiver': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

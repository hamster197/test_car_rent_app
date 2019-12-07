import string

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from project.models import Language, Car


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Введите email', required=True, help_text='yourmail@mail.ru')
    password1 = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput, required=True,
                                help_text='min 8', min_length=8,)
    password2 = forms.CharField(label='Repeat password', max_length=20, widget=forms.PasswordInput, required=True,
                                help_text='min 8', min_length=8)
    name = forms.CharField(label='Name:', max_length=20, required=True, help_text='min 8'
                           , min_length=8)
    lang = forms.ModelChoiceField(queryset=Language.objects.all(), initial='Rus',
                                  label='Language:')



    def clean_name(self):
        name = self.cleaned_data['name']
        if User.objects.filter(username=name).exists():
            raise ValidationError("Логин уже зарегестрирован в системе!")
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email уже зарегестрирован в системе!")
        return email


    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password1')
        re_password = self.cleaned_data.get('password2')
        if not password == re_password:
            self.add_error('password1', 'Пароли не совпадают!')
        has_no = set(password).isdisjoint
        if (len(password) < 8
                or has_no(string.digits)
                or has_no(string.ascii_lowercase)
                or has_no(string.ascii_uppercase)):
                self.add_error('password1', 'Пароль должнен содержеть цифры, прописные и строчные буквы!')



class UsrEditForm(forms.Form):
    username = forms.CharField(label='Username:', required=True)
    email = forms.EmailField(label='Email:', required=True)
    lang = forms.ModelChoiceField(label='Language:', required=True, queryset=Language.objects.all())

class CarRentChangeForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('rented_by',)

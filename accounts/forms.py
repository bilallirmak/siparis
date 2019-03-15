from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
# from .backend import EmailBackend
# from django.core.validators import validate_email
# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend
User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler Eşleşmiyor")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
    email = forms.EmailField()




class LoginForm(forms.Form):

    username = forms.CharField(max_length=100,label='',
                                   widget=forms.TextInput(
                                       attrs={'placeholder': 'Kullanıcı Adı ya da E-Posta'}
                                   ))
    password = forms.CharField(max_length=100, label='',
                                   widget=forms.PasswordInput(
                                       attrs={'placeholder': 'Şifre'}
                                   ))




    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            try:
                user = authenticate(username=username, password=password)
            except User.DoesNotExist:
                raise forms.ValidationError("Kullanıcı Adını veya Şifreyi Yanlış Girdiniz!")

            if not user:
                raise forms.ValidationError("Kullanıcı Adını veya Şifreyi Yanlış Girdiniz!")


        return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # username = forms.CharField(max_length=254, label='Kullanıcı Adı')
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifre(Tekrar)', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', "last_name", 'email',)
        # fields['username'].widget.attrs({'placeholder': 'Kullanıcı Adı'})

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler Eşleşmiyor")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False
        if commit:
            user.save()
        return user





# class RegisterForm(forms.ModelForm):
#     username = forms.CharField(max_length=254,label='Kullanıcı Adı')
#     first_name = forms.CharField(max_length=254,label='Ad')
#     last_name = forms.CharField(max_length=254,label='Soyad')
#
#     password1 = forms.CharField(max_length=100, label='Şifre',widget=forms.PasswordInput)
#     password2= forms.CharField(max_length=100, label='Şifre Doğrulama',widget=forms.PasswordInput)
#     email = forms.EmailField(max_length = 254,widget=forms.EmailInput)
#
#
#
#     class Meta:
#
#         model = User
#
#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#             'password1',
#             'password2',
#             'email',
#             ]
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Şifreler Eşleşmiyor')
#         return password2

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #
    #     if validate_email(email):
    #         email=True
    #     else:
    #         email=False
    #
    #     return email








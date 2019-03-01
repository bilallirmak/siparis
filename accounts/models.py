from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, full_name=None,  password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Bir e-mail adresi olmalı")
        if not password:
            raise ValueError("Bir şifre olmalı")

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            username=username,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username=None, full_name=None, password=None):
        user = self.create_user(
            email,
            username=username,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user
    def create_superuser(self, email, username=None, full_name=None, password=None):
        user = self.create_user(
            email,
            username=username,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tam isim")
    username = models.CharField(max_length=254, verbose_name='Kullanıcı Adı', null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=254, verbose_name='Ad', null=True,blank=True)
    last_name = models.CharField(max_length=254, verbose_name='Soyad', null=True,blank=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff user
    admin = models.BooleanField(default=False) #superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm = models.BooleanField(default=False)
    # confirmed_date = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username',] #['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    def get_username(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    @property
    def name(self):
        return self.username

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
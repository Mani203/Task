import datetime
import jwt
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
from session import settings


class UserManager(BaseUserManager):
    def create_user(self, name, password, user_name, mobile=None, email=None):
        user = self.model(name=name, email=self.normalize_email(email), mobile=mobile, user_name=user_name)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, password, mobile, name):
        user = self.model(name=name, mobile=mobile)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    signup_date = models.DateField(auto_now_add=True)
    user_name = models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'user_name'

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.id)

    def __id__(self):
        return self.id

    class Meta:
        db_table = 'student_account'
        managed = True


class StudentData(models.Model):
    student = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    login_datetime = models.DateTimeField(auto_now_add=True)
    logout_datetime = models.DateTimeField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

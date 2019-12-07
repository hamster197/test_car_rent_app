import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



class Language(models.Model):
    lang = models.CharField(verbose_name='Language:', max_length=3, )
    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
    def __str__(self):
        return self.lang

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='fuser', verbose_name='User:', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='flang', verbose_name='Language:', on_delete=models.CASCADE,)
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Car(models.Model):
    user = models.ForeignKey(User, related_name='cuser', verbose_name='User:', on_delete=models.CASCADE)
    rented_by = models.ForeignKey(User, related_name='cruser', verbose_name='Rented by:', on_delete=models.CASCADE,
                                     null=True)
    date_of_manufacture = models.IntegerField(verbose_name='Date of manufacture',
                                              validators=[MinValueValidator(1940),
                                                          MaxValueValidator(datetime.datetime.now().year)])
    creation_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    def __str__(self):
        return str(self.creation_date)

class CarsNames(models.Model):
    car = models.ForeignKey(Car, verbose_name='Car:', related_name='ncar', on_delete=models.CASCADE, null=True)
    lang = models.ForeignKey(Language, verbose_name='Language', related_name='clang', on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name='Name of car', max_length=50)

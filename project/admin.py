from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from project.models import UserProfile, Language, Car, CarsNames


class CarsNameAdmin(admin.StackedInline):
    model = CarsNames

class CarsAdmin(admin.ModelAdmin):
    inlines = [CarsNameAdmin]
    list_display = ('user', 'rented_by', 'date_of_manufacture','creation_date',)
    list_filter = ['user']

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class UserAdmin(UserAdmin):
    inlines = (UserInline, )




admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Language)
admin.site.register(Car, CarsAdmin)
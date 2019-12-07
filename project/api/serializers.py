from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from project.models import UserProfile, CarsNames, Language


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, required=True,)
    language = serializers.ChoiceField(required=True, choices=Language.objects.all())

class UserEditSerializer(serializers.Serializer):
    old_email = serializers.EmailField(
        required=True,
    )
    new_email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(min_length=8, required=True,)
    language = serializers.ChoiceField(required=True, choices=Language.objects.all())

class UsersProfileSerializer(serializers.ModelSerializer, ):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    language = serializers.CharField(source='language.lang')
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'language')

class CarsSerializer(serializers.ModelSerializer, ):
    creation_date = serializers.CharField(source='car.creation_date')
    class Meta:
        model = CarsNames
        fields = ('creation_date', 'name',)
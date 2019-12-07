
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from project.api.serializers import *
from project.models import UserProfile, CarsNames, Language

class UserCreate(generics.CreateAPIView):
    """
       Not Obtain Authorization Token
       ---
       parameters:
            - name: email
              type: string
            - name: password
              type: string
            - name: username
              type: string
            - name: language
              type: choices
              enum: ['rus', 'eng',]
        responseMessages:
            - code: 200
              message: HTTP_200_OK
            - code: 400
              message: HTTP_400_BAD_REQUEST
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        """
           Create User
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        language = serializer.validated_data['language']
        user = User.objects.create(username=username, email=email)
        user.save()
        user.set_password(password)
        user.save()
        userprofile = UserProfile.objects.create(user=user, language=language)
        userprofile.save()
        return Response(status=status.HTTP_200_OK)


class UserEdit(generics.CreateAPIView):
    """
       Obtain Authorization Token
       ---
       parameters:
            - name: old_email
              type: string
            - name: new_email
              type: string
            - name: password
              type: string
            - name: username
              type: string
            - name: language
              type: choices
              enum: ['rus', 'eng',]
        responseMessages:
            - code: 200
              message: HTTP_200_OK
            - code: 400
              message: HTTP_400_BAD_REQUEST
            - code: 401
              message: HTTP_401_UNAUTHORIZED
    """
    serializer_class = UserEditSerializer

    def post(self, request):
        """
           Save the changed user data
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        old_email = serializer.validated_data['old_email']
        new_email = serializer.validated_data['new_email']
        password = serializer.validated_data['password']
        language = serializer.validated_data['language']
        user = get_object_or_404(User, email=old_email)
        user.username = username
        user.email = new_email
        user.save()
        user.set_password(password)
        user.save()
        usprofile = get_object_or_404(UserProfile, user=user)
        usprofile.language = language
        usprofile.save()
        return Response(status=status.HTTP_200_OK)

class UsersListView(generics.ListAPIView,):
    """
       Obtain Authorization Token
       ---
        responseMessages:
            - code: 200
              message: HTTP_200_OK
            - code: 400
              message: HTTP_400_BAD_REQUEST
            - code: 401
              message: HTTP_401_UNAUTHORIZED
    """
    queryset = UserProfile.objects.all()
    serializer_class = UsersProfileSerializer

class CarListView(generics.ListAPIView,):
    """
       Obtain Authorization Token
       ---
        responseMessages:
            - code: 200
              message: HTTP_200_OK
            - code: 400
              message: HTTP_400_BAD_REQUEST
            - code: 401
              message: HTTP_401_UNAUTHORIZED
    """
    serializer_class = CarsSerializer

    def get_queryset(self):
        """
           Get all the cars an authorized user
        """
        lang_usr = get_object_or_404(UserProfile, user=self.request.user).language
        lang = get_object_or_404(Language, lang=lang_usr)
        return CarsNames.objects.filter(lang=lang, car__user=self.request.user)




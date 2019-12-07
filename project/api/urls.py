from django.urls import path

from project.api.views import *

app_name = 'project_api'
urlpatterns = [
    path('users/add/', UserCreate.as_view(), name="user_create"),
    path('users/edit/', UserEdit.as_view(), name="user_edit"),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('cars/', CarListView.as_view(), name='cars_list'),
]


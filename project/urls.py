
from django.urls import path, include

from project.views import *

app_name = 'project'
urlpatterns = [
    path('', AboutView, name='About'),
    path('cars/index/', AllCarsView, name='Cars_index'),
    path('cars/change_rent/<idd>/', ChangeRentView, name='Cars_Change_Rent'),
    path('signup/', SignUpView, name='SignUp'),
    path('api/', include('project.api.urls', namespace='api')),
]

import json
from datetime import datetime

from django import test


from django.test import Client
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework.test import RequestsClient


from project.models import Car, Language, UserProfile, CarsNames

client = RequestsClient()

class URLTests(test.TestCase,):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'email': '1@ya.ru',
            'password': 'secret',
            }
        self.url = 'http://127.0.0.1:8000/'
        User.objects.create_user(**self.credentials)
        Language.objects.create(lang='rus')
        UserProfile.objects.create(user=User.objects.all().first(),
                                   language=Language.objects.all().first())
        Car.objects.create(user=User.objects.all().first(), date_of_manufacture=1978)
        CarsNames.objects.create(car=Car.objects.all().first(), lang=Language.objects.all().first(),
                                 name='Test car')

    def test_SignUpPage(self):
        response = self.client.get(reverse('project:SignUp'),)
        self.assertEqual(response.status_code, 200)

    def test_LoginPage(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        c = Client()
        response = c.post('/accounts/login/', data={'email': self.credentials['email'],
                                                    'password': self.credentials['password'],})
        self.assertEqual(response.status_code, 200)

    def test_HomePage(self):
        response = self.client.get(reverse('project:About'), self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('project:About'),)
        self.assertEqual(response.status_code, 302)

    def test_CarsIndexPage(self):
        response = self.client.get(reverse('project:Cars_index'), self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('project:Cars_index'),)
        self.assertEqual(response.status_code, 302)


    def test_CarsRentPage(self):
        usr = get_object_or_404(User, email=self.credentials['email'])
        self.credentials = {
            'user': usr,
            'date_of_manufacture':datetime.now().year
        }
        Car.objects.create(**self.credentials)
        url = reverse('project:Cars_Change_Rent', args=(Car.objects.all().first().pk,))
        response = self.client.get(url, self.credentials, follow=True,)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)



    def test_ApiSignupAndReceiveToken(self):
        response = client.post(self.url+'auth/token/login/', json={
            'username': self.credentials['username'],
            'password': self.credentials['password'],
        },)
        self.assertEqual(response.status_code, 200)

    def test_ApiSignIn(self):
        response = client.post(self.url + 'api/users/add/', json={
            'username': 'apiusr',
            'email': 'api@ya.ru',
            'password': 'testapi1978',
            'language': Language.objects.first().lang,
        },)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_object_or_404(User, username='apiusr').email, 'api@ya.ru')
        self.assertEqual(str(get_object_or_404(UserProfile, user__username='apiusr').language),
            Language.objects.first().lang)

    def test_ApiChangeUserAccauntData(self):
        response = client.post(self.url + 'auth/token/login/', json={
            'username': self.credentials['username'],
            'password': self.credentials['password'],
        }, )
        response_acc = client.post(self.url + 'api/users/edit/', json={
            'username': 'newtestuser',
            'old_email': '1@ya.ru',
            'new_email': 'newapi@ya.ru',
            'password': 'test2018',
            'language': 'rus',
        }, headers={'Authorization': 'Token ' + response.json()['auth_token']},)
        response_acc_uath = client.post(self.url + 'api/users/edit/', json={
            'username': 'newtestuser',
            'old_email': '1@ya.ru',
            'new_email': 'newapi@ya.ru',
            'password': 'test2018',
            'language': 'rus',
        })
        user = get_object_or_404(User, email='newapi@ya.ru')
        self.assertEqual(response_acc.status_code, 200)
        self.assertEqual(response_acc_uath.status_code, 401)
        self.assertEqual(user.username, 'newtestuser')
        self.assertEqual(str(get_object_or_404(UserProfile, user=user).language), 'rus')


    def test_ApiGetAllUsers(self):
        response = client.post(self.url + 'auth/token/login/', json={
            'username': self.credentials['username'],
            'password': self.credentials['password'],
        }, )
        response_all_users = client.get(self.url + 'api/users/',
                                        headers={'Authorization': 'Token ' + response.json()['auth_token']})
        response_all_users_unath = client.get(self.url + 'api/users/')
        self.assertEqual(response_all_users.status_code, 200)
        self.assertEqual(response_all_users_unath.status_code, 401)
        self.assertEqual(len(json.loads(response_all_users.content)), User.objects.all().count())
        self.assertEqual(json.loads(response_all_users.content)[0]['username'], User.objects.all().first().username)


    def test_ApiGetAllUserCars(self):
        response = client.post(self.url + 'auth/token/login/', json={
            'username': self.credentials['username'],
            'password': self.credentials['password'],
        }, )
        response_all_cars = client.get(self.url + 'api/cars/',
                                        headers={'Authorization': 'Token ' + response.json()['auth_token']})
        response_all_cars_unath = client.get(self.url + 'api/cars/')
        self.assertEqual(response_all_cars.status_code, 200)
        self.assertEqual(response_all_cars_unath.status_code, 401)
        self.assertEqual(len(json.loads(response_all_cars.content)), CarsNames.objects.all().count())
        self.assertEqual(json.loads(response_all_cars.content)[0]['name'], CarsNames.objects.all().first().name)
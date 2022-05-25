from asyncio import Task
from audioop import reverse
from contextvars import Token

from django.contrib.auth.hashers import make_password
from django.db.backends.base import client
from django.test import Client
from django.test import Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase
from rest_framework import status
from rest_framework.utils import json

from scheduler.models import Event
from users.models import Resource


class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class ViewDashboardTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', password='test_user')
        self.client.login(username='test_user', password='test_user')

    def test_login(self):
        self.user = authenticate(username='test_user', password='test_user')

    def test_index(self):
        self.client.login(username='test_user', password='test_user')
        response = self.client.get('https://the-workforce.herokuapp.com/scheduler/calender/')
        self.assertEqual(response.status_code, 200)


class AuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.is_active = False
        self.user.save()

    def test_correct(self):
        check = User.objects.get(username='test')
        self.assertEqual(check.is_active, 0)


class APIClient:
    pass


class LogoutTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', password='test_user')
        self.client.login(username='test_user', password='123')

    def test_logout(self):
        self.client.logout()



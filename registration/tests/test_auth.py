from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clubbisenes.models import ShiftUser, UserProfileModel
from django.contrib.auth.models import Group


class TestAuth(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

    def setUp(self):
        test_user = User.objects.create_user(
            username='test_user',
            password='12345',
        )

    def test_auth_get(self):
        response = self.client.get('/reg/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/authtification.html')

    def test_auth_post(self):
        response = self.client.post('/reg/login/', data={
            'username': 'test_user',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('/reg/changeTable/')

    def test_auth_post_table(self):
        test_user1 = User.objects.create_user(
            username='test_user1',
            password='12345',
        )
        profile = UserProfileModel.objects.create(
            user=test_user1,
            table=23
        )

        response = self.client.post('/reg/login/', data={
            'username': 'test_user1',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('/')

    def test_auth_post_no_table(self):
        test_user1 = User.objects.create_user(
            username='test_user1',
            password='12345',
        )
        response = self.client.post('/reg/login/', data={
            'username': 'test_user1',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('/reg/changeTable/')


class TestRegistration(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

    def test_reg_get(self):
        response = self.client.get('/reg/reg/')
        self.assertTemplateUsed('registration/registration.html')

    def test_reg_post(self):
        user_group = Group.objects.create(
            name='clients'
        )
        response = self.client.post(reverse('regist'), data={
            'username': 'otto',
            'phone': '+7(903)0900909',
            'password': 'Ww123456',
            'password2': 'Ww123456'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('/reg/changeTable/')


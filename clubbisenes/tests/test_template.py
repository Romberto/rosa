from django.contrib.auth.models import User, Group

from django.test import TestCase

from clubbisenes.models import ShiftUser, UserProfileModel, ShiftUser


class TestTemplates(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

    def setUp(self):
        test_cachier = User.objects.create_user(username='test_cashier',
                                                password='12345')
        cashier_group = Group.objects.create(
            name='cachers'
        )
        test_cachier.groups.add(cashier_group)

        test_dj = User.objects.create_user(username='dj',
                                           password='12345')
        dj_group = Group.objects.create(
            name='djs'
        )
        test_dj.groups.add(dj_group)

        test_user = User.objects.create_user(
            username='test_user',
            password='12345',
        )
        user_group = Group.objects.create(
            name='clients'
        )
        test_user.groups.add(user_group)

        test_profile = UserProfileModel.objects.create(
            user=test_user,
            table=5
        )

    def test_index(self):
        self.client.login(username="test_user", password="12345")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test_user')
        self.assertTemplateUsed(response, 'clubbisenes/index.html')
        self.client.logout()

    def test_cashier(self):
        self.client.login(username="test_cashier", password="12345")
        response = self.client.get('/cashier/')
        self.assertEqual(str(response.context['user']), 'test_cashier')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubbisenes/cashier.html')
        self.client.logout()

    def test_dj(self):
        self.client.login(username="dj", password="12345")
        response = self.client.get('/dj/')
        self.assertEqual(str(response.context['user']), 'dj')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubbisenes/dj.html')
        self.client.logout()





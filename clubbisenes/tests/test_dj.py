from django.contrib.auth.models import User, Group
from django.test import TestCase

from clubbisenes.models import ShiftUser, Sounds, UserProfileModel, SoundStatus


class TestModerationSound(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

        STATUS = ['pay', 'wait_moder', 'wait_pay', 'post', 'no_moder']
        for status in STATUS:
            cls.status = SoundStatus.objects.create(
                statusName=status
            )

    def setUp(self):
        test_dj = User.objects.create_user(username='dj',
                                           password='12345')
        dj_group = Group.objects.create(
            name='djs'
        )
        test_dj.groups.add(dj_group)

        test_user = User.objects.create_user(
            username='test_user',
            password='Ww12345',
        )
        test_profile = UserProfileModel.objects.create(
            user=test_user,
            table=5
        )

        sound = Sounds.objects.create(
            user=test_user,
            name='assa'
        )

    def test_moderanion_get(self):
        sound = Sounds.objects.get(name='assa')
        pk = str(sound.id)
        req = '/dj/' + pk
        self.client.login(username='dj', password='12345')

        response = self.client.get(req)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubbisenes/product.html')

    def test_moderation_post_Yes(self):
        sound = Sounds.objects.get(name='assa')
        pk = str(sound.id)
        req = '/dj/' + pk
        response = self.client.post(req, data={
            'mod': 'Y'
        })
        sound = Sounds.objects.get(name='assa')
        self.assertEqual(sound.status.id, 3)


    def test_moderation_post_No(self):
        sound = Sounds.objects.get(name='assa')
        pk = str(sound.id)
        req = '/dj/' + pk
        response = self.client.post(req, data={
            'mod': 'N'
        })
        sound = Sounds.objects.get(name='assa')
        self.assertEqual(sound.status.id, 5)



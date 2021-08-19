from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from clubbisenes.models import ShiftUser, UserProfileModel, SoundStatus, Sounds


class PermitionRedirect(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

    def test_per_dj(self):
        response = self.client.get('/dj/')
        self.assertRedirects(response, '/test', target_status_code=301)

    def test_per(self):
        response = self.client.get('/cashier/')
        self.assertRedirects(response, '/test', target_status_code=301)

    def test_main(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/reg/login/')


    def test_dj_int(self):
        response = self.client.get('/dj/3')
        self.assertRedirects(response, '/test', target_status_code=301)

    def test_sound(self):
        response = self.client.get('/sound/')
        self.assertRedirects(response, '/reg/login/')


class TestSound(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            password='Ww123456'
        )
        test_profile = UserProfileModel.objects.create(
            user=self.test_user,
            table=5
        )

        for status in range(3):
            self.status = SoundStatus.objects.create(
                statusName=status
            )

        self.countSounds = Sounds.objects.count()

    def test_sound_created(self):
        self.client.login(username='test_user', password='Ww123456')

        file = SimpleUploadedFile('foto.png', content=open('clubbisenes/tests/foto.png',
                                                           'rb').read(), content_type="image")
        response = self.client.post('/sound/', data={'name': "new",
                                                     'file': file})

        new_sound = Sounds.objects.get(name='new')

        new_count = Sounds.objects.count() - 1
        self.assertEqual(self.countSounds, new_count)
        self.assertEqual(new_sound.status.id, 2)
        self.assertRedirects(response, '/auth', target_status_code=301)
        self.client.logout()


class TestSoundGet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

    def setUp(self):
        test_user1 = User.objects.create_user(username='test_user',
                                              password='Ww123456')
        pro = UserProfileModel.objects.create(
            user=test_user1,
            table=17
        )

    def test_sound_get(self):
        self.client.login(username='test_user', password='Ww123456')
        response = self.client.get('/sound/')
        # self.assertEqual(str(response.context['user']), 'test_user')
        self.assertTemplateUsed(response, 'clubbisenes/sound.html')
        user = User.objects.get(username='test_user')
        self.assertEqual(user.profile.get().table, 17)




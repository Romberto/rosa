from django.contrib.auth.models import User, Group
from django.test import TestCase
from clubbisenes.models import ShiftUser, SoundStatus, UserProfileModel, Sounds


class TestCasheir(TestCase):
    ITER_COUNT = 17

    @classmethod
    def setUpTestData(cls):
        cls.test_shift = ShiftUser()
        cls.test_shift.state = True
        cls.test_shift.save()

        STATUS = ['pay', 'wait_moder', 'wait_pay', 'post', 'no_moder']
        for status in STATUS:
            status = SoundStatus.objects.create(
                statusName=status
            )
        cls.gr_users = Group.objects.create(
            name="clients"
        )
        user = User.objects.create_user(username='user1r', password="Ww123456")
        profile = UserProfileModel.objects.create(
            user=user,
            table=5
        )
        user.groups.add(cls.gr_users)
        sound_st = SoundStatus.objects.get(id=3)
        sound = Sounds.objects.create(
            user=user,
            name='asssa',
            status=sound_st
        )

        for item in range(cls.ITER_COUNT):
            user = User.objects.create_user(username='user' + str(item), password="Ww123456")
            profile = UserProfileModel.objects.create(
                user=user,
                table=item
            )
            user.groups.add(cls.gr_users)
            sound_st = SoundStatus.objects.get(id=3)
            sound = Sounds.objects.create(
                user=user,
                name='asssa' + str(item),
                status=sound_st
            )
        gr_cashiers = Group.objects.create(
            name="cachers"
        )
        user_cashier = User.objects.create_user(username='kassa', password='Ww123456')
        user_cashier.groups.add(gr_cashiers)

    #      TestGet не зарегистрированный пользователь

    def test_cashier_get(self):
        response = self.client.get('/cashier/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/test')

    #      TestGet залогиненный кассир

    def test_cashier_get_auth(self):
        self.client.login(username='kassa', password='Ww123456')
        response = self.client.get('/cashier/')
        self.assertEqual(response.context['user'].username, 'kassa')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubbisenes/cashier.html')
        self.assertEqual(response.context['wait_pay'].count(), self.ITER_COUNT + 1)  # песни ожидающие оплату
        self.assertEqual(len(response.context['table_list']), self.ITER_COUNT)  # длинна списка активных столов

    def test_cashier_post(self):
        self.client.login(username='kassa', password='Ww123456')
        response = self.client.post('/cashier/', data={
            'pay': '2'
        })
        sound = Sounds.objects.get(id=2)
        self.assertEqual(sound.status.statusName, 'pay')
        self.assertRedirects(response, '/cashier', target_status_code=301)

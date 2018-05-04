from django.test import TestCase
from django.contrib.auth.models import User
from unitedcp.models import UserProfile


class RegisterTest(TestCase):

    def setUp(self):
        User.objects.create_user('tata12', 'tata@mail.ru', 'tata@11')

    def user_profile_created(self):

        user_profile = UserProfile.objects.get(user__username='tata12')
        self.assertEqual(user_profile.user.username, 'tata12')

from pprint import pp
from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from cloudinary.uploader import upload_image
import django.contrib.auth.views as auth_views


from .models import Profile
from . import views
from data import departments, years


class UserTestCase(TransactionTestCase):
    
    def setUp(self) -> None:
        # create fake user; from project's User model
        self.user_info = {
            'username': 'user-test1',
            'email': 'test1@test.com',
            'password': 'ekrlw32rlwr',
        }
        self.user = get_user_model().objects.create_user( **self.user_info)
        # verify the user: 
        self.user.status.verified = True
        self.user.status.save()


class ProfileTestCase(UserTestCase):
    '''
    Test case for `Profile` model.
    '''

    def test_auto_create_profile(self):
        # try to get the user's profile
        self.assertTrue(hasattr(self.user, 'profile'))
        profile = Profile.objects.get(user__username=self.user_info['username'])
        self.assertEqual(self.user.profile, profile)

        self.assertEqual(profile.profile_pic.url + '.png', Profile._meta.get_field('profile_pic').get_default())
        self.assertEqual(profile.language, Profile._meta.get_field('language').get_default())
        self.assertEqual(profile.theme, Profile._meta.get_field('theme').get_default())
        self.assertEqual(profile.major, None)
        self.assertEqual(profile.year, None)
        
    def test_crud_prfile(self):
        # Note User:Profile is 1:1 relationship
        # user cannot create profile without a User object

        # create another user
        new_user = get_user_model().objects.create_user(
            username = 'sad-orea',
            email='sdaf@asd.xom',
            password='dsfergvfd',
        )

        # try add another profile to new_user: it should have one already
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user = new_user)

        Profile.objects.filter(user__username='sad-orea').exists()
        self.assertTrue(Profile.objects.filter(user__username='sad-orea').exists())
        profile = Profile.objects.get(user__username='sad-orea')
        
        # delete the user object; will also delete its profile object
        profile.user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Profile.objects.get(user__username='sad-orea')

        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(username='sad-orea')
        
        
        # update profile
        origin_img_url = 'https://res.cloudinary.com/petroly-initiative/image/upload/v1622359053/profile_pics/blank_profile.png'
        res = upload_image(
            origin_img_url,
            folder="profile_pics/test/",
            public_id=self.user.username,
            overwrite=True,
            invalidate=True,
            transformation=[{"width": 200, "height": 200, "crop": "fill"}],
            format="jpg",
        )

        self.user.profile.profile_pic = res
        self.user.profile.major = departments[7][0]
        self.user.profile.year = years[2][0]
        self.user.profile.language = 'ar-SA'
        self.user.profile.theme = 'dark'
        self.user.profile.save()

        self.assertEqual(self.user.profile.profile_pic.public_id, f'profile_pics/test/{self.user.username}')
        self.assertEqual(self.user.profile.profile_pic.metadata['original_filename'], 'blank_profile')
        self.assertEqual(self.user.profile.profile_pic.metadata['width'], 200)
        self.assertEqual(self.user.profile.profile_pic.metadata['format'], 'jpg')
        self.assertEqual(self.user.profile.major, departments[7][0])
        self.assertEqual(self.user.profile.year, years[2][0])
        self.assertEqual(self.user.profile.language, 'ar-SA')
        self.assertEqual(self.user.profile.theme, 'dark')



class AccountViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # create fake user
        cls.user = get_user_model().objects.create_user(
            username = 'freshman',
            email = 'sadness@kfupm.com',
            password = 'stay-strong',
        )
        cls.admin = get_user_model().objects.create_user(
            username = 'senior',
            email = 'happieness@kfupm.com',
            password = 'stay-whatsoever',
            is_staff = True,
        )

    def test_forbidden_user(self):
        # non admin user cannot open any page
        # except the login page
        res = self.client.get('/account/login/', follow=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.wsgi_request.path, '/account/login/')
        self.assertTemplateUsed(res, 'registration/login.html')
        self.assertEqual(res.resolver_match.func.__name__, auth_views.LoginView.as_view().__name__)

        # login with wrong credientials user
        res = self.client.post(
            '/account/login/', follow=True, 
            data={'username':'blah', 'password':'im tired writing tests'}
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/login.html')

        # login a non-staff user
        res = self.client.post(
            '/account/login/', follow=True, 
            data={'username':'freshman', 'password':'stay-strong'}
        )
        self.assertEqual(res.status_code, 403)  # not allowed
        self.assertEqual(res.wsgi_request.path, '/account/')
        self.assertEqual(res.resolver_match.func.__name__, views.IndexView.as_view().__name__)

        # logout this user
        res = self.client.post('/account/logout/', follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.wsgi_request.path, '/account/logout/')
        self.assertEqual(res.resolver_match.func.__name__, auth_views.LogoutView.as_view().__name__)


    def test_staff_user(self):
        # login a staff user
        res = self.client.post(
            '/account/login/', follow=True, 
            data={'username':'senior', 'password':'stay-whatsoever'}
        )
        
        self.assertEqual(res.status_code, 200)  # allowed
        self.assertEqual(res.wsgi_request.path, '/account/')
        self.assertEqual(res.resolver_match.func.__name__, views.IndexView.as_view().__name__)
        
        # logout this user
        res = self.client.post('/account/logout/', follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.wsgi_request.path, '/account/logout/')
        self.assertEqual(res.resolver_match.func.__name__, auth_views.LogoutView.as_view().__name__)

        

class UserRegisterTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()

    

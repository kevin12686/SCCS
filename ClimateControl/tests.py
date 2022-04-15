from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

user = get_user_model()


# Create your tests here.

class LoginTest(TestCase):
    def setUp(self) -> None:
        self.test_user = user.objects.create_user(username='ABC12345', is_admin=True, password='@123ABCdef')
        self.client = Client()

    def tearDown(self) -> None:
        self.test_user.delete()

    def test_login_success(self):
        resp = self.client.post('/login/', {'username': 'ABC12345', 'password': '@123ABCdef'})
        self.assertRedirects(resp, settings.LOGIN_REDIRECT_URL)

    def test_incorrect_username(self):
        resp = self.client.post('/login/', {'username': 'NULL', 'password': '@123ABCdef'})
        self.assertFormError(resp, 'form', 'username', ['Username is incorrect.'])

    def test_nonexist_username(self):
        resp = self.client.post('/login/', {'username': 'NOTEXISTED', 'password': '@123ABCdef'})
        self.assertFormError(resp, 'form', None, [
            'Please enter a correct username and password. Note that both fields may be case-sensitive.'])

    def test_incorrect_password1(self):
        resp = self.client.post('/login/', {'username': 'ABC12345', 'password': 'abcd'})
        self.assertFormError(resp, 'form', None, [
            'Please enter a correct username and password. Note that both fields may be case-sensitive.'])

    def test_incorrect_password2(self):
        resp = self.client.post('/login/', {'username': 'ABC12345', 'password': 'P@SSw0rd'})
        self.assertFormError(resp, 'form', None, [
            'Please enter a correct username and password. Note that both fields may be case-sensitive.'])


class PasswordResetTest(TestCase):
    def setUp(self) -> None:
        self.test_user = user.objects.create_user(username='ABC12345', is_admin=True, password='@123ABCdef')
        self.client = Client()
        self.client.login(username='ABC12345', password='@123ABCdef')

    def tearDown(self) -> None:
        self.test_user.delete()

    def test_password_reset_success(self):
        resp = self.client.post('/reset/', {'old_password': '@123ABCdef', 'new_password1': '@123XYZdef'})
        self.assertRedirects(resp, reverse_lazy('Index'))

    def test_oldpassword_incorrect1(self):
        resp = self.client.post('/reset/', {'old_password': 'ERR', 'new_password1': '@123ABCdef'})
        self.assertFormError(resp, 'form', 'old_password',
                             ['Your old password was entered incorrectly. Please enter it again.'])

    def test_oldpassword_incorrect2(self):
        resp = self.client.post('/reset/', {'old_password': 'Wr0ngP@ss', 'new_password1': '@123ABCdef'})
        self.assertFormError(resp, 'form', 'old_password',
                             ['Your old password was entered incorrectly. Please enter it again.'])

    def test_newpassword_incorrect(self):
        resp = self.client.post('/reset/', {'old_password': '@123ABCdef', 'new_password1': 'abcd'})
        self.assertFormError(resp, 'form', 'new_password1',
                             ['This password is too short. It must contain at least 8 characters.',
                              'This password must contain at least a symbol.'])


class CreateAccount(TestCase):
    def setUp(self) -> None:
        self.test_user = user.objects.create_user(username='ABC12345', is_admin=True, password='@123ABCdef')
        self.client = Client()

    def tearDown(self) -> None:
        self.test_user.delete()

    def test_account_created(self):
        resp = self.client.post('/user/create/', {'username': 'ABC12346', 'password': '@123ABCdef'})
        self.assertRedirects(resp, '/user/')

    def test_null_username(self):
        resp = self.client.post('/user/create/', {'username': '', 'password': '@123ABCdef'})
        self.assertFormError(resp, 'form', 'username', ['This field is required.'])

    def test_existing_username(self):
        resp = self.client.post('/user/create/', {'username': 'ABC12345', 'password': '@123ABCdef'})
        self.assertFormError(resp, 'form', 'username', ['A user with that username already exists.'])

    def test_incorrect_password(self):
        resp = self.client.post('/user/create/', {'username': 'ABC12346', 'password1': 'abcd'})
        self.assertFormError(resp, 'form', 'password', ['This field is required.'])

    def test_null_password(self):
        resp = self.client.post('/user/create/', {'username': 'ABC12346', 'password1': ''})
        self.assertFormError(resp, 'form', 'password', ['This field is required.'])

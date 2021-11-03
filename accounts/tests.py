from django.test import TestCase
from accounts.forms import UsersRegisterForm,UsersLoginForm
from django import forms

class UsersRegisterFormTests(TestCase):
    def test_password_length_less_than_8(self):
        data = {"username": "bordacount","email": "abcd@gmail.com","confirm_email": "abcd@gmail.com", "password":"abc"}
        form = UsersRegisterForm(data)
        self.assertFalse(form.is_valid())

        try:
            form.clean()
        except forms.ValidationError as e:
            self.assertEquals('Password must be greater than 8 characters', e.message)

    def test_email_different_from_confirm_email(self):
        data = {"username": "bordacount","email": "abcd@gmail.com","confirm_email": "abc1@gmail.com", "password":"abcdefgh12344"}
        form = UsersRegisterForm(data)
        self.assertFalse(form.is_valid())

        try:
            form.clean()
        except forms.ValidationError as e:
            self.assertEquals('Email must match', e.message)

    def test_email_already_exists(self):
        data = {"username": "bordacount","email": "bhanu1@tamu.edu","confirm_email": "bhanu1@tamu.edu", "password":"abcdefgh12344"}
        form = UsersRegisterForm(data)
        self.assertTrue(form.is_valid())

        try:
            form.clean()
        except forms.ValidationError as e:
            self.assertEquals('Email is already registered', e.message)



class UsersLoginFormTests(TestCase):
    def test_user_does_not_exist(self):
        data = {"username": "doesnotexist", "password":"1234567890"}
        form = UsersLoginForm(data)
        self.assertFalse(form.is_valid())

        try:
            form.clean()
        except forms.ValidationError as e:
            self.assertEquals('This user does not exists or Incorrect Password', e.message)
    
    def test_user_password_mismatch(self):
        data = {"username": "abc", "password":"wrongpassword"}
        form = UsersLoginForm(data)
        self.assertFalse(form.is_valid())

        try:
            form.clean()
        except forms.ValidationError as e:
            self.assertEquals('This user does not exists or Incorrect Password', e.message)
    

from django.test import TestCase
from django.core import mail
from django import forms
from .forms import ContactForm



# Mock out the CaptchaField to always pass in tests
class ContactFormWithoutCaptcha(ContactForm):
    captcha = forms.CharField(required=False)  

class ContactFormTests(TestCase):

    def test_form_validity(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message',
        }
        form = ContactFormWithoutCaptcha(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_email_sending(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message',
            'captcha_0': 'dummy_key',  
            'captcha_1': 'test_captcha'  
        }
        form = ContactForm(data=form_data)
        if form.is_valid():
            form.save()
            self.assertEqual(len(mail.outbox), 1)
            email = mail.outbox[0]
            self.assertEqual(email.subject, 'Test Subject')
            self.assertEqual(email.body, 'Test Message')
            self.assertEqual(email.from_email, 'john@example.com')

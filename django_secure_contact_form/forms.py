from django import forms
from .models import ContactMessage
from captcha.fields import CaptchaField

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'captcha']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your message'}),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message',
        }
        error_messages = {
            'name': {'required': 'Please enter your name.'},
            'email': {'required': 'Please enter your email address.'},
            'subject': {'required': 'Please enter the subject.'},
            'message': {'required': 'Please enter your message.'},
        }


from django import forms
from .models import ContactMessage

class CustomContactForm(ContactForm):
    custom_field = forms.CharField(required=False)

    class Meta(ContactForm.Meta):
        fields = ContactForm.Meta.fields + ['custom_field']

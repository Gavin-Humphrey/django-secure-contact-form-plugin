import time
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.signing import Signer, BadSignature
from .models import ContactMessage
from captcha.fields import CaptchaField


def get_plugin_config():
    """Helper to fetch config dictionary with fallback defaults."""
    default_config = {
        'HONEYPOT_ENABLED': True,
        'TIME_GUARD_ENABLED': True,
        'MIN_SUBMISSION_TIME': 3,
        'CAPTCHA_ENABLED': True,
    }
    user_config = getattr(settings, 'SECURE_CONTACT_FORM', {})
    return {**default_config, **user_config}


class ContactForm(forms.ModelForm):
    # 1. Honeypot Field
    hp_website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'style': 'display:none !important;',
                'tabindex': '-1',
                'autocomplete': 'off',
            }
        ),
        label='',
    )

    # 2. Time-Based Submission Guard
    form_rendered_at = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Your message'}
            ),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = get_plugin_config()

        # Dynamically attach CaptchaField if CAPTCHA_ENABLED is True
        if self.config.get('CAPTCHA_ENABLED', True):
            self.fields['captcha'] = CaptchaField()

        # Stamp form creation time using Django's Cryptographic Signer
        if self.config.get('TIME_GUARD_ENABLED', True) and not self.is_bound:
            signer = Signer()
            self.fields['form_rendered_at'].initial = signer.sign(str(int(time.time())))

    def clean_hp_website(self):
        """Honeypot validation."""
        if not self.config.get('HONEYPOT_ENABLED', True):
            return ''

        value = self.cleaned_data.get('hp_website')
        if value:
            raise ValidationError("Bot activity detected.")
        return value

    def clean_form_rendered_at(self):
        """Timestamp verification using configurable heuristic threshold."""
        if not self.config.get('TIME_GUARD_ENABLED', True):
            return ''

        value = self.cleaned_data.get('form_rendered_at')
        if not value:
            return value

        signer = Signer()
        min_time = self.config.get('MIN_SUBMISSION_TIME', 3)

        try:
            unsigned_time = signer.unsign(value)
            rendered_timestamp = int(unsigned_time)
            current_timestamp = int(time.time())

            if (current_timestamp - rendered_timestamp) < min_time:
                raise ValidationError("Form submitted too quickly. Please wait a moment.")
        except (BadSignature, ValueError):
            raise ValidationError("Invalid security token.")

        return value
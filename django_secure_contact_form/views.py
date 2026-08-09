from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .forms import ContactForm, get_plugin_config


@csrf_protect
def contact_view(request):
    config = get_plugin_config()

    if request.method == 'POST':
        # Silent Honeypot Drop (if enabled in settings)
        if config.get('HONEYPOT_ENABLED', True) and request.POST.get('hp_website'):
            return redirect('contact_success')

        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                recipient_email = getattr(
                    settings, 
                    'CONTACT_FORM_RECIPIENT_EMAIL', 
                    getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                )

                email = EmailMessage(
                    subject=f"Contact Form: {contact_message.subject}",
                    body=contact_message.message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
                    to=[recipient_email],
                    reply_to=[contact_message.email],
                )

                email.send(fail_silently=False)
                return redirect('contact_success')

            except Exception as e:
                return render(request, 'django_secure_contact_form/contact_form.html', {
                    'form': form,
                    'error_message': f'Error sending email: {str(e)}'
                })
    else:
        form = ContactForm()

    return render(request, 'django_secure_contact_form/contact_form.html', {'form': form})


def contact_success_view(request):
    return render(request, 'django_secure_contact_form/contact_success.html')
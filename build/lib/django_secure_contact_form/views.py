from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactFormSettings
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string


@csrf_protect
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                send_mail(
                    contact_message.subject,
                    contact_message.message,
                    contact_message.email,
                    ['admin@example.com'],
                    fail_silently=False,
                )
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

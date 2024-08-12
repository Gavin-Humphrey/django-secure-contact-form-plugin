# Django Secure Contact Form Plugin

## Overview

The **Django Secure Contact Form** plugin provides a secure and customizable contact form for Django projects. It includes features like CAPTCHA for enhanced security and email notifications.

## Installation

To install the plugin, follow these steps:

1. **Install the Package:**

   You can install the plugin via PyPI using pip:

   ```bash
   pip install django-secure-contact-form

2. **Add the Plugin to Your Django Project:**

Add 'django_secure_contact_form' and 'captcha' to your INSTALLED_APPS in `settings.py`:

````python
    INSTALLED_APPS = [
        # Other installed apps
        'django_secure_contact_form',
        'captcha',
    ]
````

3. **Include URLs:**

In your project's `urls.py`, include the plugin’s URLs:   

    from django.urls import include, path

````python
    urlpatterns = [
        # Other URL patterns
        path('contact/', include('django_secure_contact_form.urls')),
        path('captcha/', include('captcha.urls')),
    ]
````
4. **Apply Migrations:**
    Run the following command to apply the migrations:

    `python manage.py migrate`


## Configuration

### Email Configuration

To use the email features of this plugin, configure Django’s email settings in your `settings.py` file. Here’s an example configuration:
````python
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.example.com'  # Replace with your SMTP server
    EMAIL_PORT = 587  # Common port for TLS
    EMAIL_USE_TLS = True  # Use TLS if required
    EMAIL_HOST_USER = 'your_email@example.com'  # Replace with your email username
    EMAIL_HOST_PASSWORD = 'your_password'  # Replace with your email password
    DEFAULT_FROM_EMAIL = 'webmaster@example.com'  # Replace with your default email address
````

## CAPTCHA Configuration
**Ensure you have the django-simple-captcha library installed and configured:**

1. **Install the Library:**
   ```bash
   pip install django-simple-captcha

2. **Configure CAPTCHA Settings in `settings.py`:**
   ```python
    CAPTCHA_IMAGE_SIZE = (110, 50)  # Set the size to a larger value if needed
    CAPTCHA_FONT_SIZE = 30           # Increase font size for better readability
    CAPTCHA_LETTER_ROTATION = (-30, 30)  # Adjust rotation
    CAPTCHA_BACKGROUND_COLOR = '#ffffff'  # Background color for contrast
    CAPTCHA_NOISE_FUNCTIONS = (
        'captcha.helpers.noise_arcs',
        'captcha.helpers.noise_dots',
    )
    ```

## Customization
### Template Customization
1. **Create a Directory in Your Project’s Templates Folder:**
   
   Create a directory named django_secure_contact_form inside your project's templates folder:

    ```plaintext
        my_project/
            templates/
                django_secure_contact_form/
    ```
2. **Copy Templates:**
   Copy the templates from the plugin’s templates directory to this new directory. For example:
    ```plaintext
   django_secure_contact_form_plugin/
        django_secure_contact_form/
            templates/
                contact_form.html
                contact_success.html
                email_template.html

**Copy these files to:**
````plaintext
my_project/
    templates/
        django_secure_contact_form/
            contact_form.html
            contact_success.html
            email_template.html
````
1. **Modify Templates:**      
   Modify the copied templates as needed to match your project’s design and requirements. The files you’ll find are:

- `contact_form.html`: The contact form page.
- `contact_success.html`: The page displayed after a successful form submission.
- `email_template.html`: The template used for the email notifications. 

## CSS Customization   

1. **Create a CSS File:**
   Create a CSS file in your static directory, e.g., `static/css/styles.css`.


2. **Link the CSS File:**
   Ensure that your contact_form.html links to the CSS file correctly:

    `<link rel="stylesheet" type="text/css" href="{% static 'css/styles.css' %}">`<br>

3. **Edit the CSS File:**
Customize the styles as needed. For example:

 ````css 
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f7f7f7;
}

form {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 0 0.625rem rgba(0, 0, 0, 0.1);
    max-width: 30rem;
    width: 100%;
    margin: 2rem 0;
}

h1 {
    margin-bottom: 1.5rem;
    text-align: center;
}

input[type="text"],
input[type="email"],
textarea {
    width: 100%;
    padding: 0.625rem;
    margin: 0.625rem 0;
    border: 1px solid #cccccc;
    border-radius: 0.25rem;
}

button {
    background-color: #007bff;
    color: #ffffff;
    border: none;
    padding: 0.625rem;
    border-radius: 0.25rem;
    cursor: pointer;
    width: 100%;
}

button:hover {
    background-color: #0056b3;
}

.errors {
    color: red;
    margin: 1rem 0;
}
````
## Usage
1. **Render the Form:**

- To display the contact form, you have two options depending on your use case:

    * **Standard Implementation:**

        If you are using the default ContactForm provided by the plugin and do not require any customization, you can directly import and use it as follows:

        ````python
        from django.shortcuts import render
        from django_secure_contact_form.forms import ContactForm

        def contact_form_view(request):
            form = ContactForm()
            return render(request, 'django_secure_contact_form/contact_form.html', {'form': form})
        ````
        In this case, you do not need to create a custom model or form file. The form will be handled entirely by the plugin.

    * **Customized Form Implementation:**

        If you need to customize the contact form, you can create a custom form that extends the ContactForm provided by the plugin. Here’s how:

        Create a Custom Form Model:

        First, create a model that inherits from ContactMessage, which is provided by the plugin:

        ````python
        from django.db import models
        from django_secure_contact_form.models import ContactMessage

        class CustomContactMessage(ContactMessage):
            custom_field = models.CharField(max_length=100, blank=True, null=True)
        ````
        **Create a Custom Form:**

        Then, create a custom form that extends ContactForm:

        ````python
        from django import forms
        from .models import CustomContactMessage
        from django_secure_contact_form.forms import ContactForm

        class CustomContactForm(ContactForm):
            custom_field = forms.CharField(required=False)

            class Meta(ContactForm.Meta):
                model = CustomContactMessage
                fields = ContactForm.Meta.fields + ['custom_field']
        ````
        **Use the Customized Form:**

        Finally, use your custom form in the view:

        ````python
        from django.shortcuts import render
        from .forms import CustomContactForm

        def contact_form_view(request):
            form = CustomContactForm()
            return render(request, 'django_secure_contact_form/contact_form.html', {'form': form})
        ````
        In this customized implementation, you should import your custom form from the appropriate module (e.g., .forms) and ensure your model inherits from ContactMessage.

    **Summary**
    Standard Implementation: Import ContactForm directly from django_secure_contact_form.forms for a plug-and-play solution.

    Customized Implementation: Extend ContactForm and ContactMessage for additional fields or custom behavior.
    
2. **Handle Form Submission:**

    In your `urls.py`, map the view to a URL:

    ````python
    from django.urls import path
    from .views import contact_form_view

    urlpatterns = [
        path('contact/', contact_form_view, name='contact_form'),
    ]
    ````

## Testing

1. **Run the Development Server:**
````bash
python manage.py runserver
````

2. **Visit the Contact Form Page:**

Open your browser and navigate to `http://127.0.0.1:8000/contact/` to test the contact form.

3. **Check Email Notifications:**

Ensure that the email notifications are sent correctly by submitting the form and verifying the email delivery.

## Troubleshooting
- **Static Files Not Loading:**
Ensure that the static files are correctly collected and served. Run:
````bash
python manage.py collectstatic
````
and ensure that your static files settings in settings.py are configured correctly.

- **Form Not Displaying:**
Verify that the form is being rendered correctly and check for any template or form-related errors.

- **CAPTCHA Issues:**
Ensure that django-simple-captcha is installed and configured properly. Check CAPTCHA settings and make sure the CAPTCHA images are being generated and displayed.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests on the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

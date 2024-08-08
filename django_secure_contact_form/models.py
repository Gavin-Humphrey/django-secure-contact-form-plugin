from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    

class ContactFormSettings(models.Model):
    email_subject_prefix = models.CharField(max_length=100, default='Contact Form Submission')
    # Add other settings as needed

    def __str__(self):
        return "Contact Form Settings"
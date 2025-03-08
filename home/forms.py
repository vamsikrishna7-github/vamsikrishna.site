from django import forms
from .models import ContactMessage
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'title', 'project_type', 'message']
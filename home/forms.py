from django import forms
from .models import ContactMessage, TemplateProducts
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'title', 'project_type', 'message']

class TemplateProductForm(forms.ModelForm):
    class Meta:
        model = TemplateProducts
        fields = ['image_video', 'tech_stack', 'title', 'description', 'preview_url', 'price', 'source', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter product title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter product description'}),
            'preview_url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'source': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter source code iFrame'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tech_stack': forms.TextInput(attrs={'placeholder': 'e.g., Django, React'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
        }
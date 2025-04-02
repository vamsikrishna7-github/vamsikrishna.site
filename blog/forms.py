from django import forms
from .models import NewsletterSubscriber
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import BlogPosts


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['name', 'email']


class BlogPostsForm(forms.ModelForm):
    class Meta:
        model = BlogPosts
        fields = '__all__'
        labels = {
            'title': 'Title',
            'subtitle': 'Subtitle',
            'main_image': 'Main Image',
            'content': 'Content',
            'conclusion_title': 'Conclusion Title',
            'conclusion_content': 'Conclusion Content',
        }
        
        # Add labels for numbered fields
        for i in range(1, 6):
            labels.update({
                f'sec{i}_title': f'Section {i} Title',
                f'sec{i}_content': f'Section {i} Content',
                f'sec{i}_lang': f'Section {i} Language Code',
                f'sec{i}_lang_title': f'Section {i} Language Title',
                f'sec{i}_image': f'Section {i} Image',
            })
        
        for i in range(1, 4):
            labels.update({
                f'link{i}_text': f'Link {i} Text',
                f'link{i}_url': f'Link {i} URL',
            })

        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'conclusion_content': forms.Textarea(attrs={'rows': 3}),
            'posted_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    class Meta:
        model = BlogPosts
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'conclusion_content': forms.Textarea(attrs={'rows': 3}),
            'posted_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields not required
        for field in self.fields:
            self.fields[field].required = False
        # Hide views and likes as they're auto-set
        self.fields['views'].widget = forms.HiddenInput()
        self.fields['likes'].widget = forms.HiddenInput()
from rest_framework import serializers
from .models import NewsletterSubscriber, BlogPosts
from home.models import VisitorCount

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['name', 'email']

class VisitorCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorCount
        fields = '__all__'

#api for Detailed blog posts
class BlogPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPosts
        fields = '__all__'
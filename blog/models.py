from django.utils.text import slugify
from django.db import models
import uuid

class BlogPosts(models.Model):
    # Core Fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    main_image = models.ImageField(upload_to='blog_images/')
    content = models.TextField()

    # --- Sections 1-5 ---
    # Section 1
    sec1_title = models.CharField(max_length=255, blank=True, null=True)
    sec1_content = models.TextField(blank=True, null=True)
    sec1_lang = models.TextField(blank=True, null=True)
    sec1_lang_title = models.CharField(max_length=100, blank=True, null=True)
    sec1_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    # Section 2
    sec2_title = models.CharField(max_length=255, blank=True, null=True)
    sec2_content = models.TextField(blank=True, null=True)
    sec2_lang = models.TextField(blank=True, null=True)
    sec2_lang_title = models.CharField(max_length=100, blank=True, null=True)
    sec2_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    # Section 3
    sec3_title = models.CharField(max_length=255, blank=True, null=True)
    sec3_content = models.TextField(blank=True, null=True)
    sec3_lang = models.TextField(blank=True, null=True)
    sec3_lang_title = models.CharField(max_length=100, blank=True, null=True)
    sec3_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    # Section 4
    sec4_title = models.CharField(max_length=255, blank=True, null=True)
    sec4_content = models.TextField(blank=True, null=True)
    sec4_lang = models.TextField(blank=True, null=True)
    sec4_lang_title = models.CharField(max_length=100, blank=True, null=True)
    sec4_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    # Section 5
    sec5_title = models.CharField(max_length=255, blank=True, null=True)
    sec5_content = models.TextField(blank=True, null=True)
    sec5_lang = models.TextField(blank=True, null=True)
    sec5_lang_title = models.CharField(max_length=100, blank=True, null=True)
    sec5_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    # --- Reference Links (New) ---
    link1_text = models.CharField(max_length=200, blank=True, null=True)  
    link1_url = models.URLField(blank=True, null=True)                   

    link2_text = models.CharField(max_length=200, blank=True, null=True)
    link2_url = models.URLField(blank=True, null=True)

    link3_text = models.CharField(max_length=200, blank=True, null=True)
    link3_url = models.URLField(blank=True, null=True)

    # Conclusion
    conclusion_title = models.CharField(max_length=255, blank=True, null=True)
    conclusion_content = models.TextField(blank=True, null=True)
    linkconclusion_text = models.CharField(max_length=200, blank=True, null=True)
    linkconclusion_url = models.CharField(blank=True, null=True)

    # Stats
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    posted_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        unique_slug = base_slug
        while BlogPosts.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class NewsletterSubscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    


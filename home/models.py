from django.db import models
from cloudinary.models import CloudinaryField
import uuid
from django.utils.text import slugify

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    title = models.CharField(max_length=200)
    project_type = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
class VisitorCount(models.Model):
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"Total Views: {self.views}"
    


class TemplateProducts(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image_video = CloudinaryField('Product_media', resource_type='auto', blank=True, null=True)
    tech_stack = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.TextField() 
    preview_url = models.URLField()
    source = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price in INR paise (e.g., ₹499.99 → 49999)")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        unique_slug = base_slug
        while TemplateProducts.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    


class TemplatePurchase(models.Model):
    template = models.ForeignKey("TemplateProducts", on_delete=models.CASCADE)
    
    buyer_name = models.CharField(max_length=100)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=20)

    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    amount_paid = models.PositiveIntegerField(help_text="Amount in INR paise")
    currency = models.CharField(max_length=10, default="INR")
    
    is_verified = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now_add=True)


# current working project
class CurrentProject(models.Model):
    title = models.CharField(max_length=100)
    github_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

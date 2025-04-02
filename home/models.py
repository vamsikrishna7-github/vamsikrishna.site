from django.db import models

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
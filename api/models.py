from django.db import models

# Create your models here.
class Profile(models.Model):
    username=models.TextField(null=False, default="Username", max_length=50)
    email=models.EmailField(null=False, default="Emaail", max_length=254)
    password = models.CharField(max_length=32)
    def __str__(self):
        return self.username
    
class Profiles(models.Model):
    username=models.TextField(null=False, default="Username", max_length=50)
    email=models.EmailField(null=False, default="Emaail", max_length=254)
    password = models.CharField(max_length=32)
    def __str__(self):
        return self.username
    
class Short(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    publish_date = models.DateTimeField()
    content = models.TextField()
    actual_content_link = models.URLField()
    image = models.URLField(blank=True, null=True)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

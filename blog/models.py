from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    profile_img =models.ImageField(upload_to="profile/")
    job = models.CharField(null=True,blank=True)
    bio = models.CharField(null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True)
    birth_date = models.DateTimeField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-username']
        indexes = [models.Index(fields=['-username'])]
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("user:user_detail", kwargs={"username": self.username})

# _____________________________________________________________-
class PublishQ(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class Post(models.Model):
    auther = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_post")
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    
    tags = TaggableManager()
    
    objects = models.Manager()
    publish = PublishQ()
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields= ['-created']),
        ]

    def __str__(self):
        return self.description
    def get_absolute_url(self):
        return reverse("blog:post", args=[self.id])
# ______________________________________________________________________
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    img_file = models.ImageField(upload_to="post_images/",validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return self.title if self.title else "None"
# __________________________________________________________________________
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100,null=True, blank=True)
    text = models.TextField()
    email = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"{self.name}: {self.post.title}"
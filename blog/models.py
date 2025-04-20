from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from pathlib import Path

def cloudinary_file_extension_validator(value):
    try:
        if hasattr(value, 'file') and hasattr(value.file, 'name'):
            filename = value.file.name
        else:
            filename = str(value)
            if '.' not in filename:
                return
        
        extension = Path(filename).suffix[1:].lower()
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']

        if extension not in allowed_extensions:
            raise ValidationError(
                f"File type '{extension}' is not allowed. Allowed types are {', '.join(allowed_extensions)}."
            )
    except Exception:
        raise ValidationError("The file is not a valid image or does not have a proper extension.")

# _____________________________________________________________

class User(AbstractUser):
    profile_img = CloudinaryField('image', null=True, blank=True) 
    job = models.CharField(max_length=100, null=True, blank=True) 
    bio = models.CharField(max_length=500, null=True, blank=True) 
    phone = models.CharField(max_length=11, null=True, blank=True)  
    birth_date = models.DateField(null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-username']
        indexes = [models.Index(fields=['-username'])]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("user:user_detail", kwargs={"username": self.username})

# _____________________________________________________________

class PublishQ(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class Post(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60) 
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    tags = TaggableManager()

    objects = models.Manager()
    publish = PublishQ()

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:post', args=[self.id])

# _____________________________________________________________

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    img_file = CloudinaryField("image", validators=[cloudinary_file_extension_validator])
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return self.title if self.title else "No title"

# _____________________________________________________________

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField()
    email = models.EmailField(max_length=100) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f"{self.name}: {self.post.title}"

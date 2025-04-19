from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

class User(AbstractUser):
    profile_img = CloudinaryField('image', null=True, blank=True)  # اضافه کردن null و blank برای اختیاری بودن
    job = models.CharField(max_length=100, null=True, blank=True)  # حداکثر طول برای job تعریف شد
    bio = models.CharField(max_length=500, null=True, blank=True)  # افزایش طول bio برای ذخیره‌سازی توضیحات بیشتر
    phone = models.CharField(max_length=15, null=True, blank=True)  # حداکثر طول برای شماره تلفن به ۱۵ تغییر کرد
    birth_date = models.DateField(null=True, blank=True)  # تغییر به DateField به جای DateTimeField برای تاریخ تولد
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
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)  # تغییر به SlugField برای url-friendly بودن
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
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.title  # تغییر به عنوان به جای توضیحات

    def get_absolute_url(self):
        return reverse('myblog:post', args=[self.id]) # استفاده از slug به جای id

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
# ______________________________________________________________________
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    img_file = CloudinaryField("post_images/", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return self.title if self.title else "No title"


# __________________________________________________________________________
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField()
    email = models.EmailField(max_length=100)  # تغییر به EmailField برای صحت ایمیل
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

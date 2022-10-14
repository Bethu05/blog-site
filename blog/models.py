from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Post(models.Model):
    title = models.CharField(default='', max_length=255)
    slug = models.SlugField(default='', blank=True, max_length=255)
    body = models.TextField(default='', blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    tags = TaggableManager()
    image = models.ImageField(default='', blank=True, upload_to='images')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(400, 200)],
                                     format='JPEG',
                                     options={'quality': 100, })
    # ? override default functions

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.slug)])

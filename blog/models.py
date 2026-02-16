from django.db import models
from django.utils.text import slugify

from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    content = RichTextField()

    image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


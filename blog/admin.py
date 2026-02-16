from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("is_published", "category")
    search_fields = ("title", "content")

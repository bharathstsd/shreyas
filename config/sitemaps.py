from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost
from website.models import Coach, Program, Transformation, GalleryItem


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return [
            "home",
            "about",
            "team",
            "transformations_list",
            "gallery",
            "calendar",
            "contact",
            "programs",
            "blog_list",
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("blog_detail", args=[obj.slug])


class CoachSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Coach.objects.order_by("name")

    def location(self, obj):
        return reverse("coach_detail", args=[obj.slug])


class ProgramSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Program.objects.order_by("title")

    def location(self, obj):
        return reverse("program_detail", args=[obj.slug])


class TransformationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Transformation.objects.order_by("name")

    def location(self, obj):
        return reverse("transformation_detail", args=[obj.slug])


class GallerySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return GalleryItem.objects.order_by("created_at")

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("gallery_detail", args=[obj.slug])


sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
    "coaches": CoachSitemap,
    "programs": ProgramSitemap,
    "transformations": TransformationSitemap,
    "gallery": GallerySitemap,
}

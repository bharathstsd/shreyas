from django.contrib import admin
from .models import Coach, Program, Testimonial, Lead, Event



admin.site.register(Coach)
# admin.site.register(Program)
admin.site.register(Testimonial)
admin.site.register(Lead)
admin.site.register(Event)

# admin.site.register(Appointment)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    prepopulated_fields = {"slug": ("title",)}


from .models import Transformation, TransformationMetric, JourneySection


class TransformationMetricInline(admin.TabularInline):
    model = TransformationMetric
    extra = 1


class JourneySectionInline(admin.StackedInline):
    model = JourneySection
    extra = 1


@admin.register(Transformation)
class TransformationAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "result_text", "is_featured")
    list_filter = ("category", "is_featured")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [TransformationMetricInline, JourneySectionInline]


from .models import GalleryItem


# @admin.register(GalleryItem)
# class GalleryItemAdmin(admin.ModelAdmin):
#     list_display = ("title", "category", "date", "is_featured")
#     list_filter = ("category", "is_featured")
#     search_fields = ("title", "caption")
#     prepopulated_fields = {"slug": ("title",)}


# from django.contrib import admin
from .models import (
    GalleryItem,
    GalleryStory,
    GalleryPhoto,
    GallerySection
)


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1


class GallerySectionInline(admin.TabularInline):
    model = GallerySection
    extra = 1


@admin.register(GalleryStory)
class GalleryStoryAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [GalleryPhotoInline, GallerySectionInline]


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "date")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(GalleryPhoto)
admin.site.register(GallerySection)



from .models import CalendarMonth, CalendarEvent


class CalendarEventInline(admin.TabularInline):
    model = CalendarEvent
    extra = 1


@admin.register(CalendarMonth)
class CalendarMonthAdmin(admin.ModelAdmin):
    list_display = ("title", "month", "year", "is_active")
    list_filter = ("year", "month", "is_active")
    inlines = [CalendarEventInline]


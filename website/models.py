from django.db import models
from django.utils.text import slugify


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=120, default="Shreyas Wellness World")
    short_name = models.CharField(max_length=80, default="Shreyas Wellness")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


# class Coach(models.Model):
#     name = models.CharField(max_length=100)
#     title = models.CharField(max_length=100, default="Coach")
#     photo = models.ImageField(upload_to='coaches/')
#     bio = models.TextField(blank=True)

#     clients = models.IntegerField(default=0)
#     years = models.IntegerField(default=0)
#     consultations = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name
# class Coach(models.Model):
#     name = models.CharField(max_length=100)
#     title = models.CharField(max_length=100, default="Coach")
#     photo = models.ImageField(upload_to='coaches/')
#     bio = models.TextField(blank=True)

#     clients = models.IntegerField(default=0)
#     years = models.IntegerField(default=0)
#     consultations = models.IntegerField(default=0)
#     specialization = models.CharField(max_length=100)

#     is_head_coach = models.BooleanField(default=False)
#     slug = models.SlugField(unique=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name

class Coach(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, default="Coach")
    photo = models.ImageField(upload_to='coaches/')
    bio = models.TextField(blank=True)

    clients = models.IntegerField(default=0)
    years = models.IntegerField(default=0)
    consultations = models.IntegerField(default=0)

    specialization = models.CharField(max_length=100)  # keep for listing page

    # NEW FIELDS
    specializations = models.TextField(
        blank=True,
        help_text="Comma separated values. Example: Weight Loss, Muscle Gain"
    )

    credentials = models.TextField(
        blank=True,
        help_text="Comma separated values. Example: NASM Certified, Herbalife Coach"
    )

    is_head_coach = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def get_specializations_list(self):
        if self.specializations:
            return [s.strip() for s in self.specializations.split(",")]
        return []

    def get_credentials_list(self):
        if self.credentials:
            return [c.strip() for c in self.credentials.split(",")]
        return []
    # def get_specializations_list(self):
    #     return [s.strip() for s in self.specialization.split(",") if s.strip()]

    # def get_credentials_list(self):
    #     return [c.strip() for c in self.credentials.split(",") if c.strip()]


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# class Program(models.Model):
#     title = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='programs/')
#     features = models.TextField(
#         blank=True,
#         help_text="Enter one feature per line"
#     )

#     def __str__(self):
#         return self.title

# from django.db import models
# from django.utils.text import slugify


class Program(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/')
    features = models.TextField(
        blank=True,
        help_text="Enter one feature per line"
    )

    def feature_list(self):
        if self.features:
            return [f.strip() for f in self.features.split("\n") if f.strip()]
        return []

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    quote = models.TextField(blank=True)

    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    # Only uploaded video
    # video = models.FileField(upload_to='reels/')
    video = models.FileField(
        upload_to='reels/',
        blank=True,
        null=True
    )


    # Journey link
    journey_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to full transformation story"
    )

    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    goal = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# class Appointment(models.Model):
#     name = models.CharField(max_length=120)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     date = models.DateField()
#     time = models.TimeField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.date} {self.time}"



class Transformation(models.Model):
    name = models.CharField(max_length=100)

    coach = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    before_photo = models.ImageField(upload_to="transformations/")
    after_photo = models.ImageField(upload_to="transformations/")

    result_text = models.CharField(
        max_length=100,
        help_text="Example: -12 kg, +8 kg muscle, -15% body fat"
    )

    short_story = models.TextField(
        help_text="Short testimonial shown on grid"
    )

    full_story = models.TextField(
        help_text="Full journey text"
    )

    category = models.CharField(
        max_length=50,
        choices=[
            ("weight_loss", "Weight Loss"),
            ("muscle_gain", "Muscle Gain"),
            ("wellness", "Lifestyle / Wellness"),
        ],
        default="weight_loss"
    )

    duration = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: 12 weeks, 6 months"
    )

    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TransformationMetric(models.Model):
    transformation = models.ForeignKey(
        Transformation,
        on_delete=models.CASCADE,
        related_name="metrics"
    )
    label = models.CharField(max_length=50)  # Weight, Body Fat
    value = models.CharField(max_length=50)  # -12 kg, -8%


# class JourneySection(models.Model):
#     transformation = models.ForeignKey(
#         Transformation,
#         on_delete=models.CASCADE,
#         related_name="sections"
#     )
#     title = models.CharField(max_length=100)
#     content = models.TextField()

class JourneySection(models.Model):
    transformation = models.ForeignKey(
        Transformation,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="journey_sections/", blank=True, null=True)


    class Meta:
        ordering = ["order"]


# from django.db import models
# from django.utils.text import slugify


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ("event", "Event"),
        ("trip", "Trip"),
        ("lifestyle", "Lifestyle"),
        ("transformation", "Transformation"),
    ]

    title = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="gallery/")
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="lifestyle"
    )
    caption = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)

    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryStory(models.Model):
    title = models.CharField(max_length=150)
    cover_photo = models.ImageField(upload_to="gallery/covers/")
    category = models.CharField(
        max_length=30,
        choices=[
            ("event", "Event"),
            ("trip", "Trip"),
            ("lifestyle", "Lifestyle"),
            ("community", "Community"),
        ],
        default="lifestyle"
    )
    description = models.TextField(blank=True)

    location = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# class GalleryPhoto(models.Model):
#     story = models.ForeignKey(
#         GalleryStory,
#         on_delete=models.CASCADE,
#         related_name="photos"
#     )
#     image = models.ImageField(upload_to="gallery/photos/")
#     caption = models.CharField(max_length=200, blank=True)
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ["order"]
class GalleryPhoto(models.Model):
    story = models.ForeignKey(
        GalleryStory,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(
        upload_to="gallery/photos/",
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="gallery/videos/",
        blank=True,
        null=True,
        help_text="MP4 only (optional)"
    )

    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]



class GallerySection(models.Model):
    story = models.ForeignKey(
        GalleryStory,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to="gallery/sections/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


from django.db import models
from django.utils.text import slugify


class CalendarMonth(models.Model):
    title = models.CharField(max_length=100)
    month = models.IntegerField()  # 1–12
    year = models.IntegerField()

    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        default=True,
        help_text="Only one active month will show on website"
    )

    def __str__(self):
        return f"{self.title} ({self.month}/{self.year})"


class CalendarEvent(models.Model):
    month = models.ForeignKey(
        CalendarMonth,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(max_length=150)
    date = models.DateField()

    time = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: 7:00 AM – Yoga Session"
    )

    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.date}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.CharField(max_length=50, blank=True)
    link = models.URLField(
        blank=True,
        help_text="Optional link (Zoom, WhatsApp, registration, etc.)"
    )


    def __str__(self):
        return f"{self.title} - {self.date}"

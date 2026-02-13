from django.db import models


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
class Coach(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, default="Coach")
    photo = models.ImageField(upload_to='coaches/')
    bio = models.TextField(blank=True)

    clients = models.IntegerField(default=0)
    years = models.IntegerField(default=0)
    consultations = models.IntegerField(default=0)

    is_head_coach = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Program(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/')
    features = models.TextField(
        blank=True,
        help_text="Enter one feature per line"
    )

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


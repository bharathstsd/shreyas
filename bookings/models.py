# from django.db import models

# Create your models here.
# class Appointment(models.Model):
#     name = models.CharField(max_length=120)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     date = models.DateField()
#     time = models.TimeField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.date} {self.time}"



from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    date = models.DateField()
    time = models.TimeField()

    zoom_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("date", "time")  # prevents double booking

    def __str__(self):
        return f"{self.name} – {self.date} {self.time}"

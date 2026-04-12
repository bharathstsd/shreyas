from django.db import models

# Create your models here.
# from django.db import models

class Invite(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    coach_name = models.CharField(max_length=100)
    coach_phone = models.CharField(max_length=20)

    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)

    image = models.ImageField(upload_to="invites/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} invited by {self.coach_name}"

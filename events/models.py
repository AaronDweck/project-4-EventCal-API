from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='events'
        )
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # this is used just incase the user bypassed the required opiton it would set a default to an hour after the start date
        if not self.end_date:
            self.end_date = self.start_date + timedelta(hours=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
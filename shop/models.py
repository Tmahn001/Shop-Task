from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

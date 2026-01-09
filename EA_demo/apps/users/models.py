from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        OO = "oo", "OO"
        SG = "sg", "SG"

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.OO
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

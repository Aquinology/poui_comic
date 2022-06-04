from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars/', default='user_avatars/no-image.jpg', blank=True)

    def __str__(self):
        return self.get_full_name()

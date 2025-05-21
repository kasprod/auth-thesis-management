from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(verbose_name=_('Bio'),null=True,blank=True)
    profile_photo = models.ImageField(verbose_name=_('Profile Photo'),upload_to='profile_image', blank=True, null=True,default="profile_image/user.png")
    phone_number = models.CharField(verbose_name=_('phone number'),max_length=25,null=True,blank=True)
    is_student = models.BooleanField(default=False)
    is_academic_personal = models.BooleanField(default=False)
    is_searcher = models.BooleanField(default=False)

    @property
    def get_full_name(self):
        return f'{self.last_name.capitalize()} {self.first_name.capitalize()}'

    def __str__(self):
        return self.username


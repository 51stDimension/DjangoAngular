from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse

# Create your models here.
class UserModel(models.Model):
    user = models.OneToOneField(User,related_name="user_profile",on_delete=models.CASCADE)
    profile_photo = models.ImageField(null=True,blank=True,upload_to='photos')


    def __str__(self):
        return self.user.username

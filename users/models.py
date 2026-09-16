from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User (AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    number_series = models.IntegerField(max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}".strip()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.email}'

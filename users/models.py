from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'), 
        ('F', 'Female'), 
        ('O', 'Other')
    ]
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
    bio = models.TextField(max_length = 500, blank = True)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = 'O')
    location = models.CharField(max_length = 100, blank = True) # Deprecated, keeping for fallback
    
    from django_countries.fields import CountryField
    country = CountryField(blank=True)
    state = models.CharField(max_length=100, blank=True)
    
    diamonds = models.IntegerField(default = 20)
    age = models.PositiveIntegerField(default = 18)
    call_price = models.IntegerField(default = 0)
    last_seen = models.DateTimeField(default = timezone.now)

    # Verification
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'
    
    def is_online(self):
        return timezone.now() - self.last_seen < timezone.timedelta(minutes = 5)
        

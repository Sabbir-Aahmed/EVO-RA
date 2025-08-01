from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator



class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images',blank=True,  default= "profile_images/default.webp")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    phone_number = models.CharField(
        max_length=15, blank=True,validators=[ RegexValidator(
                                            regex=r'^(\+8801|01)\d{9}$',
                                            message="Phone number must be in the format: '01XXXXXXXXX' or '+8801XXXXXXXXX'."
                                        ),
                                    ],
                                   help_text="Enter your phone number like 01XXXXXXXXX. '+880' will be added automatically if not included."
    )

    def save(self, *args, **kwargs):
        if self.phone_number:
            cleaned_number = self.phone_number.replace(' ', '')
            if cleaned_number.startswith('01'):
                self.phone_number = '+880' + cleaned_number[1:]
            elif not cleaned_number.startswith('+880'):
                self.phone_number = '+880' + cleaned_number
        super().save(*args, **kwargs)

        
    def __str__(self):
        return self.username
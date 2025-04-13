from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from category.models import Category

# Extending Django's default User model to include custom fields for freelancers and employers
class User(AbstractUser):
    # Define user types: either a freelancer or an employer
    USER_TYPE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('employer', 'Employer')
    ]

    # Custom field to identify the type of user (freelancer or employer)
    user_type = models.CharField(
        max_length=255,
        verbose_name='User Type',
        choices=USER_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # Links each user to a job category; useful mainly for freelancers
    category = models.ForeignKey(
        Category,
        verbose_name="Job Field",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    # Stores the user's phone number; must be unique and 10 digits
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Phone Number",
        blank=True,
        null=True
    )

    # Uploaded resumes (usually for freelancers)
    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True,
        verbose_name="Resume"
    )

    # Returns a human-readable string representation of the user object
    def __str__(self):
        return f"{self.username}({self.user_type})"
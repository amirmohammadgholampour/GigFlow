from django.db import models
from django.contrib.auth import get_user_model

# Getting the custom User model
User = get_user_model()

class SampleWork(models.Model):
    """
    Model to represent a portfolio item created by a freelancer to showcase their skills.
    """

    # Reference to the user (freelancer) who created this sample work
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="User"
    )
    
    # Title or name of the portfolio item
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )

    # Detailed description of the sample work or project
    description = models.TextField(
        verbose_name="Description"
    )

    # Main skill or technology used in the project
    skill = models.CharField(
        max_length=255,
        verbose_name="Skill used for sample project"
    )

    # Optional image representing the sample work
    image = models.ImageField(
        verbose_name="Image", 
        blank=True
    )

    # Timestamp when the sample work was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # String representation of the SampleWork instance
    def __str__(self):
        return self.name
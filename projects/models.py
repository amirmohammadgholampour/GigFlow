from django.db import models 
from user.models import User 
from category.models import Category

# Represents a project posted by a user (typically an employer)
class Projects(models.Model):
    # The user who created the project (usually an employer)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,     # If the user is deleted, their projects will be deleted too
        related_name="user_id"        # Used for reverse relation lookups
    )

    # Title of the project
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )

    # Detailed description of the project
    description = models.TextField(
        verbose_name="Description"
    )

    # The category this project falls under (e.g., "Design", "Development")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Category"
    )

    # Deadline for the project (string format — consider using DateField for stricter validation)
    deadline = models.CharField(
        max_length=255,
        verbose_name="Deadline"
    )

    # Project's proposed budget or price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Timestamp when the project was created (automatically set once)
    created_at = models.DateTimeField(auto_now_add=True)

    # Human-readable representation of the project (used in admin panel and logs)
    def __str__(self):
        return self.name
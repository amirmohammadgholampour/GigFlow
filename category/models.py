from django.db import models 

# Represents a high-level job category (e.g., Design, Development, Marketing)
class Category(models.Model):
    # The name of the category (e.g., "Design", "Programming")
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )

    # Timestamp for when the category was created (automatically set once)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: Add a string representation for admin panels and readability
    def __str__(self):
        return self.name
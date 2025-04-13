from django.db import models 
from category.models import Category

# Represents a skill that can be linked to a job category (e.g., "Python" under "Programming")
class Skill(models.Model):
    # The name of the skill (e.g., "React", "UI Design")
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )

    # The category this skill belongs to (e.g., "Development", "Design")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE  # If the category is deleted, all related skills will be deleted too
    )

    # Timestamp for when the skill was created (automatically set once)
    created_at = models.DateTimeField(auto_now_add=True)

    # Returns the name of the skill as its string representation
    def __str__(self):
        return self.name
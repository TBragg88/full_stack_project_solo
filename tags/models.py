from django.db import models


class Tag(models.Model):
    """
    Master tag database - categories for organizing recipes.
    """
    TAG_TYPES = [
        ('cuisine', 'Cuisine'),
        ('meal_type', 'Meal Type'),
        ('dietary', 'Dietary'),
        ('cooking_method', 'Cooking Method'),
        ('time', 'Time'),
        ('course', 'Course'),
    ]

    name = models.CharField(max_length=100, unique=True)
    tag_type = models.CharField(max_length=50, choices=TAG_TYPES)
    color = models.CharField(max_length=7, help_text='hex color for UI')
    icon_url = models.TextField(blank=True, null=True,
                                help_text='optional icon for navigation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tag_type})"


class RecipeTag(models.Model):
    """
    Junction table connecting recipes to tags.
    Note: We use 'recipes.Recipe' because Recipe is in a different app.
    """
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['recipe', 'tag']  # Prevent duplicate tags

    def __str__(self):
        return f"{self.recipe.title} - {self.tag.name}"

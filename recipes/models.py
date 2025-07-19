from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Recipe(models.Model):
    """
    Main recipe model - stores all the basic information about a recipe.
    """
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    prep_time = models.IntegerField(
        help_text='minutes',
        validators=[MinValueValidator(0)]
    )
    cook_time = models.IntegerField(
        help_text='minutes',
        validators=[MinValueValidator(0)]
    )
    base_servings = models.IntegerField(
        help_text='original recipe servings - used for scaling calculations'
    )
    difficulty_level = models.CharField(max_length=20,
                                        choices=DIFFICULTY_CHOICES)
    main_image_url = CloudinaryField('image', default='placeholder')
    is_public = models.BooleanField(default=True,
                                    help_text='true/false for privacy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time

    def get_average_rating(self):
        """Calculate average rating for this recipe"""
        ratings = self.rating_set.all()
        if ratings:
            return sum(r.rating_value for r in ratings) / len(ratings)
        return 0

    def get_total_likes(self):
        """Get total number of likes"""
        return self.userlikes_set.count()


class Ingredient(models.Model):
    """
    Master ingredient database - one entry per unique ingredient.
    Includes nutritional data per 100g for smart recipe calculations.
    """
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(
        max_length=100,
        help_text='produce/meat/dairy/etc'
    )
    common_unit = models.CharField(
        max_length=20,
        help_text='grams/ml/pieces/etc'
    )
    dietary_flags = models.TextField(
        blank=True,
        help_text='JSON array: '
                  '["dairy", "gluten", "nuts", "soy", "eggs"] '
                  '- what this ingredient contains'
    )

    # Macronutrients per 100g
    calories_per_100g = models.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            null=True,
                                            blank=True)
    protein_per_100g = models.DecimalField(max_digits=8,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    carbs_per_100g = models.DecimalField(max_digits=8,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    fat_per_100g = models.DecimalField(max_digits=8,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    fibre_per_100g = models.DecimalField(max_digits=8,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    sugars_per_100g = models.DecimalField(max_digits=8,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    sodium_mg_per_100g = models.DecimalField(max_digits=8,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    saturated_fat_per_100g = models.DecimalField(max_digits=8,
                                                 decimal_places=2,
                                                 null=True,
                                                 blank=True)

    # Optional meta field
    nutritional_basis = models.CharField(
        max_length=20,
        default="per 100g",
        help_text='Basis of nutritional values (e.g. per 100g, per slice)'
    )

    def __str__(self):
        return self.name

    def get_dietary_flags(self):
        """Convert JSON string to Python list"""
        if self.dietary_flags:
            try:
                return json.loads(self.dietary_flags)
            except json.JSONDecodeError:
                return []
        return []

    def set_dietary_flags(self, flags_list):
        """Convert Python list to JSON string"""
        self.dietary_flags = json.dumps(flags_list)


class RecipeIngredient(models.Model):
    """
    Junction table connecting recipes to ingredients with quantities.
    This allows many-to-many relationships with extra data.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_numeric = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        help_text='250.0/125.5/etc for calculations'
    )
    quantity_display = models.CharField(
        max_length=100,
        help_text='250g/1 1/2 cups for display'
    )
    unit = models.CharField(max_length=20, help_text='grams/ml/pieces/etc')
    notes = models.TextField(blank=True,
                             help_text='optional: sifted, room temp, etc')
    display_order = models.IntegerField(help_text='order in ingredient list')

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.quantity_display} {self.ingredient.name}"


class RecipeStep(models.Model):
    """
    Individual cooking steps for recipes.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.IntegerField(help_text='1,2,3...')
    instruction = models.TextField()
    estimated_time = models.IntegerField(
        null=True,
        blank=True,
        help_text='minutes for this step'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.instruction[:50]}..."


class StepImage(models.Model):
    """
    Images for cooking steps to help users visualize the process.
    """
    step = models.ForeignKey(RecipeStep, on_delete=models.CASCADE)
    image_url = CloudinaryField('image')
    alt_text = models.CharField(
        max_length=255,
        help_text='description for accessibility and display'
    )
    display_order = models.IntegerField(
        help_text='if multiple images per step')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Image for {self.step}"

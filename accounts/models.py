from django.contrib.auth.models import User
from django.db import models
import json


class UserProfile(models.Model):
    """
    Extends Django's built-in User model with additional profile information.
    This is a One-to-One relationship - each User has exactly one UserProfile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True)
    dietary_preferences = models.TextField(
        blank=True,
        help_text='JSON array: '
        '["vegan", "gluten-free", "dairy-free", "nut-free"]'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method defines how the object appears in admin and when printed.
        """
        return f"{self.user.username}'s Profile"

    def get_dietary_preferences(self):
        """
        Convert JSON string to Python list for easier use in templates/views.
        """
        if self.dietary_preferences:
            try:
                return json.loads(self.dietary_preferences)
            except json.JSONDecodeError:
                return []
        return []

    def set_dietary_preferences(self, preferences_list):
        """
        Convert Python list to JSON string for storage in database.
        """
        self.dietary_preferences = json.dumps(preferences_list)

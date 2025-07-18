from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    """
    User ratings for recipes (1-5 stars).
    """
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1-5 stars'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['recipe', 'user']  # One rating per user per recipe

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title}: {self.rating_value} stars"


class UserLikes(models.Model):
    """
    User likes/saves for recipes - like a bookmark system.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe']  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"


class Comment(models.Model):
    """
    Comments on recipes - supports replies (nested comments).
    """
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.parent_comment:
            return f"Reply by {self.user.username} to {self.parent_comment.user.username}"
        return f"Comment by {self.user.username} on {self.recipe.title}"

    def get_replies(self):
        """Get all replies to this comment"""
        return Comment.objects.filter(parent_comment=self).order_by('created_at')

    def is_reply(self):
        """Check if this is a reply to another comment"""
        return self.parent_comment is not None

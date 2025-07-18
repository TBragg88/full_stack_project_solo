from django.contrib.auth.models import User
from django.db import models


class SearchHistory(models.Model):
    """
    Optional: Track user search history for analytics or suggestions.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    search_query = models.CharField(max_length=255)
    results_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Search Histories"
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"{self.user.username} searched: {self.search_query}"
        return f"Anonymous searched: {self.search_query}"

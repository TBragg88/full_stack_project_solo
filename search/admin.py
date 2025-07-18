from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for SearchHistory model.
    """
    list_display = [
                    'search_query',
                    'user',
                    'results_count',
                    'created_at'
                    ]
    list_filter = [
                   'created_at',
                   'results_count'
                   ]
    search_fields = [
                     'search_query',
                     'user__username'
                     ]

    readonly_fields = ['created_at']
    ordering = ['-created_at']

    # Show only the most recent 1000 searches (performance optimization)
    def get_queryset(self, request):
        return super().get_queryset(request)[:1000]

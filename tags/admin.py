from django.contrib import admin
from .models import Tag, RecipeTag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for Tag model.
    """
    list_display = [
                    'name',
                    'tag_type',
                    'color',
                    'created_at'
                    ]
    list_filter = [
                   'tag_type',
                   'created_at'
                   ]
    search_fields = ['name']

    fieldsets = [
        ('Tag Information', {
            'fields': [
                       'name',
                       'tag_type'
                       ]
        }),
        ('Display Options', {
            'fields': [
                       'color',
                       'icon_url'
                       ]
        }),
        ('Timestamps', {
            'fields': ['created_at'],
            'classes': ['collapse']
        })
    ]

    readonly_fields = ['created_at']
    ordering = ['tag_type', 'name']


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    """
    Admin interface for RecipeTag model.
    """
    list_display = [
                    'recipe',
                    'tag',
                    'created_at'
                    ]
    list_filter = [
                   'tag__tag_type',
                   'created_at'
                   ]
    search_fields = [
                     'recipe__title',
                     'tag__name'
                     ]

    # Make it easy to add tags to recipes
    autocomplete_fields = ['recipe']

    ordering = ['-created_at']

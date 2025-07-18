# social/admin.py
from django.contrib import admin
from .models import Rating, UserLikes, Comment


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Admin interface for Rating model.
    """
    list_display = [
                    'recipe',
                    'user',
                    'rating_value',
                    'created_at'
                    ]
    list_filter = [
                   'rating_value',
                   'created_at'
                   ]
    search_fields = [
                     'recipe__title',
                     'user__username'
                     ]

    # Show readonly fields
    readonly_fields = [
                       'created_at',
                       'updated_at'
                       ]

    ordering = ['-created_at']


@admin.register(UserLikes)
class UserLikesAdmin(admin.ModelAdmin):
    """
    Admin interface for UserLikes model.
    """
    list_display = [
                    'user',
                    'recipe',
                    'created_at'
                    ]
    list_filter = ['created_at']
    search_fields = [
                     'user__username',
                     'recipe__title'
                     ]

    readonly_fields = ['created_at']
    ordering = ['-created_at']


class CommentReplyInline(admin.TabularInline):
    """
    Shows replies to a comment directly on the comment page.
    """
    model = Comment
    fk_name = 'parent_comment'  # This tells Django which ForeignKey to use
    extra = 0
    fields = [
              'user',
              'comment_text',
              'created_at'
              ]
    readonly_fields = ['created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model.
    """
    inlines = [CommentReplyInline]

    list_display = [
                    'recipe',
                    'user',
                    'comment_preview',
                    'is_reply',
                    'created_at'
                    ]
    list_filter = [
                   'created_at',
                   'updated_at'
                   ]
    search_fields = [
                     'recipe__title',
                     'user__username',
                     'comment_text'
                     ]

    readonly_fields = [
                       'created_at',
                       'updated_at'
                       ]

    fieldsets = [
        ('Comment Information', {
            'fields': [
                       'recipe',
                       'user',
                       'comment_text'
                       ]
        }),
        ('Reply Information', {
            'fields': ['parent_comment'],
            'description':
            'Leave blank if this is not a reply to another comment.'
        }),
        ('Timestamps', {
            'fields': [
                       'created_at',
                       'updated_at'],
            'classes': ['collapse']
        })
    ]

    def comment_preview(self, obj):
        """Show a preview of the comment in the list view."""
        return (
            obj.comment_text[:100] + "..."
            if len(obj.comment_text) > 100
            else obj.comment_text
        )
    comment_preview.short_description = "Comment Preview"

    ordering = ['-created_at']

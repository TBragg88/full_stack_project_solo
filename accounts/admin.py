from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


admin.site.site_header = "Only Pans Recipe Admin"
admin.site.site_title = "Only Pans Admin"
admin.site.index_title = "Welcome to Only Pans Administration"


class UserProfileInline(admin.StackedInline):
    """
    This allows you to edit UserProfile data directly on the User page.
    StackedInline displays the fields vertically (good for few fields).
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profiles"

    # Show these fields in the admin
    fields = ['profile_image_url', 'bio', 'dietary_preferences']


class CustomUserAdmin(UserAdmin):
    """
    Extends Django's default User admin to include UserProfile.
    """
    inlines = [UserProfileInline]

# Unregister the default User admin and register our custom one


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register UserProfile separately too (in case you want to edit it directly)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = [
                    'user',
                    'created_at',
                    'updated_at'
                    ]
    list_filter = [
                   'created_at',
                   'updated_at'
                   ]
    search_fields = [
                     'user__username',
                     'user__email',
                     'bio'
                     ]
    readonly_fields = [
                       'created_at',
                       'updated_at'
                       ]

    # Organize fields into sections
    fieldsets = [
        ('User Information', {
            'fields': ['user']
        }),
        ('Profile Details', {
            'fields': [
                       'profile_image_url',
                       'bio',
                       'dietary_preferences'
                       ]
        }),
        ('Timestamps', {
            'fields': [
                       'created_at',
                       'updated_at'
                       ],
            'classes': ['collapse']  # collapsed by default
        })
    ]

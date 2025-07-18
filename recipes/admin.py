# recipes/admin.py
from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, RecipeStep, StepImage


class RecipeIngredientInline(admin.TabularInline):
    """
    Allows you to add ingredients directly on the Recipe page.
    TabularInline displays fields horizontally (good for many items).
    """
    model = RecipeIngredient
    extra = 1  # Shows 1 empty form by default
    fields = [
              'ingredient',
              'quantity_display',
              'quantity_numeric',
              'unit',
              'notes',
              'display_order']
    ordering = ['display_order']


class RecipeStepInline(admin.TabularInline):
    """
    Allows you to add cooking steps directly on the Recipe page.
    """
    model = RecipeStep
    extra = 1
    fields = [
              'step_number',
              'instruction',
              'estimated_time'
              ]
    ordering = ['step_number']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin interface for Recipe model.
    """
    # Include the related models as inlines
    inlines = [RecipeIngredientInline, RecipeStepInline]

    # What to show in the recipe list
    list_display = [
                    'title',
                    'user',
                    'difficulty_level',
                    'total_time',
                    'is_public',
                    'created_at'
                    ]

    # Add filters on the right side
    list_filter = [
                   'difficulty_level',
                   'is_public',
                   'created_at',
                   'updated_at'
                   ]

    # Add search functionality
    search_fields = [
                     'title',
                     'description',
                     'user__username'
                     ]

    # Fields that can't be edited
    readonly_fields = [
                       'created_at',
                       'updated_at'
                       ]

    # Organize fields into sections
    fieldsets = [
        ('Basic Information', {
            'fields': [
                       'user',
                       'title',
                       'description',
                       'main_image_url'
                       ]
        }),
        ('Recipe Details', {
            'fields': [
                       'prep_time',
                       'cook_time',
                       'base_servings',
                       'difficulty_level',
                       'is_public'
                       ]
        }),
        ('Timestamps', {
            'fields': [
                        'created_at',
                        'updated_at'
                        ],
            'classes': ['collapse']
        })
    ]

    # Default ordering
    ordering = ['-created_at']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Admin interface for Ingredient model.
    """
    list_display = [
                    'name',
                    'category',
                    'common_unit',
                    'calories_per_100g'
                    ]
    list_filter = ['category']
    search_fields = ['name', 'category']

    fieldsets = [
        ('Basic Information', {
            'fields': [
                       'name',
                       'category',
                       'common_unit',
                       'dietary_flags'
                       ]
        }),
        ('Nutritional Information', {
            'fields': [
                       'calories_per_100g',
                       'protein_per_100g',
                       'carbs_per_100g',
                       'fat_per_100g'
                       ],
            'classes': ['collapse']
        })
    ]


class StepImageInline(admin.TabularInline):
    """
    Allows you to add step images directly on the RecipeStep page.
    """
    model = StepImage
    extra = 1
    fields = ['image_url', 'alt_text', 'display_order']


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    """
    Admin interface for RecipeStep model.
    """
    inlines = [StepImageInline]
    list_display = [
                    'recipe',
                    'step_number',
                    'instruction_preview',
                    'estimated_time'
                    ]
    list_filter = [
                   'recipe',
                   'estimated_time'
                   ]
    search_fields = [
                     'recipe__title',
                     'instruction'
                     ]
    ordering = ['recipe',
                'step_number'
                ]

    def instruction_preview(self, obj):
        """Show a preview of the instruction in the list view."""
        return (
            obj.instruction[:100] + "..."
            if len(obj.instruction) > 100
            else obj.instruction
        )
    instruction_preview.short_description = "Instruction Preview"

# Register the remaining models with basic admin


admin.site.register(RecipeIngredient)
admin.site.register(StepImage)

# Generated by Django 5.2.4 on 2025-07-19 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_main_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='fibre_per_100g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='nutritional_basis',
            field=models.CharField(default='per 100g', help_text='Basis of nutritional values (e.g. per 100g, per slice)', max_length=20),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='saturated_fat_per_100g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='sodium_mg_per_100g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='sugars_per_100g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]

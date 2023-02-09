# Generated by Django 4.1.6 on 2023-02-07 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="price",
            new_name="unit_price",
        ),
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(default="-"),
        ),
    ]
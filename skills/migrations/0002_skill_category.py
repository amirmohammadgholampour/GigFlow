# Generated by Django 5.2 on 2025-04-10 12:54

import builtins
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='category',
            field=models.ForeignKey(default=builtins.print, on_delete=django.db.models.deletion.CASCADE, to='category.category'),
            preserve_default=False,
        ),
    ]

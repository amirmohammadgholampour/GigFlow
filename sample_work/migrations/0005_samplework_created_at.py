# Generated by Django 5.2 on 2025-04-06 16:41

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_work', '0004_alter_samplework_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplework',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=builtins.print),
            preserve_default=False,
        ),
    ]

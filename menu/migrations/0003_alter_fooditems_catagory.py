# Generated by Django 5.2.1 on 2025-07-13 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_catagory_options_alter_catagory_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditems',
            name='catagory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fooditems', to='menu.catagory'),
        ),
    ]

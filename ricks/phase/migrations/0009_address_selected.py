# Generated by Django 4.1.4 on 2023-02-13 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phase', '0008_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
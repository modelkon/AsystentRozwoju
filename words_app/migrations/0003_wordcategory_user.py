# Generated by Django 4.2.4 on 2023-08-08 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words_app', '0002_wordcategory_wordtolearn_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordcategory',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

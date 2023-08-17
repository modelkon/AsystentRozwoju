# Generated by Django 4.2.4 on 2023-08-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='wordtolearn',
            name='category',
            field=models.ManyToManyField(to='words_app.wordcategory'),
        ),
    ]

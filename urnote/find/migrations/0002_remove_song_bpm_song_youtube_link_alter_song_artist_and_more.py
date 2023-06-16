# Generated by Django 4.2.1 on 2023-06-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='bpm',
        ),
        migrations.AddField(
            model_name='song',
            name='youtube_link',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-03 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_rename_user_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
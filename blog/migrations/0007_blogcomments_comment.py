# Generated by Django 4.0 on 2022-02-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_users_blogcomments_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomments',
            name='comment',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.0.2 on 2024-02-24 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SocialDistribution", "0014_follower_following_delete_follow"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_draft",
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-09 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("telegram_bot", "0005_alter_telegramprofile_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.BigIntegerField(verbose_name="user id")),
                (
                    "created_on",
                    models.DateTimeField(auto_now_add=True, verbose_name="created on"),
                ),
            ],
        ),
    ]
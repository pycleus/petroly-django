# Generated by Django 3.2.10 on 2022-01-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0017_report_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.CharField(choices=[('content', 'inappropriate content'), ('link', 'invalid link'), ('other', 'other')], max_length=8, verbose_name='Reason'),
        ),
    ]
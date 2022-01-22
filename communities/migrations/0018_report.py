# Generated by Django 3.2.10 on 2022-01-19 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0017_delete_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Created on')),
                ('reason', models.CharField(choices=[('content', 'inappropriate content'), ('link', 'invalid link'), ('other', 'other')], max_length=8, verbose_name='Reason')),
                ('other_reason', models.CharField(blank=True, default='', max_length=100, verbose_name='Other_reason')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='communities.community', verbose_name='community')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
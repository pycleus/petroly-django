# Generated by Django 3.2.2 on 2021-06-14 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_alter_answer_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answers',
        ),
        migrations.AddField(
            model_name='answer',
            name='answers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answersfor2m', to='forum.answer'),
        ),
        migrations.RemoveField(
            model_name='tag',
            name='question',
        ),
        migrations.AddField(
            model_name='tag',
            name='question',
            field=models.ManyToManyField(related_name='tags', to='forum.Question'),
        ),
    ]
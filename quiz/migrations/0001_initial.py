# Generated by Django 4.1.5 on 2023-01-15 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, verbose_name='Question')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Text')),
                ('answer', models.BooleanField(default=False, verbose_name='Is Answer?')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='quiz.quiz')),
            ],
        ),
    ]

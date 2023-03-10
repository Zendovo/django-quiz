# Generated by Django 4.1.5 on 2023-01-15 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='question',
        ),
        migrations.AddField(
            model_name='quiz',
            name='title',
            field=models.CharField(default='test', max_length=50, verbose_name='Quiz Title'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Question Title')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz')),
            ],
        ),
    ]

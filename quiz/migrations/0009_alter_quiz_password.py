# Generated by Django 4.1.5 on 2023-01-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_alter_selectedoptions_options_quiz_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='password',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Quiz Password'),
        ),
    ]

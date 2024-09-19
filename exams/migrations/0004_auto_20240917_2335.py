# Generated by Django 3.0.5 on 2024-09-17 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_auto_20240917_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='time_spent',
            field=models.DurationField(blank=True, null=True),
        ),
    migrations.AddField(
            model_name='examresult',
            name='total_marks',
            field=models.DecimalField(decimal_places=2, default=8, max_digits=5),
            preserve_default=False,
        ),
    ]

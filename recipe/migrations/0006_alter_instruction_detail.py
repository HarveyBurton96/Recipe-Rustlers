# Generated by Django 3.2.16 on 2023-02-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20230220_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='detail',
            field=models.CharField(max_length=400),
        ),
    ]
# Generated by Django 4.1.1 on 2022-09-14 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0029_supportquery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportquery",
            name="message",
            field=models.TextField(max_length=60),
        ),
    ]
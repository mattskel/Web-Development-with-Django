# Generated by Django 4.2.4 on 2023-12-29 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_field', models.ImageField(upload_to='images/')),
                ('file_field', models.FileField(upload_to='files/')),
            ],
        ),
    ]
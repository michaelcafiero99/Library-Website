# Generated by Django 3.2.9 on 2021-11-25 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.TextField(max_length=255)),
                ('password', models.TextField(max_length=255)),
                ('firstName', models.TextField(max_length=255)),
                ('lastName', models.TextField(max_length=255)),
                ('emailAddress', models.TextField(max_length=255, null=True)),
            ],
        ),
    ]

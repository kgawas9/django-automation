# Generated by Django 5.0.2 on 2024-04-10 20:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

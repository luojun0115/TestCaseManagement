# Generated by Django 2.2 on 2021-06-15 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210615_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='brief_content',
            field=models.TextField(default=2021),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.1.3 on 2020-11-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201123_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default='sample name', max_length=255),
            preserve_default=False,
        ),
    ]

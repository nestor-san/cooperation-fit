# Generated by Django 3.1.3 on 2020-11-23 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_review_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooperation',
            name='org_staff',
        ),
        migrations.AddField(
            model_name='cooperation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]

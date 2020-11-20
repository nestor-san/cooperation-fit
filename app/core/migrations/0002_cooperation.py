# Generated by Django 3.1.3 on 2020-11-20 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('org_worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='org_worker', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
                ('voluntary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='voluntary', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

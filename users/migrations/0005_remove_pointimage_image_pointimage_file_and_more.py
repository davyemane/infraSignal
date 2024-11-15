# Generated by Django 5.1.2 on 2024-11-14 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_problemtype_sensitivepoint_pointimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointimage',
            name='image',
        ),
        migrations.AddField(
            model_name='pointimage',
            name='file',
            field=models.FileField(default=14, upload_to='sensitive_points/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pointimage',
            name='sensitive_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='users.sensitivepoint'),
        ),
    ]

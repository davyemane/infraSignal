# Generated by Django 5.1.2 on 2024-11-12 10:28

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_groups_customuser_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensitivePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('sector', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('IN_PROGRESS', 'En cours'), ('RESOLVED', 'Résolu'), ('CANCELED', 'Annulé')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensitive_points', to=settings.AUTH_USER_MODEL)),
                ('problem_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sensitive_points', to='users.problemtype')),
            ],
        ),
        migrations.CreateModel(
            name='PointImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sensitive_points/')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('sensitive_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='users.sensitivepoint')),
            ],
        ),
    ]

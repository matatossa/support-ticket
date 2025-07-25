# Generated by Django 5.0.7 on 2024-09-10 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_remove_claim_customer_remove_claim_websitelink_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('website_link', models.URLField()),
                ('description', models.TextField()),
                ('cause', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('archived_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveIntegerField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

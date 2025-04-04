# Generated by Django 4.2.7 on 2025-04-02 13:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('json_data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

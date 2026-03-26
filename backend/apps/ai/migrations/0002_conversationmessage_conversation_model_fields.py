# Generated manually for AI copilot persistence.

import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="last_response_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="conversation",
            name="model",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name="ConversationMessage",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("role", models.CharField(choices=[("USER", "User"), ("ASSISTANT", "Assistant"), ("SYSTEM", "System")], max_length=20)),
                ("content", models.TextField()),
                ("response_id", models.CharField(blank=True, max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "conversation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="ai.conversation",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(app_label)s_%(class)ss",
                        to="tenants.tenant",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]

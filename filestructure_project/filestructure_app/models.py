from django.db import models
import uuid

class ProcessedFile(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    json_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Session {self.session_id}"
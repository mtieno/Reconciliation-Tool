from django.db import models

from django.db import models

class CSVRecord(models.Model):
    unique_identifier = models.CharField(max_length=100)
    data = models.JSONField()  # Stores record data as JSON

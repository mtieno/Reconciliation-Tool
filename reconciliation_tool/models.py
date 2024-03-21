from django.db import models

class CSVRecord(models.Model):
    unique_identifier = models.CharField(max_length=100, db_index=True)
    data = models.JSONField()  # Stores record data as JSON

    def __str__(self):
        return f"CSVRecord: {self.unique_identifier}"
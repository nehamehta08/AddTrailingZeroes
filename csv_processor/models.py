from django.db import models

class ProcessedCSV(models.Model):
    original_csv = models.FileField(upload_to='uploads/')
    processed_csv = models.FileField(upload_to='processed/')

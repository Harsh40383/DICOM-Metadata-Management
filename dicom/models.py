# dicom/models.py

from django.db import models

class DICOMMetadata(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=20)
    birthdate = models.DateField(null=True, blank=True)
    study_id = models.CharField(max_length=50)
    study_description = models.CharField(max_length=255)
    study_date = models.DateField()
    modality = models.CharField(max_length=10)
    pixel_spacing = models.CharField(max_length=50)
    # Add more fields as needed

    def __str__(self):
        return f"{self.patient_name} - {self.study_description}"

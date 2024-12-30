from django.db import models

class Documents(models.Model):
    CATEGORY_CHOICES = [
        ('invoice', 'Invoice'),
        ('project_progress', 'Project Progress'),
        ('remote_work', 'Remote Work'),
    ]
    
    title = models.CharField(max_length=255)
    document_pdf = models.FileField(upload_to='documents/')  # Utilisation de FileField pour stocker les fichiers
    created_by = models.CharField(max_length=100, null=True, blank=True)  # Peut être null si non fourni
    status = models.CharField(max_length=500)  # Peut être null si non fourni
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Blog', null=True, blank=True)
    managerId = models.IntegerField(null=True, blank=True)  # Peut être null si non fourni
    isApprouved = models.BooleanField(null=True, blank=True)
    
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'documents'

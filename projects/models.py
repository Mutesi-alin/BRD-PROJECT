from django.db import models
from clients.models import Client


class Project(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
    )

    VALID_TRANSITIONS = {
        'PENDING': ['APPROVED', 'REJECTED'],
        'APPROVED': ['ONGOING'],
        'REJECTED': [],
        'ONGOING': ['COMPLETED'],
        'COMPLETED': [],
    }

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.name
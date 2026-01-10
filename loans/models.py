from django.db import models

# Create your models here.
from django.db import models
from projects.models import Project
from user.models import User

# Create your models here.
class Loan(models.Model):
    APPROVAL_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    amount_approved = models.DecimalField(max_digits=15, decimal_places=2)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approval_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Loan for {self.project.name}"

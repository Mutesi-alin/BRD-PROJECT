from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from loans.models import Loan
from user.models import User

class Disbursement(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    disbursement_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Disbursement {self.amount}"

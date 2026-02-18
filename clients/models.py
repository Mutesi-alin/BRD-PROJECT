from django.db import models
from django.core.validators import RegexValidator

rwanda_nid_validator = RegexValidator(
    regex=r'^\d{16}$',
    message='National ID must be exactly 16 digits.'
)


class Client(models.Model):
    CLIENT_TYPE_CHOICES = (
        ('INDIVIDUAL', 'Individual'),
        ('ORGANIZATION', 'Organization'),
    )

    name = models.CharField(max_length=255)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    national_id = models.CharField(max_length=16, unique=True, validators=[rwanda_nid_validator])
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
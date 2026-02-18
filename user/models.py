from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'ADMIN'
    LOAN_OFFICER = 'LOAN_OFFICER'
    PROJECT_OFFICER = 'PROJECT_OFFICER'
    FINANCE_OFFICER = 'FINANCE_OFFICER'
    MANAGEMENT = 'MANAGEMENT'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LOAN_OFFICER, 'Loan Officer'),
        (PROJECT_OFFICER, 'Project Officer'),
        (FINANCE_OFFICER, 'Finance Officer'),
        (MANAGEMENT, 'Management'),
    ]

    email = models.EmailField(unique=True)  
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=LOAN_OFFICER)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} - {self.role}"

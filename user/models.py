from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('LOAN', 'Loan Officer'),
        ('PROJECT', 'Project Officer'),
        ('FINANCE', 'Finance Officer'),
        ('MANAGEMENT', 'Management'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Add these to fix the clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),  # Change this to your last migration number
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('PENDING', 'Pending'),
                    ('APPROVED', 'Approved'),
                    ('REJECTED', 'Rejected'),
                    ('ONGOING', 'Ongoing'),
                    ('COMPLETED', 'Completed'),
                ],
                default='PENDING'
            ),
        ),
    ]
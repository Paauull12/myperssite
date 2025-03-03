from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    nume_real = models.CharField(max_length=20, verbose_name="Nume Real")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    cnp_cui = models.CharField(max_length=15, unique=True, verbose_name='CNP/CUI')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='Numar telefon')
    company_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nume Companie")

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Notes(models.Model):

    NOTE_STATUS_CHOICES = (
        ('notdone', 'Neterminat'),
        ('done', 'Terminat')
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notes',
                                limit_choices_to={'user_type': 'student'})
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_notes',
                                limit_choices_to={'user_type': 'teacher'})
    title = models.CharField(max_length=120)
    note = models.TextField()
    date = models.DateTimeField(verbose_name="Data notitei")
    note_type = models.CharField(max_length=10, choices=NOTE_STATUS_CHOICES)


# mediatii/models.py
class Meditation(models.Model):
    PAYMENT_STATUS = (
        ('unpaid', 'Neplătit'),
        ('pending', 'În așteptare'),
        ('paid', 'Plătit'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_meditations',
                                limit_choices_to={'user_type': 'student'})
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_meditations',
                                limit_choices_to={'user_type': 'teacher'})
    date = models.DateTimeField(verbose_name="Data meditației")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sumă de plată")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='unpaid',
                                      verbose_name="Status plată")

    class Meta:
        verbose_name = "Meditație"
        verbose_name_plural = "Meditații"
        ordering = ['-date']
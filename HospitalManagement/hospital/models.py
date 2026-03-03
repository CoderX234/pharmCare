from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    d_dob = models.DateField()
    d_email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    d_aadhar = models.CharField(max_length=12)
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Patient(models.Model):
    # link to django user account for logins; permit existing records without
    # a user so migrations are smoother
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="patient",
        help_text="Associated auth user for this patient (username should match name)"
    )
    registrationDate = models.DateField()
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    p_dob = models.DateField()
    mobile = models.CharField(max_length=10, null=True)
    p_email = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    p_aadhar = models.CharField(max_length=12)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    bloodgroup = models.CharField(max_length=3)
    disease = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField(null=True)
    time1 = models.TimeField(max_length=150)

    def __str__(self):
        return self.doctor.name+"--"+self.patient.name


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    med = models.CharField(max_length=150)
    dnd = models.CharField(max_length=150)

    def __str__(self):
        return self.patient.name

# Create your models here.


class Profile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_DOCTOR = 'doctor'
    ROLE_NURSE = 'nurse'
    ROLE_FRONT_DESK = 'front_desk'
    ROLE_PATIENT = 'patient'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_DOCTOR, 'Doctor'),
        (ROLE_NURSE, 'Nurse'),
        (ROLE_FRONT_DESK, 'Front Desk'),
        (ROLE_PATIENT, 'Patient'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_PATIENT)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure a Profile exists for the user; if it doesn't, create one.
    try:
        instance.profile.save()
    except Exception:
        Profile.objects.get_or_create(user=instance)

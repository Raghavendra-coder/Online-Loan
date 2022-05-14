from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLES = (
        ('Admin', 'Admin'),
        ('Agent', 'Agent'),
        ('Customer', 'Customer')
    )
    role = models.CharField(max_length=8, choices=ROLES)
    mobile = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='user/images/profiles', default='user/images/profiles/profile_picture.png',
                                null=True)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=6)


class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    EDUCATION = (
        ('G', 'Graduated'),
        ('N', 'NOt Graduated'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    married = models.BooleanField()
    gender = models.CharField(max_length=1, choices=GENDER)
    dependents = models.IntegerField(default=0)
    education = models.CharField(max_length=1, choices=EDUCATION)
    self_employed = models.BooleanField()
    income = models.FloatField()
    credit_history = models.FloatField(default=1.0)


class Loan(models.Model):
    name = models.CharField(max_length=10)
    interest = models.FloatField()

    def __str__(self):
        return self.name


class UserLoan(models.Model):
    STATUS = (
        ('Nw', 'New'),
        ('Rq', 'Request'),
        ('Rj', 'Rejected'),
        ('Ap', 'Approved')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loans')
    principle = models.FloatField()
    tenure = models.FloatField()
    emi = models.FloatField(blank=True)
    loan_status = models.CharField(max_length=2, choices=STATUS, default="Nw")
    unique_together = ['user', 'loan_type']
    date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


class AccuracyTable(models.Model):
    accuracy = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

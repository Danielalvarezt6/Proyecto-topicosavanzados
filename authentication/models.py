from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='Sexo')
    age = models.PositiveIntegerField(verbose_name='Edad')
    expediente = models.CharField(max_length=20, unique=True, verbose_name='Número de expediente')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_sex_display()} - {self.age} años"

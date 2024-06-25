from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class Capteurs(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    piece = models.CharField(max_length=255, blank=True)
    emplacement = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        chaine = f"nom {self.nom}"
        return chaine
    
    class Meta:
        db_table = 'mqtt_capteurs'
    
class Donnees(models.Model):
    capteurID = models.ForeignKey(Capteurs, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    valeur = models.FloatField()

    def __str__(self):
        chaine = f"capteurID {self.capteurID}, timestamp {self.timestamp}"
        return chaine

    class Meta:
        db_table = 'mqtt_donnees'

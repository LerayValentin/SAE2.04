# myapp/serializers.py

from rest_framework import serializers
from .models import Donnees

class DonneesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donnees
        fields = ['capteurID', 'timestamp', 'valeur']

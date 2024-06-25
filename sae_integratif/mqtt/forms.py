from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Capteurs, Donnees
from django import forms


class CapteursForm(forms.ModelForm):
    class Meta:
        model = Capteurs
        fields = ('nom','emplacement')
        labels = {
            'nom': _("Nom"),
            'emplacement': _("Emplacement"),
        }

class DonneesForm(forms.ModelForm):
    class Meta:
        model = Donnees
        fields = ('capteurID', 'timestamp', 'valeur')
        labels = {
            'capteurID': _("CapteurID"),
            'timestamp': _("TimeStamp"),
            'valeur': _("Valeur"),
        }


class FiltreDonneesForm(forms.Form):
    nom_capteur = forms.CharField(label='Nom du capteur', required=False)
    capteur_id = forms.IntegerField(label='ID du capteur', required=False)
    date_debut = forms.DateField(label='Date de début', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(label='Date de fin', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

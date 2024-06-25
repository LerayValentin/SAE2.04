from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import DonneesForm, CapteursForm, FiltreDonneesForm
from mqtt import models
from .models import Donnees, Capteurs
from django.db.models import Q
from rest_framework import generics
from .serializers import DonneesSerializer
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
import csv


def index(request):
    donnees = models.Donnees.objects.all()
    return render(request, 'mqtt/index/index.html', {'donnees': donnees})


def index_capteurs(request):
    capteurs = models.Capteurs.objects.all()
    return render(request, 'mqtt/capteurs/capteurs.html', {'capteurs': capteurs})


def show_capteur(request, id):
    capteur = models.Capteurs.objects.get(id=id)
    donnees = list(models.Donnees.objects.filter(capteurID_id=id))
    return render(request, 'mqtt/capteurs/show_capteur.html', {'capteur': capteur, "donnees": donnees})



def update_capteur(request, id):
    capteur = models.Capteurs.objects.get(id=id)
    form = CapteursForm(instance=capteur)
    return render(request, 'mqtt/capteurs/update_capteur.html', {'form': form, 'capteur': capteur})


def processing_update_capteur(request, id):
    capteur = models.Capteurs.objects.get(id=id)
    form = CapteursForm(request.POST, instance=capteur)
    if form.is_valid():
        capteur = form.save(commit=False)
        capteur.id = id
        capteur.save()
        return HttpResponseRedirect("/capteurs/")
    else:
        return render(request, "'mqtt/capteurs/update_capteur.html", {"form": form, "id": id})
    

def delete_capteur(request, id):
    capteur = models.Capteurs.objects.get(id=id)
    capteur.delete()
    return HttpResponseRedirect("/capteurs/")


def index_filtre(request):
    form = FiltreDonneesForm()
    return render(request, 'mqtt/index/index_filtre.html', {'form': form})

def processing_filtre(request, id):
    form = FiltreDonneesForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data()
        return render(request, "'mqtt/index/index.html", {"form": form, 'data': data})
    else:
        return render(request, "'mqtt/index/index_filtre.html", {"form": form})
    


def donnees_view(request):
    form = FiltreDonneesForm(request.GET)
    donnees = Donnees.objects.all()

    if form.is_valid():
        capteur_id = form.cleaned_data.get('capteur_id')
        date_debut = form.cleaned_data.get('date_debut')
        date_fin = form.cleaned_data.get('date_fin')
        nom_capteur = form.cleaned_data.get('nom_capteur')  # Récupérer le nom du capteur

        if capteur_id:
            donnees = donnees.filter(Q(capteurID__id=capteur_id))

        if nom_capteur:  # Filtrer par le nom du capteur s'il est spécifié
            donnees = donnees.filter(Q(capteurID__nom__icontains=nom_capteur))

        if date_debut and date_fin:
            donnees = donnees.filter(timestamp__range=[date_debut, date_fin])

    context = {
        'form': form,
        'donnees': donnees,
    }
    return render(request, 'mqtt/index/filtre.html', context)


class DonneesList(generics.ListAPIView):
    queryset = Donnees.objects.all()
    serializer_class = DonneesSerializer

def donnees_graph(request):
    capteurs = Capteurs.objects.all()
    graphs = []

    for capteur in capteurs:
        donnees = Donnees.objects.filter(capteurID=capteur)
        timestamps = [donnee.timestamp for donnee in donnees]
        valeurs = [donnee.valeur for donnee in donnees]

        fig, ax = plt.subplots()
        ax.plot(timestamps, valeurs, marker='o', linestyle='-', color='b', label='Données')
        ax.set_xlabel('Temps')
        ax.set_ylabel('Valeur')
        ax.set_title(f'Données du Capteur {capteur.nom}')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.grid(True)

        # Ajuster la taille du graphique
        fig.set_size_inches(14, 8)

        # Convertir le graphique en image base 64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=200) 
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph = base64.b64encode(image_png).decode('utf-8')

        graphs.append({'nom': capteur.nom, 'graph': graph})

    return render(request, 'mqtt/index/donnees_graph.html', {'graphs': graphs})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donnees_capteurs.csv"'

    writer = csv.writer(response, delimiter=';')  # Utilisation du point-virgule comme délimiteur
    writer.writerow(['Nom Capteur', 'Piece', 'Emplacement', 'Timestamp', 'Valeur'])

    donnees = Donnees.objects.all()
    for donnee in donnees:
        writer.writerow([donnee.capteurID.nom, donnee.capteurID.piece, donnee.capteurID.emplacement,
                         donnee.timestamp.strftime('%Y-%m-%d %H:%M:%S'), donnee.valeur])

    return response
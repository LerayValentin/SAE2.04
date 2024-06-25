from django.urls import path
from .views import DonneesList, donnees_graph
from . import views

urlpatterns = [
    path('', views.index),
    path('capteurs/', views.index_capteurs),
    path('capteurs/update_capteur/<int:id>/', views.update_capteur),
    path('capteurs/processing_update_capteur/<int:id>/', views.processing_update_capteur),
    path('capteurs/show_capteur/<int:id>/', views.show_capteur),
    path('capteurs/delete_capteur/<int:id>/', views.delete_capteur),
    path('index/index_filtre/', views.index_filtre),
    path('filtre/', views.donnees_view),
    path('api/donnees/', DonneesList.as_view()),
    path('graph/', donnees_graph),
    path('export-csv/', views.export_csv, name='export_csv'),

]

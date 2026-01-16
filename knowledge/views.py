from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from .models import Character, Crew, DevilFruit, Arc, Episode
from .serializers import (
    CharacterListSerializer, CharacterDetailSerializer,
    CrewListSerializer, CrewDetailSerializer,
    DevilFruitListSerializer, DevilFruitDetailSerializer,
    ArcListSerializer, ArcDetailSerializer,
    EpisodeListSerializer, EpisodeDetailSerializer
)


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les personnages"""
    queryset = Character.objects.all().prefetch_related('crews', 'fruit_history__devil_fruit')
    search_fields = ['name', 'epithet', 'role', 'description']
    ordering_fields = ['id', 'name', 'bounty']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CharacterDetailSerializer
        return CharacterListSerializer


class CrewViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les équipages"""
    queryset = Crew.objects.all().prefetch_related('members')
    search_fields = ['name', 'ship_name', 'base_location']
    ordering_fields = ['id', 'name']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CrewDetailSerializer
        return CrewListSerializer


class DevilFruitViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les fruits du démon"""
    queryset = DevilFruit.objects.all().prefetch_related('holders__character')
    search_fields = ['name', 'romanji', 'ability', 'description']
    ordering_fields = ['id', 'name', 'rarity', 'fruit_type']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DevilFruitDetailSerializer
        return DevilFruitListSerializer


class ArcViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les arcs"""
    queryset = Arc.objects.all().prefetch_related('episodes')
    search_fields = ['name', 'saga', 'description']
    ordering_fields = ['id', 'name', 'start_episode_number']
    ordering = ['start_episode_number']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArcDetailSerializer
        return ArcListSerializer


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les épisodes"""
    queryset = Episode.objects.all().select_related('arc')
    search_fields = ['title']
    ordering_fields = ['number', 'title']
    ordering = ['number']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EpisodeDetailSerializer
        return EpisodeListSerializer


def admin_stats_view(request):
    """Vue admin pour les statistiques avec graphiques matplotlib"""
    if not request.user.is_staff:
        from django.contrib.auth.decorators import login_required
        from django.contrib.admin.views.decorators import staff_member_required
        return staff_member_required(login_required(lambda: None))()
    
    # Graphique 1: Répartition des fruits par type
    fruits = DevilFruit.objects.all()
    fruit_types = {}
    for fruit in fruits:
        fruit_types[fruit.get_fruit_type_display()] = fruit_types.get(fruit.get_fruit_type_display(), 0) + 1
    
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    if fruit_types:
        ax1.pie(fruit_types.values(), labels=fruit_types.keys(), autopct='%1.1f%%', startangle=90)
        ax1.set_title('Répartition des fruits du démon par type')
    else:
        ax1.text(0.5, 0.5, 'Aucune donnée disponible', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Répartition des fruits du démon par type')
    
    plt.tight_layout()
    buffer1 = BytesIO()
    plt.savefig(buffer1, format='png', dpi=100)
    buffer1.seek(0)
    image1_base64 = base64.b64encode(buffer1.getvalue()).decode()
    plt.close(fig1)
    
    # Graphique 2: Top 10 équipages par nombre de membres
    crews = Crew.objects.all()
    crew_member_counts = []
    for crew in crews:
        member_count = crew.members.count()
        crew_member_counts.append((crew.name, member_count))
    
    crew_member_counts.sort(key=lambda x: x[1], reverse=True)
    top_10 = crew_member_counts[:10]
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    if top_10:
        names = [c[0] for c in top_10]
        counts = [c[1] for c in top_10]
        ax2.barh(names, counts)
        ax2.set_xlabel('Nombre de membres')
        ax2.set_title('Top 10 équipages par nombre de membres')
        ax2.invert_yaxis()
    else:
        ax2.text(0.5, 0.5, 'Aucune donnée disponible', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Top 10 équipages par nombre de membres')
    
    plt.tight_layout()
    buffer2 = BytesIO()
    plt.savefig(buffer2, format='png', dpi=100)
    buffer2.seek(0)
    image2_base64 = base64.b64encode(buffer2.getvalue()).decode()
    plt.close(fig2)
    
    return render(request, 'admin/stats.html', {
        'graph1': image1_base64,
        'graph2': image2_base64,
    })


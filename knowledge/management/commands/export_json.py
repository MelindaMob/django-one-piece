from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from io import StringIO
import os
import json
from datetime import datetime

from knowledge.models import Character, Crew, DevilFruit, Arc, Episode, FruitHolder


class Command(BaseCommand):
    help = 'Exporte toutes les données en JSON dans le dossier /exports'

    def handle(self, *args, **options):
        # Créer le dossier exports s'il n'existe pas
        exports_dir = os.path.join(settings.BASE_DIR, 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Exporter chaque modèle
        models_to_export = [
            ('knowledge.Arc', 'arcs'),
            ('knowledge.Episode', 'episodes'),
            ('knowledge.Crew', 'crews'),
            ('knowledge.Character', 'characters'),
            ('knowledge.DevilFruit', 'devil_fruits'),
            ('knowledge.FruitHolder', 'fruit_holders'),
        ]
        
        all_data = {}
        
        for model_path, key in models_to_export:
            self.stdout.write(f'Export de {key}...')
            output = StringIO()
            call_command('dumpdata', model_path, stdout=output, indent=2)
            output.seek(0)
            content = output.getvalue()
            if content.strip():
                data = json.loads(content)
                all_data[key] = data
            else:
                all_data[key] = []
        
        # Sauvegarder dans un fichier unique
        filename = os.path.join(exports_dir, f'opkb_export_{timestamp}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(self.style.SUCCESS(f'Export terminé: {filename}'))
        
        # Afficher les statistiques
        self.stdout.write('\nStatistiques:')
        self.stdout.write(f'  - Arcs: {Arc.objects.count()}')
        self.stdout.write(f'  - Épisodes: {Episode.objects.count()}')
        self.stdout.write(f'  - Équipages: {Crew.objects.count()}')
        self.stdout.write(f'  - Personnages: {Character.objects.count()}')
        self.stdout.write(f'  - Fruits du démon: {DevilFruit.objects.count()}')
        self.stdout.write(f'  - Détenteurs: {FruitHolder.objects.count()}')


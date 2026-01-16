from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random

from knowledge.models import Character, Crew, DevilFruit, Arc, Episode, FruitHolder


# Données réelles One Piece
ONE_PIECE_CHARACTERS = [
    {'name': 'Monkey D. Luffy', 'epithet': 'Chapeau de Paille', 'role': 'PIRATE', 'bounty': 3000000000, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Roronoa Zoro', 'epithet': 'Chasseur de Pirates', 'role': 'PIRATE', 'bounty': 1111000000, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Nami', 'epithet': 'La Chatte Voleuse', 'role': 'PIRATE', 'bounty': 366000000, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Usopp', 'epithet': 'Dieu', 'role': 'PIRATE', 'bounty': 500000000, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Sanji', 'epithet': 'Pied Noir', 'role': 'PIRATE', 'bounty': 1032000000, 'origin': 'North Blue', 'status': 'ALIVE'},
    {'name': 'Tony Tony Chopper', 'epithet': 'Amant du Coton', 'role': 'PIRATE', 'bounty': 1000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Nico Robin', 'epithet': 'Enfant Démoniaque', 'role': 'PIRATE', 'bounty': 930000000, 'origin': 'West Blue', 'status': 'ALIVE'},
    {'name': 'Franky', 'epithet': 'Cyborg', 'role': 'PIRATE', 'bounty': 394000000, 'origin': 'South Blue', 'status': 'ALIVE'},
    {'name': 'Brook', 'epithet': 'Chanteur', 'role': 'PIRATE', 'bounty': 383000000, 'origin': 'West Blue', 'status': 'ALIVE'},
    {'name': 'Jinbe', 'epithet': 'Chevalier des Mers', 'role': 'PIRATE', 'bounty': 1100000000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Shanks', 'epithet': 'Le Roux', 'role': 'PIRATE', 'bounty': 4048900000, 'origin': 'West Blue', 'status': 'ALIVE'},
    {'name': 'Marshall D. Teach', 'epithet': 'Barbe Noire', 'role': 'PIRATE', 'bounty': 3996000000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Boa Hancock', 'epithet': 'Impératrice Serpent', 'role': 'PIRATE', 'bounty': 1659000000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Buggy', 'epithet': 'Le Clown', 'role': 'PIRATE', 'bounty': 3189000000, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Trafalgar D. Water Law', 'epithet': 'Le Chirurgien de la Mort', 'role': 'PIRATE', 'bounty': 3000000000, 'origin': 'North Blue', 'status': 'ALIVE'},
    {'name': 'Eustass Kid', 'epithet': 'Le Capitaine', 'role': 'PIRATE', 'bounty': 3000000000, 'origin': 'South Blue', 'status': 'ALIVE'},
    {'name': 'Monkey D. Garp', 'epithet': 'Le Poing', 'role': 'MARINE', 'bounty': 0, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Sakazuki', 'epithet': 'Akainu', 'role': 'MARINE', 'bounty': 0, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Borsalino', 'epithet': 'Kizaru', 'role': 'MARINE', 'bounty': 0, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Issho', 'epithet': 'Fujitora', 'role': 'MARINE', 'bounty': 0, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Monkey D. Dragon', 'epithet': 'Le Révolutionnaire', 'role': 'REVOLUTIONARY', 'bounty': 0, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Sabo', 'epithet': 'La Flamme', 'role': 'REVOLUTIONARY', 'bounty': 602000000, 'origin': 'East Blue', 'status': 'ALIVE'},
    {'name': 'Portgas D. Ace', 'epithet': 'Le Poing de Feu', 'role': 'PIRATE', 'bounty': 550000000, 'origin': 'South Blue', 'status': 'DEAD'},
    {'name': 'Gol D. Roger', 'epithet': 'Le Roi des Pirates', 'role': 'PIRATE', 'bounty': 5564800000, 'origin': 'East Blue', 'status': 'DEAD'},
    {'name': 'Edward Newgate', 'epithet': 'Barbe Blanche', 'role': 'PIRATE', 'bounty': 5046000000, 'origin': 'Grand Line', 'status': 'DEAD'},
    {'name': 'Kaido', 'epithet': 'La Créature', 'role': 'PIRATE', 'bounty': 4611100000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Charlotte Linlin', 'epithet': 'Big Mom', 'role': 'PIRATE', 'bounty': 4388000000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Dracule Mihawk', 'epithet': 'Œil de Faucon', 'role': 'PIRATE', 'bounty': 3590000000, 'origin': 'Grand Line', 'status': 'ALIVE'},
    {'name': 'Donquixote Doflamingo', 'epithet': 'Joker', 'role': 'PIRATE', 'bounty': 340000000, 'origin': 'North Blue', 'status': 'ALIVE'},
    {'name': 'Crocodile', 'epithet': 'Sirène', 'role': 'PIRATE', 'bounty': 1965000000, 'origin': 'Grand Line', 'status': 'ALIVE'},
]

ONE_PIECE_CREWS = [
    {'name': 'Équipage du Chapeau de Paille', 'ship_name': 'Thousand Sunny', 'base_location': 'Grand Line'},
    {'name': 'Équipage de Barbe Rouge', 'ship_name': 'Moby Dick', 'base_location': 'New World'},
    {'name': 'Équipage de Barbe Noire', 'ship_name': 'Sabre de Xebec', 'base_location': 'New World'},
    {'name': 'Équipage du Chapeau de Paille (Heart)', 'ship_name': 'Polar Tang', 'base_location': 'New World'},
    {'name': 'Équipage de Kid', 'ship_name': 'Victoria Punk', 'base_location': 'New World'},
    {'name': 'Équipage de Big Mom', 'ship_name': 'Queen Mama Chanter', 'base_location': 'New World'},
    {'name': 'Équipage de Kaido', 'ship_name': 'Mammoth', 'base_location': 'New World'},
    {'name': 'Équipage de Buggy', 'ship_name': 'Big Top', 'base_location': 'Grand Line'},
    {'name': 'Équipage de Crocodile', 'ship_name': 'Banana Gator', 'base_location': 'Grand Line'},
    {'name': 'Équipage de Donquixote', 'ship_name': 'Numancia Flamingo', 'base_location': 'New World'},
    {'name': 'Équipage de Shanks', 'ship_name': 'Red Force', 'base_location': 'New World'},
    {'name': 'Équipage de Kuja', 'ship_name': 'Perfume Yuda', 'base_location': 'Grand Line'},
    {'name': 'Équipage de Jinbe', 'ship_name': 'Shark Superb', 'base_location': 'Grand Line'},
]

ONE_PIECE_FRUITS = [
    {'name': 'Gomu Gomu no Mi', 'romanji': 'Gomu Gomu no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet au corps de s\'étirer comme du caoutchouc', 'rarity': 3, 'status': 'ACTIVE'},
    {'name': 'Mera Mera no Mi', 'romanji': 'Mera Mera no Mi', 'fruit_type': 'LOGIA', 'ability': 'Permet de créer et contrôler le feu', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Magu Magu no Mi', 'romanji': 'Magu Magu no Mi', 'fruit_type': 'LOGIA', 'ability': 'Permet de créer et contrôler le magma', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Pika Pika no Mi', 'romanji': 'Pika Pika no Mi', 'fruit_type': 'LOGIA', 'ability': 'Permet de créer et contrôler la lumière', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Hana Hana no Mi', 'romanji': 'Hana Hana no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de faire pousser des parties du corps n\'importe où', 'rarity': 4, 'status': 'ACTIVE'},
    {'name': 'Yami Yami no Mi', 'romanji': 'Yami Yami no Mi', 'fruit_type': 'LOGIA', 'ability': 'Permet de créer et contrôler les ténèbres', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Gura Gura no Mi', 'romanji': 'Gura Gura no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de créer des tremblements de terre', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Ope Ope no Mi', 'romanji': 'Ope Ope no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de créer une zone où on peut tout manipuler', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Mero Mero no Mi', 'romanji': 'Mero Mero no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de transformer les gens en pierre', 'rarity': 4, 'status': 'ACTIVE'},
    {'name': 'Suna Suna no Mi', 'romanji': 'Suna Suna no Mi', 'fruit_type': 'LOGIA', 'ability': 'Permet de créer et contrôler le sable', 'rarity': 4, 'status': 'ACTIVE'},
    {'name': 'Ito Ito no Mi', 'romanji': 'Ito Ito no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de créer et manipuler des fils', 'rarity': 4, 'status': 'ACTIVE'},
    {'name': 'Hito Hito no Mi', 'romanji': 'Hito Hito no Mi', 'fruit_type': 'ZOAN', 'ability': 'Permet de se transformer en humain', 'rarity': 3, 'status': 'ACTIVE'},
    {'name': 'Hito Hito no Mi, Modèle: Bouddha', 'romanji': 'Hito Hito no Mi, Modèle: Daibutsu', 'fruit_type': 'ZOAN', 'ability': 'Permet de se transformer en Bouddha géant', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Uo Uo no Mi, Modèle: Seiryu', 'romanji': 'Uo Uo no Mi, Modèle: Seiryu', 'fruit_type': 'ZOAN', 'ability': 'Permet de se transformer en dragon azur', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Soru Soru no Mi', 'romanji': 'Soru Soru no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de manipuler les âmes', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Yomi Yomi no Mi', 'romanji': 'Yomi Yomi no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de revenir à la vie après la mort', 'rarity': 5, 'status': 'ACTIVE'},
    {'name': 'Suke Suke no Mi', 'romanji': 'Suke Suke no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de devenir invisible', 'rarity': 3, 'status': 'ACTIVE'},
    {'name': 'Bara Bara no Mi', 'romanji': 'Bara Bara no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de séparer son corps en morceaux', 'rarity': 2, 'status': 'ACTIVE'},
    {'name': 'Supa Supa no Mi', 'romanji': 'Supa Supa no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de transformer ses membres en lames', 'rarity': 3, 'status': 'ACTIVE'},
    {'name': 'Kilo Kilo no Mi', 'romanji': 'Kilo Kilo no Mi', 'fruit_type': 'PARAMECIA', 'ability': 'Permet de changer son poids', 'rarity': 2, 'status': 'ACTIVE'},
]

ONE_PIECE_ARCS = [
    {'name': 'Romance Dawn', 'saga': 'East Blue', 'start': 1, 'end': 3},
    {'name': 'Orange Town', 'saga': 'East Blue', 'start': 4, 'end': 8},
    {'name': 'Village de Sirop', 'saga': 'East Blue', 'start': 9, 'end': 18},
    {'name': 'Baratie', 'saga': 'East Blue', 'start': 19, 'end': 30},
    {'name': 'Arlong Park', 'saga': 'East Blue', 'start': 31, 'end': 44},
    {'name': 'Loguetown', 'saga': 'East Blue', 'start': 45, 'end': 53},
    {'name': 'Rêve de Barbe Blanche', 'saga': 'East Blue', 'start': 54, 'end': 61},
    {'name': 'Alabasta', 'saga': 'Alabasta', 'start': 62, 'end': 130},
    {'name': 'Jaya', 'saga': 'Sky Island', 'start': 144, 'end': 152},
    {'name': 'Skypiea', 'saga': 'Sky Island', 'start': 153, 'end': 195},
    {'name': 'Long Ring Long Land', 'saga': 'Water 7', 'start': 207, 'end': 219},
    {'name': 'Water 7', 'saga': 'Water 7', 'start': 229, 'end': 263},
    {'name': 'Enies Lobby', 'saga': 'Water 7', 'start': 264, 'end': 312},
    {'name': 'Post-Enies Lobby', 'saga': 'Water 7', 'start': 313, 'end': 325},
    {'name': 'Thriller Bark', 'saga': 'Thriller Bark', 'start': 337, 'end': 381},
    {'name': 'Archipel Sabaody', 'saga': 'Summit War', 'start': 385, 'end': 405},
    {'name': 'Amazon Lily', 'saga': 'Summit War', 'start': 408, 'end': 417},
    {'name': 'Impel Down', 'saga': 'Summit War', 'start': 422, 'end': 452},
    {'name': 'Marineford', 'saga': 'Summit War', 'start': 457, 'end': 489},
    {'name': 'Post-Guerre', 'saga': 'Summit War', 'start': 490, 'end': 516},
    {'name': 'Île des Hommes-Poissons', 'saga': 'New World', 'start': 523, 'end': 574},
    {'name': 'Punk Hazard', 'saga': 'New World', 'start': 579, 'end': 628},
    {'name': 'Dressrosa', 'saga': 'New World', 'start': 629, 'end': 746},
    {'name': 'Zou', 'saga': 'New World', 'start': 751, 'end': 802},
    {'name': 'Whole Cake Island', 'saga': 'New World', 'start': 825, 'end': 902},
    {'name': 'Reverie', 'saga': 'New World', 'start': 903, 'end': 908},
    {'name': 'Pays de Wano', 'saga': 'Wano', 'start': 909, 'end': 1057},
]


class Command(BaseCommand):
    help = 'Génère des données One Piece pour One Piece Knowledge Base'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Vider toutes les tables avant de générer')
        parser.add_argument('--characters', type=int, default=0, help='Nombre de personnages à créer (0 = tous)')
        parser.add_argument('--crews', type=int, default=0, help='Nombre d\'équipages à créer (0 = tous)')
        parser.add_argument('--fruits', type=int, default=0, help='Nombre de fruits à créer (0 = tous)')
        parser.add_argument('--arcs', type=int, default=0, help='Nombre d\'arcs à créer (0 = tous)')
        parser.add_argument('--episodes', type=int, default=200, help='Nombre d\'épisodes à créer')

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Suppression de toutes les données...'))
            FruitHolder.objects.all().delete()
            Character.objects.all().delete()
            Crew.objects.all().delete()
            DevilFruit.objects.all().delete()
            Episode.objects.all().delete()
            Arc.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Données supprimées'))

        # Créer les arcs
        self.stdout.write('Création des arcs...')
        arcs = []
        num_arcs = options['arcs'] if options['arcs'] > 0 else len(ONE_PIECE_ARCS)
        selected_arcs = ONE_PIECE_ARCS[:num_arcs] if num_arcs <= len(ONE_PIECE_ARCS) else ONE_PIECE_ARCS
        
        for arc_data in selected_arcs:
            arc = Arc.objects.create(
                name=arc_data['name'],
                saga=arc_data['saga'],
                start_episode_number=arc_data['start'],
                end_episode_number=arc_data['end'],
                description=f"Arc {arc_data['name']} de la saga {arc_data['saga']}"
            )
            arcs.append(arc)
        
        self.stdout.write(self.style.SUCCESS(f'{len(arcs)} arcs créés'))

        # Créer les épisodes
        self.stdout.write('Création des épisodes...')
        episodes = []
        for i in range(options['episodes']):
            # Trouver l'arc correspondant
            arc = None
            for a in arcs:
                if a.start_episode_number <= (i + 1) <= a.end_episode_number:
                    arc = a
                    break
            
            episode = Episode.objects.create(
                number=i + 1,
                title=f"Épisode {i + 1}",
                air_date=None,
                arc=arc
            )
            episodes.append(episode)
        
        self.stdout.write(self.style.SUCCESS(f'{len(episodes)} épisodes créés'))

        # Créer les fruits du démon
        self.stdout.write('Création des fruits du démon...')
        fruits = []
        num_fruits = options['fruits'] if options['fruits'] > 0 else len(ONE_PIECE_FRUITS)
        selected_fruits = ONE_PIECE_FRUITS[:num_fruits] if num_fruits <= len(ONE_PIECE_FRUITS) else ONE_PIECE_FRUITS
        
        for fruit_data in selected_fruits:
            fruit = DevilFruit.objects.create(
                name=fruit_data['name'],
                romanji=fruit_data.get('romanji', ''),
                fruit_type=fruit_data['fruit_type'],
                ability=fruit_data['ability'],
                weaknesses='Eau de mer' if random.random() > 0.3 else '',
                rarity=fruit_data['rarity'],
                status=fruit_data['status'],
                first_appearance_arc=random.choice(arcs) if arcs and random.random() > 0.5 else None,
                description=f"Fruit du démon de type {fruit_data['fruit_type']}"
            )
            fruits.append(fruit)
        
        self.stdout.write(self.style.SUCCESS(f'{len(fruits)} fruits créés'))

        # Créer les équipages
        self.stdout.write('Création des équipages...')
        crews = []
        num_crews = options['crews'] if options['crews'] > 0 else len(ONE_PIECE_CREWS)
        selected_crews = ONE_PIECE_CREWS[:num_crews] if num_crews <= len(ONE_PIECE_CREWS) else ONE_PIECE_CREWS
        
        for crew_data in selected_crews:
            crew = Crew.objects.create(
                name=crew_data['name'],
                ship_name=crew_data.get('ship_name', ''),
                base_location=crew_data.get('base_location', ''),
                description=f"Équipage de pirates célèbre"
            )
            crews.append(crew)
        
        self.stdout.write(self.style.SUCCESS(f'{len(crews)} équipages créés'))

        # Créer les personnages
        self.stdout.write('Création des personnages...')
        characters = []
        num_chars = options['characters'] if options['characters'] > 0 else len(ONE_PIECE_CHARACTERS)
        selected_chars = ONE_PIECE_CHARACTERS[:num_chars] if num_chars <= len(ONE_PIECE_CHARACTERS) else ONE_PIECE_CHARACTERS
        
        for char_data in selected_chars:
            character = Character.objects.create(
                name=char_data['name'],
                epithet=char_data.get('epithet', ''),
                role=char_data['role'],
                bounty=char_data.get('bounty', 0),
                origin=char_data.get('origin', ''),
                status=char_data.get('status', 'ALIVE'),
                first_appearance_episode=random.choice(episodes[:100]) if episodes and random.random() > 0.3 else None,
                description=f"Personnage de One Piece",
                image_url=''
            )
            characters.append(character)
        
        self.stdout.write(self.style.SUCCESS(f'{len(characters)} personnages créés'))

        # Assigner des capitaines aux équipages
        self.stdout.write('Assignation des capitaines...')
        crew_captains = {
            'Équipage du Chapeau de Paille': 'Monkey D. Luffy',
            'Équipage de Barbe Rouge': 'Edward Newgate',
            'Équipage de Barbe Noire': 'Marshall D. Teach',
            'Équipage du Chapeau de Paille (Heart)': 'Trafalgar D. Water Law',
            'Équipage de Kid': 'Eustass Kid',
            'Équipage de Big Mom': 'Charlotte Linlin',
            'Équipage de Kaido': 'Kaido',
            'Équipage de Buggy': 'Buggy',
            'Équipage de Crocodile': 'Crocodile',
            'Équipage de Donquixote': 'Donquixote Doflamingo',
            'Équipage de Shanks': 'Shanks',
            'Équipage de Kuja': 'Boa Hancock',
        }
        
        for crew in crews:
            captain_name = crew_captains.get(crew.name)
            if captain_name:
                captain = next((c for c in characters if c.name == captain_name), None)
                if captain:
                    crew.captain = captain
                    crew.save()

        # Assigner des personnages aux équipages (assignations cohérentes)
        self.stdout.write('Assignation des membres aux équipages...')
        
        # Définir les membres de chaque équipage
        crew_members_map = {
            'Équipage du Chapeau de Paille': ['Monkey D. Luffy', 'Roronoa Zoro', 'Nami', 'Usopp', 'Sanji', 'Tony Tony Chopper', 'Nico Robin', 'Franky', 'Brook', 'Jinbe'],
            'Équipage de Barbe Rouge': ['Edward Newgate'],  # Seulement le capitaine pour éviter les erreurs
            'Équipage de Barbe Noire': ['Marshall D. Teach'],  # Seulement le capitaine
            'Équipage du Chapeau de Paille (Heart)': ['Trafalgar D. Water Law'],  # Seulement le capitaine
            'Équipage de Kid': ['Eustass Kid'],  # Seulement le capitaine
            'Équipage de Big Mom': ['Charlotte Linlin'],  # Seulement le capitaine
            'Équipage de Kaido': ['Kaido'],  # Seulement le capitaine
            'Équipage de Buggy': ['Buggy'],  # Seulement le capitaine
            'Équipage de Crocodile': ['Crocodile'],  # Seulement le capitaine
            'Équipage de Donquixote': ['Donquixote Doflamingo'],  # Seulement le capitaine
            'Équipage de Shanks': ['Shanks'],  # Seulement le capitaine
            'Équipage de Kuja': ['Boa Hancock'],  # Seulement le capitaine
            'Équipage de Jinbe': ['Jinbe'],  # Seulement le capitaine
        }
        
        # Assigner les membres selon le mapping
        for crew in crews:
            member_names = crew_members_map.get(crew.name, [])
            if member_names:
                crew_members = [c for c in characters if c.name in member_names]
                if crew_members:
                    crew.members.set(crew_members)
                    self.stdout.write(f'  - {crew.name}: {len(crew_members)} membres assignés')

        # Créer des FruitHolders (assignations réelles)
        self.stdout.write('Création des détenteurs de fruits...')
        fruit_holders_map = {
            'Gomu Gomu no Mi': 'Monkey D. Luffy',
            'Mera Mera no Mi': 'Portgas D. Ace',
            'Magu Magu no Mi': 'Sakazuki',
            'Pika Pika no Mi': 'Borsalino',
            'Hana Hana no Mi': 'Nico Robin',
            'Yami Yami no Mi': 'Marshall D. Teach',
            'Gura Gura no Mi': 'Edward Newgate',
            'Ope Ope no Mi': 'Trafalgar D. Water Law',
            'Mero Mero no Mi': 'Boa Hancock',
            'Suna Suna no Mi': 'Crocodile',
            'Ito Ito no Mi': 'Donquixote Doflamingo',
            'Hito Hito no Mi': 'Tony Tony Chopper',
            'Soru Soru no Mi': 'Charlotte Linlin',
            'Yomi Yomi no Mi': 'Brook',
            'Suke Suke no Mi': 'Absalom',
            'Bara Bara no Mi': 'Buggy',
        }
        
        for fruit in fruits:
            holder_name = fruit_holders_map.get(fruit.name)
            if holder_name:
                holder = next((c for c in characters if c.name == holder_name), None)
                if holder:
                    FruitHolder.objects.create(
                        devil_fruit=fruit,
                        character=holder,
                        from_date=None,
                        to_date=None,
                        is_current=True
                    )

        self.stdout.write(self.style.SUCCESS('Données générées avec succès!'))
        self.stdout.write(f'Résumé: {len(characters)} personnages, {len(crews)} équipages, {len(fruits)} fruits, {len(arcs)} arcs, {len(episodes)} épisodes')

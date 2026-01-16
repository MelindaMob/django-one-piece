from rest_framework import serializers
from .models import Character, Crew, DevilFruit, Arc, Episode, FruitHolder


class EpisodeListSerializer(serializers.ModelSerializer):
    """Serializer pour liste d'épisodes"""
    class Meta:
        model = Episode
        fields = ['id', 'number', 'title', 'air_date']


class EpisodeDetailSerializer(serializers.ModelSerializer):
    """Serializer pour détail d'épisode"""
    arc = serializers.StringRelatedField()
    
    class Meta:
        model = Episode
        fields = ['id', 'number', 'title', 'air_date', 'arc']


class ArcListSerializer(serializers.ModelSerializer):
    """Serializer pour liste d'arcs"""
    class Meta:
        model = Arc
        fields = ['id', 'name', 'saga', 'start_episode_number', 'end_episode_number']


class ArcDetailSerializer(serializers.ModelSerializer):
    """Serializer pour détail d'arc avec épisodes"""
    episodes = EpisodeListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Arc
        fields = ['id', 'name', 'saga', 'start_episode_number', 'end_episode_number', 'description', 'episodes']


class CrewListSerializer(serializers.ModelSerializer):
    """Serializer pour liste d'équipages"""
    class Meta:
        model = Crew
        fields = ['id', 'name', 'ship_name']


class CrewDetailSerializer(serializers.ModelSerializer):
    """Serializer pour détail d'équipage avec membres"""
    members = serializers.SerializerMethodField()
    captain = serializers.SerializerMethodField()
    
    class Meta:
        model = Crew
        fields = ['id', 'name', 'ship_name', 'base_location', 'description', 'captain', 'members']
    
    def get_captain(self, obj):
        if obj.captain:
            return {'id': obj.captain.id, 'name': obj.captain.name}
        return None
    
    def get_members(self, obj):
        members = obj.members.all()
        return [{'id': m.id, 'name': m.name, 'bounty': m.bounty} for m in members]


class DevilFruitListSerializer(serializers.ModelSerializer):
    """Serializer pour liste de fruits"""
    class Meta:
        model = DevilFruit
        fields = ['id', 'name', 'romanji', 'fruit_type', 'rarity']


class DevilFruitDetailSerializer(serializers.ModelSerializer):
    """Serializer pour détail de fruit avec détenteurs"""
    holders = serializers.SerializerMethodField()
    first_appearance_arc = serializers.SerializerMethodField()
    
    class Meta:
        model = DevilFruit
        fields = ['id', 'name', 'romanji', 'fruit_type', 'ability', 'weaknesses', 
                 'rarity', 'status', 'first_appearance_arc', 'description', 'holders']
    
    def get_first_appearance_arc(self, obj):
        if obj.first_appearance_arc:
            return {'id': obj.first_appearance_arc.id, 'name': obj.first_appearance_arc.name}
        return None
    
    def get_holders(self, obj):
        holders = obj.holders.all()
        return [{
            'id': h.id,
            'character': {'id': h.character.id, 'name': h.character.name},
            'from_date': h.from_date,
            'to_date': h.to_date,
            'is_current': h.is_current
        } for h in holders]


class CharacterListSerializer(serializers.ModelSerializer):
    """Serializer pour liste de personnages"""
    crews = CrewListSerializer(many=True, read_only=True)
    current_fruits = serializers.SerializerMethodField()
    
    class Meta:
        model = Character
        fields = ['id', 'name', 'epithet', 'role', 'bounty', 'origin', 'status', 'crews', 'current_fruits']
    
    def get_current_fruits(self, obj):
        current_holders = FruitHolder.objects.filter(character=obj, is_current=True)
        return [{'id': h.devil_fruit.id, 'name': h.devil_fruit.name} for h in current_holders]


class CharacterDetailSerializer(serializers.ModelSerializer):
    """Serializer pour détail de personnage"""
    crews = CrewDetailSerializer(many=True, read_only=True)
    fruits_history = serializers.SerializerMethodField()
    first_appearance_episode = serializers.SerializerMethodField()
    
    class Meta:
        model = Character
        fields = ['id', 'name', 'epithet', 'role', 'bounty', 'origin', 'status',
                 'first_appearance_episode', 'description', 'image_url', 'crews', 'fruits_history']
    
    def get_fruits_history(self, obj):
        holders = obj.fruit_history.all()
        return [{
            'id': h.id,
            'devil_fruit': {'id': h.devil_fruit.id, 'name': h.devil_fruit.name, 'fruit_type': h.devil_fruit.fruit_type},
            'from_date': h.from_date,
            'to_date': h.to_date,
            'is_current': h.is_current
        } for h in holders]
    
    def get_first_appearance_episode(self, obj):
        if obj.first_appearance_episode:
            return {
                'number': obj.first_appearance_episode.number,
                'title': obj.first_appearance_episode.title,
                'arc': obj.first_appearance_episode.arc.name if obj.first_appearance_episode.arc else None
            }
        return None


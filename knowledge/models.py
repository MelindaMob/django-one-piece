from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Arc(models.Model):
    """Arc narratif de One Piece"""
    name = models.CharField(max_length=200, unique=True)
    saga = models.CharField(max_length=200, blank=True)
    start_episode_number = models.IntegerField(default=1)
    end_episode_number = models.IntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['start_episode_number']

    def __str__(self):
        return self.name


class Episode(models.Model):
    """Épisode de One Piece"""
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    air_date = models.DateField(null=True, blank=True)
    arc = models.ForeignKey(Arc, on_delete=models.SET_NULL, null=True, blank=True, related_name='episodes')

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"#{self.number} - {self.title}"


class Crew(models.Model):
    """Équipage de pirates"""
    name = models.CharField(max_length=200, unique=True)
    ship_name = models.CharField(max_length=200, blank=True)
    base_location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    captain = models.ForeignKey('Character', on_delete=models.SET_NULL, null=True, blank=True, related_name='captain_of')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Character(models.Model):
    """Personnage de One Piece"""
    class Role(models.TextChoices):
        PIRATE = 'PIRATE', _('Pirate')
        MARINE = 'MARINE', _('Marine')
        REVOLUTIONARY = 'REVOLUTIONARY', _('Révolutionnaire')
        CIVILIAN = 'CIVILIAN', _('Civil')
        OTHER = 'OTHER', _('Autre')

    class Status(models.TextChoices):
        ALIVE = 'ALIVE', _('Vivant')
        DEAD = 'DEAD', _('Mort')
        UNKNOWN = 'UNKNOWN', _('Inconnu')

    name = models.CharField(max_length=200, unique=True)
    epithet = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OTHER)
    bounty = models.IntegerField(default=0)
    origin = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ALIVE)
    first_appearance_episode = models.ForeignKey(
        Episode, on_delete=models.SET_NULL, null=True, blank=True, related_name='characters_first_appearance'
    )
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    crews = models.ManyToManyField(Crew, related_name='members', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DevilFruit(models.Model):
    """Fruit du démon"""
    class FruitType(models.TextChoices):
        PARAMECIA = 'PARAMECIA', _('Paramecia')
        ZOAN = 'ZOAN', _('Zoan')
        LOGIA = 'LOGIA', _('Logia')

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Actif')
        LOST = 'LOST', _('Perdu')
        UNKNOWN = 'UNKNOWN', _('Inconnu')

    name = models.CharField(max_length=200, unique=True)
    romanji = models.CharField(max_length=200, blank=True)
    fruit_type = models.CharField(max_length=20, choices=FruitType.choices, default=FruitType.PARAMECIA)
    ability = models.TextField()
    weaknesses = models.TextField(blank=True)
    rarity = models.IntegerField(default=3)  # 1-5
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    first_appearance_arc = models.ForeignKey(Arc, on_delete=models.SET_NULL, null=True, blank=True, related_name='fruits')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.rarity < 1 or self.rarity > 5:
            raise ValidationError({'rarity': 'La rareté doit être entre 1 et 5'})


class FruitHolder(models.Model):
    """Historique des détenteurs de fruits du démon"""
    devil_fruit = models.ForeignKey(DevilFruit, on_delete=models.CASCADE, related_name='holders')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='fruit_history')
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_current', '-from_date']

    def __str__(self):
        return f"{self.character.name} - {self.devil_fruit.name}"

    def clean(self):
        # Vérifier qu'un seul holder est actuel par fruit
        if self.is_current:
            existing_current = FruitHolder.objects.filter(
                devil_fruit=self.devil_fruit,
                is_current=True
            ).exclude(pk=self.pk if self.pk else None)
            if existing_current.exists():
                raise ValidationError(
                    {'is_current': 'Un seul détenteur actuel est autorisé par fruit du démon'}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        # Si on définit un nouveau holder comme actuel, désactiver les autres
        if self.is_current:
            FruitHolder.objects.filter(
                devil_fruit=self.devil_fruit,
                is_current=True
            ).exclude(pk=self.pk if self.pk else None).update(is_current=False)
        super().save(*args, **kwargs)


from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import csv
from io import BytesIO
from datetime import datetime

from .models import Character, Crew, Arc, Episode, DevilFruit, FruitHolder


class EpisodeInline(admin.TabularInline):
    """Inline pour les épisodes dans Arc"""
    model = Episode
    extra = 1
    fields = ['number', 'title', 'air_date']


class FruitHolderInline(admin.TabularInline):
    """Inline pour les détenteurs de fruits"""
    model = FruitHolder
    extra = 1
    fields = ['character', 'from_date', 'to_date', 'is_current']


@admin.register(Arc)
class ArcAdmin(admin.ModelAdmin):
    list_display = ['name', 'saga', 'start_episode_number', 'end_episode_number']
    list_filter = ['saga']
    search_fields = ['name', 'saga', 'description']
    ordering = ['start_episode_number']
    inlines = [EpisodeInline]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'arc', 'air_date']
    list_filter = ['arc', 'air_date']
    search_fields = ['title']
    ordering = ['number']


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ['name', 'ship_name', 'base_location', 'captain', 'member_count']
    list_filter = ['base_location']
    search_fields = ['name', 'ship_name', 'base_location']
    ordering = ['name']
    filter_horizontal = ['members']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Nombre de membres'


@admin.register(DevilFruit)
class DevilFruitAdmin(admin.ModelAdmin):
    list_display = ['name', 'romanji', 'fruit_type', 'rarity', 'status']
    list_filter = ['fruit_type', 'status', 'rarity']
    search_fields = ['name', 'romanji', 'ability', 'description']
    ordering = ['name']
    inlines = [FruitHolderInline]
    
    actions = ['export_pdf', 'export_csv']
    
    def export_pdf(self, request, queryset):
        """Export PDF pour les fruits du démon"""
        if queryset.count() != 1:
            self.message_user(request, "Veuillez sélectionner exactement un fruit du démon.", level='error')
            return
        
        fruit = queryset.first()
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        )
        
        # Titre
        story.append(Paragraph(f"Fiche Fruit du Démon: {fruit.name}", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Informations principales
        data = [
            ['Nom', fruit.name],
            ['Romanji', fruit.romanji or 'N/A'],
            ['Type', fruit.get_fruit_type_display()],
            ['Rareté', str(fruit.rarity) + '/5'],
            ['Statut', fruit.get_status_display()],
        ]
        
        if fruit.first_appearance_arc:
            data.append(['Première apparition', fruit.first_appearance_arc.name])
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Capacité
        story.append(Paragraph("Capacité", heading_style))
        story.append(Paragraph(fruit.ability, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Faiblesses
        if fruit.weaknesses:
            story.append(Paragraph("Faiblesses", heading_style))
            story.append(Paragraph(fruit.weaknesses, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Description
        if fruit.description:
            story.append(Paragraph("Description", heading_style))
            story.append(Paragraph(fruit.description, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Détenteurs
        holders = fruit.holders.all().order_by('-is_current', '-from_date')
        if holders:
            story.append(Paragraph("Détenteurs", heading_style))
            holder_data = [['Personnage', 'Date début', 'Date fin', 'Actuel']]
            for holder in holders:
                holder_data.append([
                    holder.character.name,
                    str(holder.from_date) if holder.from_date else 'N/A',
                    str(holder.to_date) if holder.to_date else 'N/A',
                    'Oui' if holder.is_current else 'Non'
                ])
            holder_table = Table(holder_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
            holder_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(holder_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Date de génération
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            f"<i>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</i>",
            styles['Normal']
        ))
        
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="fruit_{fruit.name.replace(" ", "_")}.pdf"'
        return response
    
    export_pdf.short_description = "Exporter fiche PDF"
    
    def export_csv(self, request, queryset):
        """Export CSV pour les fruits du démon"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="devil_fruits_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nom', 'Romanji', 'Type', 'Capacité', 'Rareté', 'Statut', 'Arc première apparition'])
        
        for fruit in queryset:
            writer.writerow([
                fruit.name,
                fruit.romanji,
                fruit.get_fruit_type_display(),
                fruit.ability[:100],  # Limiter la longueur
                fruit.rarity,
                fruit.get_status_display(),
                fruit.first_appearance_arc.name if fruit.first_appearance_arc else ''
            ])
        
        return response
    
    export_csv.short_description = "Exporter CSV"


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'epithet', 'role', 'bounty', 'status', 'origin']
    list_filter = ['role', 'status']
    search_fields = ['name', 'epithet', 'description']
    ordering = ['name']
    filter_horizontal = ['crews']
    inlines = [FruitHolderInline]
    
    actions = ['export_pdf', 'export_csv']
    
    def export_pdf(self, request, queryset):
        """Export PDF pour les personnages"""
        if queryset.count() != 1:
            self.message_user(request, "Veuillez sélectionner exactement un personnage.", level='error')
            return
        
        character = queryset.first()
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        )
        
        # Titre
        story.append(Paragraph(f"Fiche Personnage: {character.name}", title_style))
        if character.epithet:
            story.append(Paragraph(f"<i>{character.epithet}</i>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Informations principales
        data = [
            ['Nom', character.name],
            ['Surnom', character.epithet or 'N/A'],
            ['Rôle', character.get_role_display()],
            ['Prime', f"{character.bounty:,} Berries" if character.bounty > 0 else 'Aucune'],
            ['Origine', character.origin or 'N/A'],
            ['Statut', character.get_status_display()],
        ]
        
        if character.first_appearance_episode:
            data.append(['Première apparition', f"Épisode #{character.first_appearance_episode.number}: {character.first_appearance_episode.title}"])
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Description
        if character.description:
            story.append(Paragraph("Description", heading_style))
            story.append(Paragraph(character.description, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Équipages
        crews = character.crews.all()
        if crews:
            story.append(Paragraph("Équipages", heading_style))
            crew_list = ', '.join([crew.name for crew in crews])
            story.append(Paragraph(crew_list, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Fruits du démon
        fruit_holders = character.fruit_history.all().order_by('-is_current', '-from_date')
        if fruit_holders:
            story.append(Paragraph("Fruits du démon", heading_style))
            fruit_data = [['Fruit', 'Date début', 'Date fin', 'Actuel']]
            for holder in fruit_holders:
                fruit_data.append([
                    holder.devil_fruit.name,
                    str(holder.from_date) if holder.from_date else 'N/A',
                    str(holder.to_date) if holder.to_date else 'N/A',
                    'Oui' if holder.is_current else 'Non'
                ])
            fruit_table = Table(fruit_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 0.5*inch])
            fruit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(fruit_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Date de génération
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            f"<i>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</i>",
            styles['Normal']
        ))
        
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="character_{character.name.replace(" ", "_")}.pdf"'
        return response
    
    export_pdf.short_description = "Exporter fiche PDF"
    
    def export_csv(self, request, queryset):
        """Export CSV pour les personnages"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="characters_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nom', 'Surnom', 'Rôle', 'Prime', 'Origine', 'Statut', 'Épisode première apparition'])
        
        for character in queryset:
            writer.writerow([
                character.name,
                character.epithet,
                character.get_role_display(),
                character.bounty,
                character.origin,
                character.get_status_display(),
                character.first_appearance_episode.number if character.first_appearance_episode else ''
            ])
        
        return response
    
    export_csv.short_description = "Exporter CSV"


@admin.register(FruitHolder)
class FruitHolderAdmin(admin.ModelAdmin):
    list_display = ['character', 'devil_fruit', 'from_date', 'to_date', 'is_current']
    list_filter = ['is_current', 'devil_fruit__fruit_type']
    search_fields = ['character__name', 'devil_fruit__name']
    ordering = ['-is_current', '-from_date']


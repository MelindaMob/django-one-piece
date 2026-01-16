from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'characters', views.CharacterViewSet, basename='character')
router.register(r'crews', views.CrewViewSet, basename='crew')
router.register(r'fruits', views.DevilFruitViewSet, basename='devilfruit')
router.register(r'arcs', views.ArcViewSet, basename='arc')
router.register(r'episodes', views.EpisodeViewSet, basename='episode')

urlpatterns = [
    path('', include(router.urls)),
]


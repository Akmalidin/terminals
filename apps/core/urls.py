from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terminals/<slug:region_id>/', views.terminals, name='terminals'),
    path('terminal/<int:pk>/', views.terminal_detail, name='terminal_detail'),
    path('collect_cash/<int:terminal_id>/', views.collect_cash, name='collect_cash'),  # Страница для инкассации
]
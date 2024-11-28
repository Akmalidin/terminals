from django.shortcuts import render, get_object_or_404, redirect
from .models import Region, Terminal, Incassation
from django.utils import timezone
from django.utils.timezone import now
import requests
from django.contrib import messages
from datetime import date
from django.urls import reverse

def index(request):
    today = date.today()
    
    regions = Region.objects.all()
    
    # Создаём словарь с регионами и количеством терминалов, которым требуется инкассация
    region_notifications = {}
    for region in regions:
        # Фильтруем терминалы по дате следующей инкассации
        terminals_to_collect = region.terminals.filter(incassations__next_collection=today)
        region_notifications[region.id] = terminals_to_collect.count()

    # Считаем общее количество терминалов, которым требуется инкассация
    total_terminals_to_collect = sum(region_notifications.values())

    return render(request, 'index.html', {
        'regions': regions,
        'region_notifications': region_notifications,
        'total_terminals_to_collect': total_terminals_to_collect
    })

# GOOGLE MAPS FUNCTION FOR REGIONS
def get_coordinates(region_name):
    api_key = 'AIzaSyCFuKQB-tb7Q7TfeU-geoEo9J2IJRgLI9s'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={region_name},Кыргызстан&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return 40.5283, 72.7985  # Исправленный формат


def terminals(request, region_id):
    region = get_object_or_404(Region, slug=region_id)
    terminals = Terminal.objects.filter(region=region)

    for terminal in terminals:
        incassation = terminal.incassations.order_by('-next_collection').first()
        if incassation:
            terminal.last_collected = incassation.last_collected
            terminal.next_collection = incassation.next_collection
            terminal.days_until_next_collection = max(0, (incassation.next_collection - timezone.now().date()).days)
        else:
            terminal.last_collected = None
            terminal.next_collection = None
            terminal.days_until_next_collection = None

    coordinates = get_coordinates(region.name)

    context = {
        'region': region,
        'terminals': terminals,
        'coordinates': coordinates,
    }
    return render(request, 'terminals.html', context)


def terminal_detail(request, pk):
    terminal = get_object_or_404(Terminal, pk=pk)

    # Получаем последнюю инкассацию
    last_incassation = terminal.incassations.order_by('-last_collected').first()

    # Проверяем, можно ли проводить сбор
    today = timezone.now().date()
    collection_due = last_incassation and last_incassation.next_collection <= today if last_incassation else False

    context = {
        'terminal': terminal,
        'last_incassation': last_incassation,  # Передаём объект инкассации
        'collection_due': collection_due,
    }

    return render(request, 'terminal_detail.html', context)




from datetime import timedelta

def collect_cash(request, terminal_id):
    terminal = get_object_or_404(Terminal, id=terminal_id)
    incassation = terminal.incassations.order_by('-next_collection').first()

    if not incassation:
        # Создаем новую запись инкассации, если ее нет
        incassation = Incassation.objects.create(
            terminal=terminal,
            last_collected=timezone.now().date(),
            interval_days=30,  # можно поменять на значение по умолчанию
        )
    else:
        # Обновляем запись
        incassation.last_collected = timezone.now().date()
        incassation.next_collection = incassation.last_collected + timedelta(days=incassation.interval_days)
        incassation.save()

    return redirect('terminal_detail', pk=terminal_id)



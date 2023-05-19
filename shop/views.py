from django.shortcuts import render, redirect
from django.db.models import Q
#from geopy.distance import distance
from .models import Shop
from .forms import ShopForm
from django.contrib.auth.decorators import login_required
import math
from math import radians, cos, sin, asin, sqrt
#from ipware import get_client_ip
from django.conf import settings






# Create your views here.
#@login_required
def shop_list(request):
    shops = Shop.objects.all()

    user_latitude = request.GET.get('lat')
    user_longitude = request.GET.get('lng')

    if user_latitude is not None and user_longitude is not None:
        try:
            user_latitude = float(user_latitude)
            user_longitude = float(user_longitude)
        except ValueError:
            user_latitude = None
            user_longitude = None

    for shop in shops:
        if user_latitude is not None and user_longitude is not None:
            shop.distance = calculate_distance(user_latitude, user_longitude, shop.latitude, shop.longitude)
        else:
            shop.distance = None  # Set distance as None if user's location is not available

    return render(request, 'list.html', {'shops': shops})



def calculate_distance(lat1, lon1, lat2, lon2):
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None  # Return None if any of the coordinates is None
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of the Earth in kilometers
    return c * r

@login_required
def shop_create(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop=form.save(commit=False)
            user = request.user
            shop.user = user
            shop.save()
            return redirect('shop_list')
    else:
        form = ShopForm()
    return render(request, 'form.html', {'form': form})
@login_required
def shop_update(request, pk):
    shop = Shop.objects.get(pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'form.html', {'form': form})

def shop_delete(request, pk):
    shop = Shop.objects.get(pk=pk)
    shop.delete()
    return redirect('shop_list')


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c

    return distance
# views.py
def get_nearby_shops(distance_km, user_latitude, user_longitude, shop_name=None):
    shops = Shop.objects.filter(latitude__isnull=False, longitude__isnull=False)
    nearby_shops = []

    for shop in shops:
        shop_latitude = float(shop.latitude)
        shop_longitude = float(shop.longitude)

        distance = calculate_distance(user_latitude, user_longitude, shop_latitude, shop_longitude)

        if distance_km and distance > distance_km:
            continue  # Skip the shop if distance is specified and it exceeds the distance criteria
        if shop_name and shop_name.lower() not in shop.name.lower():
            continue  # Skip the shop if name is specified and it doesn't match the search criteria
            
        nearby_shops.append(shop)

    return nearby_shops


def shop_search(request):
    if request.method == 'POST':
        distance_km = request.POST.get('distance')
        shop_name = request.POST.get('shop_name')

        if not distance_km and not shop_name:
            error_message = 'Distance or shop name is required.'
            return render(request, 'error.html', {'error_message': error_message})

        try:
            distance_km = float(distance_km) if distance_km else None
        except ValueError:
            error_message = 'Invalid distance value.'
            return render(request, 'error.html', {'error_message': error_message})

        user_latitude = request.POST.get('lat')
        user_longitude = request.POST.get('lng')

        if not user_latitude or not user_longitude:
            error_message = 'User location is missing.'
            return render(request, 'error.html', {'error_message': error_message})

        nearby_shops = get_nearby_shops(distance_km, user_latitude, user_longitude, shop_name)
        print(nearby_shops)

        return render(request, 'search_results.html', {'shops': nearby_shops})

    return render(request, 'search.html')

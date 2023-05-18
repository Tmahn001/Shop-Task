from django.shortcuts import render, redirect
from django.db.models import Q
from geopy.distance import distance
from .models import Shop
from .forms import ShopForm
from django.contrib.auth.decorators import login_required
from math import radians, cos, sin, asin, sqrt
from ipware import get_client_ip
from django.conf import settings
from pathlib import Path



# Create your views here.
@login_required
def shop_list(request):
    shops = Shop.objects.filter(user=request.user).all()

    user_latitude = float(request.GET.get('lat'))
    user_longitude = float(request.GET.get('lng'))

    for shop in shops:
        if user_latitude and user_longitude:
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

def shop_search(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        distance_km = float(request.POST.get('distance'))

        user_location = (latitude, longitude)
        shops = Shop.objects.filter(
            Q(latitude__isnull=False) & Q(longitude__isnull=False)
        )

        nearby_shops = []
        for shop in shops:
            shop_location = (float(shop.latitude), float(shop.longitude))
            if distance(user_location, shop_location).km <= distance_km:
                nearby_shops.append(shop)

        return render(request, 'search_results.html', {'shops': nearby_shops})

    return render(request, 'search.html')



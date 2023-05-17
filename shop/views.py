from django.shortcuts import render, redirect
from django.db.models import Q
from geopy.distance import distance
from .models import Shop
from .forms import ShopForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'list.html', {'shops': shops})

@login_required
def shop_create(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
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



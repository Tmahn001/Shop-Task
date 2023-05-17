from django.test import TestCase
from django.urls import reverse
from .models import Shop
# Create your tests here.

class ShopTestCase(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(
            name='Test Shop',
            latitude=12.345,
            longitude=67.890
        )

    def test_shop_list(self):
        response = self.client.get(reverse('shop_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop.name)

    def test_shop_create(self):
        data = {
            'name': 'New Shop',
            'latitude': 34.567,
            'longitude': 89.012
        }
        response = self.client.post(reverse('shop_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Shop.objects.filter(name='New Shop').exists())

    def test_shop_update(self):
        data = {
            'name': 'Updated Shop',
            'latitude': 45.678,
            'longitude': 90.123
        }
        url = reverse('shop_update', args=[self.shop.pk])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, 'Updated Shop')

    def test_shop_search(self):
        data = {
            'latitude': 12.345,
            'longitude': 67.890,
            'distance': 10
        }
        response = self.client.post(reverse('shop_search'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop.name)



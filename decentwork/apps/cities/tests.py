from collections import OrderedDict

from django.db import IntegrityError
from django.test import Client, TestCase
from rest_framework.test import APITestCase

from .models import City
from .selectors import select_cities_starts_with_query_limit_5


class CityTests(TestCase):
    fixtures = ['cities']

    def test_live_search_query(self):
        """Tests if live search select function returns 5 cities when 5 available."""
        cities = select_cities_starts_with_query_limit_5('W')
        self.assertEqual(len(cities), 5)

    def test_unique_city(self):
        """Tests if i can't add city which alread exists."""
        City.objects.create(name='Test')
        city2 = None
        try:
            city2 = City.objects.create(name='Test')
        except IntegrityError:
            pass
        self.assertEqual(city2, None)

    def test_city_str_represantation(self):
        """Tests string reprasantation of city."""
        city = City.objects.create(name='Test')
        self.assertEqual(str(city), 'Test')

    def test_verbose_name_plural_in_city_model(self):
        """Tests plural name of `City` model."""
        self.assertEqual(str(City._meta.verbose_name_plural), 'Cities')


class ApiCityTests(APITestCase):
    fixtures = ['cities']

    def setUp(self):
        self.client = Client()

    def test_400_when_no_query_string(self):
        """Tests if response from /cities/search/ status code is 400 when no query_string."""
        response = self.client.get('/cities/search/')
        self.assertEqual(response.status_code, 400)

    def test_400_when_no_City_in_database(self):
        """Tests if response have 400 status code when no city in database."""
        response = self.client.get('/cities/search/', {'query': 'NO_IN_DB'})
        self.assertEqual(response.status_code, 400)

    def test_200_when_city_in_db(self):
        """Tests success status code."""
        response = self.client.get('/cities/search/', {'query': 'Łódź'})
        self.assertEqual(response.status_code, 200)

    def test_response_when_city_in_db(self):
        """Tests success response data."""
        response = self.client.get('/cities/search/', {'query': 'Łódź'})
        self.assertEqual(response.data, [OrderedDict([('id', 1), ('name', 'Łódź')])])

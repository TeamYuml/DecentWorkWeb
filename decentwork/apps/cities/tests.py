from django.db import IntegrityError

from .models import City
from .selectors import select_cities_starts_with_query_limit_5

from decentwork.apps.factories.tests import DecentWorkApiTestCase, DecentWorkTestCase


class CityTests(DecentWorkTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.city = self.dw_faker.city(name='Łódź')

    def test_live_search_query(self):
        """Tests if live search select function returns 5 cities when 5 available."""
        cities = select_cities_starts_with_query_limit_5('Ł')
        self.assertGreater(len(cities), 0)
        self.assertLess(len(cities), 6)

    def test_unique_city(self):
        """Tests if i can't add city which alread exists."""
        city2 = None

        try:
            city2 = self.dw_faker.city(name="Łódź")
        except IntegrityError:
            pass

        assert city2 == None

    def test_city_str_represantation(self):
        """Tests string reprasantation of city."""
        assert str(self.city) == 'Łódź'

    def test_verbose_name_plural_in_city_model(self):
        """Tests plural name of `City` model."""
        assert str(City._meta.verbose_name_plural) == 'Cities'


class ApiCityTests(DecentWorkApiTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.city = self.dw_faker.city(name='Łódź')

    def test_400_when_no_query_string(self):
        """Tests if response from /cities/search/ status code is 400 when no query_string."""
        response = self.client.get('/cities/search/')
        assert response.status_code == 400

    def test_400_when_no_City_in_database(self):
        """Tests if response have 400 status code when no city in database."""
        response = self.client.get('/cities/search/', {'query': 'NO_IN_DB'})
        assert response.status_code == 400

    def test_200_when_city_in_db(self):
        """Tests success status code."""
        response = self.client.get('/cities/search/', {'query': 'Łódź'})
        assert response.status_code == 200

    def test_response_when_city_in_db(self):
        """Tests success response data."""
        response = self.client.get('/cities/search/', {'query': 'Łódź'})
        assert response.data[0]['name'] == 'Łódź'

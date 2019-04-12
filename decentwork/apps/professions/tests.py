from django.db import IntegrityError

from .models import Profession
from .selectors import select_professions_starts_with_query_limit_5

from decentwork.apps.factories.tests import DecentWorkApiTestCase, DecentWorkTestCase


class ProfessionTests(DecentWorkTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.profession = self.dw_faker.profession(name='Elektryk')

    def test_live_search_query(self):
        """Tests if live search select function returns 5 cities when 5 available."""
        professions = select_professions_starts_with_query_limit_5('E')
        self.assertGreater(len(professions), 0)
        self.assertLess(len(professions), 6)

    def test_unique_profession(self):
        """Tests if i can't add city which alread exists."""
        profession = None

        try:
            profession = self.dw_faker.profession(name='Elektryk')
        except IntegrityError:
            pass

        assert profession == None

    def test_profession_str_represantation(self):
        """Tests string reprasantation of city."""
        profession = Profession.objects.create(name='Test')
        assert str(profession) == 'Test'


class ApiProfessionTests(DecentWorkApiTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.profession = self.dw_faker.profession(name='Elektryk')

    def test_400_when_no_query_string(self):
        """Tests if response from /professions/search/ status code is 400 when no query_string."""
        response = self.client.get('/professions/search/')
        assert response.status_code == 400

    def test_400_when_no_City_in_database(self):
        """Tests if response have 400 status code when no city in database."""
        response = self.client.get('/professions/search/', {'query': 'NO_IN_DB'})
        assert response.status_code == 400

    def test_200_when_city_in_db(self):
        """Tests success status code."""
        response = self.client.get('/professions/search/', {'query': 'Elektryk'})
        assert response.status_code == 200

    def test_response_when_city_in_db(self):
        """Tests success response data."""
        response = self.client.get('/professions/search/', {'query': 'Elektryk'})
        assert response.data[0]['name'] == 'Elektryk'

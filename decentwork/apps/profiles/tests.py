from rest_framework.authtoken.models import Token

from decentwork.apps.common.models import User
from decentwork.apps.factories.tests import DecentWorkApiTestCase


class UserProfilesTests(DecentWorkApiTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user = self.dw_faker.user()

    def _get_credentials(self):
        token = Token.objects.get(user=self.user)
        self.apiclient.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_update_method_status_201(self):
        self._get_credentials()
        data = {'description': 'test', 'city': 'Warszawa', 'professions': 'Hydraulik',
                'phone_numbers': '123456789'}
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data)
        self.assertEqual(response.status_code, 200)

    def test_update_response_when_success(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test', 'last_name': 'Test2',
            },
            'description': 'test', 'city': 'Warszawa', 'professions': ['Hydraulik'],
            'phone_numbers': ['123456789']
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.data['user']['first_name'], 'Test')
        self.assertEqual(response.data['user']['last_name'], 'Test2')
        self.assertEqual(response.data['description'], 'test')
        self.assertEqual(response.data['city'], 'Warszawa')
        self.assertEqual(response.data['professions'][0], 'Hydraulik')

    def test_update_when_no_description(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test', 'last_name': 'Test2',
            },
            'city': 'Warszawa', 'professions': ['Hydraulik'],
            'phone_numbers': ['123456789']
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_no_phone(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test', 'last_name': 'Test2',
            },
            'city': 'Warszawa', 'professions': ['Hydraulik'], 'description': 'test'
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_no_city(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test', 'last_name': 'Test2',
            },
            'professions': ['Hydraulik'], 'description': 'test'
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_no_profession(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test', 'last_name': 'Test2',
            },
            'city': 'Warszawa', 'description': 'test'
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_no_last_name(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test'
            },
            'city': 'Warszawa', 'description': 'test'
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_no_first_name(self):
        self._get_credentials()
        data = {
            'user': {
                'last_name': 'Test2',
            },
            'city': 'Warszawa', 'description': 'test'
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_two_professions(self):
        self._get_credentials()
        data = {
            'user': {
                'first_name': 'Test', 'last_name': 'Test2',
            },
            'city': 'Warszawa', 'professions': ['Hydraulik', 'Elektryk'], 'description': 'test'
        }
        response = self.apiclient.put('/profiles/userProfiles/'
            + str(self.user.id) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_when_no_token(self):
        data = {
            'user': {
                'last_name': 'Test2',
            },
            'city': 'Warszawa', 'description': 'test'
        }
        response = self.apiclient.post('/profiles/userProfiles/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_list_200(self):
        """Test status of listing users profiles."""
        response = self.apiclient.get('/profiles/userProfiles/')
        self.assertEqual(response.status_code, 200)

    def test_retrive_one_user_profile(self):
        """Test data from retrievieng one user profile."""
        response = self.apiclient.get('/profiles/userProfiles/'
            + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['city'], None)
        self.assertEqual(response.data['professions'], [])

    def test_partial_update_city(self):
        """Test update city in profile."""
        data = {'city': 'Łódź'}
        self._get_credentials()
        response = self.apiclient.patch('/profiles/userProfiles/'
            + str(self.user.id) + '/', data)
        self.assertEqual(response.data['city'], 'Łódź')

    def test_partial_update_professions(self):
        """Test update profile's professions."""
        data = {'professions': 'Murarz'}
        self._get_credentials()
        response = self.apiclient.patch('/profiles/userProfiles/'
            + str(self.user.id) + '/', data)
        self.assertEqual(response.data['professions'], ['Murarz'])

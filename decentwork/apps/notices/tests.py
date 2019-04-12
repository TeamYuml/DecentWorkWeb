from rest_framework.authtoken.models import Token

from decentwork.apps.cities.models import City
from decentwork.apps.common.models import User
from decentwork.apps.factories.tests import DecentWorkApiTestCase
from decentwork.apps.professions.models import Profession


class NoticesApiTests(DecentWorkApiTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user = self.dw_faker.user()
        self.notice = self.dw_faker.notice(
            owner=self.user,
            title='Test',
            profession=Profession.objects.get(name='Hydraulik'),
            city=City.objects.get(name='Warszawa'),
        )
        self.user_assign = self.dw_faker.user_assign(
            user=self.user,
            notice=self.notice
        )

    def _get_credentials(self):
        token = Token.objects.get(user=self.user)
        self.apiclient.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_list_method_status_200(self):
        """Test status 200 when getting /engagments."""
        response = self.apiclient.get('/notices/notices/')
        self.assertEqual(response.status_code, 200)

    def test_list_method_response(self):
        """Test response data when getting list of engagments."""
        notice2 = self.dw_faker.notice(
            owner=self.user,
            title='Test2',
        )

        response = self.apiclient.get('/notices/notices/')
        self.assertEqual(response.data['results'][0]['title'], 'Test')
        self.assertEqual(response.data['results'][1]['title'], 'Test2')

    def test_list_method_content_type(self):
        """Test content-type in viewset method."""
        response = self.apiclient.get('/notices/notices/')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_retrieve_method_status_200(self):
        """Test response status from retrieve viewset method."""
        response = self.apiclient.get('/notices/notices/' + str(self.notice.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_method_contents_json(self):
        """Test response content-type in retrieve method."""
        response = self.apiclient.get('/notices/notices/' + str(self.notice.id) + '/')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_retrive_response_json(self):
        """Test response data in retrieve method."""
        response = self.apiclient.get('/notices/notices/' + str(self.notice.id) + '/')
        self.assertEqual(response.data['title'], 'Test')

    def test_create_without_token(self):
        """Test if create returns 401 when no token."""
        response = self.apiclient.post('/notices/notices/')
        self.assertEqual(response.status_code, 401)

    def test_create_engagment_when_all_data_pass(self):
        """Test create returns 201 when all data is good."""
        self._get_credentials()
        data = {'title': 'Hello2', 'description': 'lol',
                'city': 'Warszawa', 'profession': 'Hydraulik'}
        response = self.apiclient.post('/notices/notices/', data)
        self.assertEqual(response.status_code, 201)

    def test_create_engagment_when_no_city(self):
        """Test create engagment returns 400 when no city passed."""
        self._get_credentials()
        data = {'title': 'Hello2', 'description': 'lol',
                'profession': 'Hydraulik'}
        response = self.apiclient.post('/notices/notices/', data)
        self.assertEqual(response.status_code, 400)

    def test_create_engagment_when_no_profession(self):
        """Test create engagment returns 201 when no profession is passed."""
        self._get_credentials()
        data = {'title': 'Hello2', 'description': 'lol', 'city': 'Warszawa'}
        response = self.apiclient.post('/notices/notices/', data)
        self.assertEqual(response.status_code, 201)

    def test_create_engagment_when_no_description(self):
        """Test create engagment returns 201 when no description is passed."""
        self._get_credentials()
        data = {'title': 'Hello2', 'city': 'Warszawa', 'profession': 'Hydraulik'}
        response = self.apiclient.post('/notices/notices/', data)
        self.assertEqual(response.status_code, 201)

    def test_create_engagment_when_no_title(self):
        """Test create engagment returns 400 when no title passed."""
        self._get_credentials()
        data = {'city': 'Warszawa', 'profession': 'Hydraulik'}
        response = self.apiclient.post('/notices/notices/', data)
        self.assertEqual(response.status_code, 400)

    def test_update_engagment(self):
        """Test update engagment returns 200."""
        self._get_credentials()
        data = {'title': 'Hello2', 'description': 'lol',
                'city': 'Warszawa', 'profession': 'Hydraulik'}
        response = self.apiclient.put('/notices/notices/' + str(self.notice.id) + '/', data)
        self.assertEqual(response.status_code, 200)

    def test_assign_engagment_and_user(self):
        """Test assigning engagment with user returns 201."""
        self._get_credentials()
        notice2 = self.dw_faker.notice(owner=self.user)
        data = {'notice': notice2.id}
        response = self.apiclient.post('/notices/assign/user/', data)
        self.assertEqual(response.status_code, 201)

    def test_delete_assign(self):
        """Test if deleting assigment between engagment and user returns 204."""
        self._get_credentials()
        response = self.apiclient.delete('/notices/assign/user/' + str(self.notice.id) + '/')
        self.assertEqual(response.status_code, 204)

    def test_assign_list(self):
        """Test showing list of users assigned to single engagment."""
        data = {'notice': self.notice.id}
        response = self.apiclient.get('/notices/assign/list/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['notice'], self.notice.id)
        self.assertEqual(response.data[0]['user'], self.user.id)

    def test_assign_list_when_no_engagment_passed(self):
        """Test if assign list returns 400 when no engagment passed."""
        response = self.apiclient.get('/notices/assign/list/')
        self.assertEqual(response.status_code, 400)

    def test_assign_check_no_engagment(self):
        """Test if assign check returns 400 when no engagment passed."""
        self._get_credentials()
        response = self.apiclient.get('/notices/assign/check/')
        self.assertEqual(response.status_code, 400)

    def test_assign_check_no_credentials(self):
        """Test if assign check returns 401 when no credentials passed."""
        response = self.apiclient.get('/notices/assign/check/')
        self.assertEqual(response.status_code, 401)

    def test_assign_check(self):
        """Test assign_check when success."""
        data = {'notice': self.notice.id}
        self._get_credentials()
        response = self.apiclient.get('/notices/assign/check/', data)
        self.assertEqual(response.status_code, 200)

    def test_assign_check_when_not_assigned(self):
        """
        Test if response contains key is_assigned and it contains False
        when user is not assigned to engagment.
        """
        notice2 = self.dw_faker.notice(owner=self.user)
        data = {'notice': notice2.id}
        self._get_credentials()
        response = self.apiclient.get('/notices/assign/check/', data)
        self.assertEqual(response.data['is_assigned'], False)

    def test_assign_check_when_assigned(self):
        """
        Test if response contains key is_assigned and it contains True
        when user is assigned to engagment.
        """
        data = {'notice': self.notice.id}
        self._get_credentials()
        response = self.apiclient.get('/notices/assign/check/', data)
        self.assertEqual(response.data['is_assigned'], True)
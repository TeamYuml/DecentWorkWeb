from rest_framework.authtoken.models import Token

from decentwork.apps.common.models import User
from decentwork.apps.common.views import TokenSignIn
from decentwork.apps.factories.tests import DecentWorkApiTestCase


class UserApiTests(DecentWorkApiTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user = self.dw_faker.user(email='test@test.com', password='test1234#')

    def test_login_when_everything_is_fine(self):
        """Tests login when success and reponse is 200."""
        data = {'email': 'test@test.com', 'password': 'test1234#'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'test@test.com')

    def test_login_when_wrong_email_format(self):
        """Tests login when email has wrong format."""
        data = {'email': 'testtest.com', 'password': 'test1234#'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 401)

    def test_login_when_no_email(self):
        """Tests login when no email in POST data."""
        data = {'password': 'test1234#'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 400)

    def test_login_when_no_password(self):
        """Tests login when no password in POST data."""
        data = {'email': 'test@test.com'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 400)

    def test_login_when_wrong_password(self):
        """Tests login when wrong password is entered."""
        data = {'email': 'test@test.com', 'password': 'test1234'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 401)

    def test_login_when_wrong_email(self):
        """Tests login when wrong email is entered."""
        data = {'email': 'tes@test.com', 'password': 'test1234#'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 401)

    def test_login_when_wrong_email_and_password(self):
        """Tests login when wrong email and password are entered."""
        data = {'email': 'tes@test.com', 'password': 'test1234'}
        response = self.client.post('/common/login/', data)
        self.assertEqual(response.status_code, 401)

    def test_token_view_when_no_id_token(self):
        """Tests if sign in with Google from mobile return 401 when no idToken sent."""
        response = self.apiclient.post('/common/tokensignin/')
        self.assertEqual(response.status_code, 400)

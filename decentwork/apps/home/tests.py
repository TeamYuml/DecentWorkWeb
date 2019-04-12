from decentwork.apps.common.models import User
from decentwork.apps.factories.tests import DecentWorkTestCase


class TestHome(DecentWorkTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user = self.dw_faker.user()

    def test_home_without_login(self):
        """Test home when user is not logged in."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_when_user_logged(self):
        """Test status code when user is logged."""
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_template_home(self):
        """Test template of response when user is logged."""
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_token_in_session(self):
        """Test if token is added to session."""
        self.client.force_login(self.user)
        self.client.get('/')
        session = self.client.session
        self.assertTrue('token' in session)

from django.test import Client, TestCase
from rest_framework.test import APIClient, APITestCase

from .factories import DecentWorkFaker


class DecentWorkTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.dw_faker = DecentWorkFaker()
        self.client = Client()


class DecentWorkApiTestCase(APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.dw_faker = DecentWorkFaker()
        self.client = Client()
        self.apiclient = APIClient()

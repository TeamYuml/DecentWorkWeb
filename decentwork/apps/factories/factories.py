import factory

from factory.django import DjangoModelFactory as Factory
from faker import Faker
from rest_framework.authtoken.models import Token

from decentwork.apps.cities.models import *
from decentwork.apps.common.models import *
from decentwork.apps.notices.models import *
from decentwork.apps.professions.models import *
from decentwork.apps.profiles.models import *


class DecentWorkFaker(object):
    """Provides objects to use in unit testing."""

    def __getattr__(self, key):
        return getattr(Faker(), key)

    def city(self, **kwargs):
        return CityFactory.create(**kwargs)

    def profession(self, **kwargs):
        return ProfessionFactory.create(**kwargs)

    def user(self, **kwargs):
        return UserFactory.create(**kwargs)

    def notice(self, **kwargs):
        return NoticeFactory.create(**kwargs)

    def token(self, **kwargs):
        return TokenFactory.create(*kwargs)

    def user_assign(self, **kwargs):
        return UserAssignedFactory.create(**kwargs)


dw_faker = DecentWorkFaker()
fake = factory.Faker


class CityFactory(Factory):
    class Meta:
        model = City

    name = fake('pystr')


class ProfessionFactory(Factory):
    class Meta:
        model = Profession

    name = fake('pystr')


class UserFactory(Factory):
    class Meta:
        model = User

    first_name = fake('first_name')
    last_name = fake('last_name')
    username = fake('license_plate')
    email = fake('email')
    password = fake('password')

    @factory.post_generation
    def post_generation(self, *args, **kwargs):
        self.set_password(self.password)
        self.save()


class NoticeFactory(Factory):
    class Meta:
        model = Notice

    owner = factory.SubFactory(UserFactory)
    profession = factory.SubFactory(ProfessionFactory)
    city = factory.SubFactory(CityFactory)
    title = fake('pystr')
    description = fake('text')


class TokenFactory(Factory):
    class Meta:
        model = Token

    key = fake('pystr')
    user = factory.SubFactory(UserFactory)


class UserAssignedFactory(Factory):
    class Meta:
        model = UserAssigned

    notice = factory.SubFactory(NoticeFactory)
    user = factory.SubFactory(UserFactory)
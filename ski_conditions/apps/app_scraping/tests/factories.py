import factory

from ..models import SkiResort


class ResortFactory(factory.DjangoModelFactory):
    resort_name = factory.Faker('company')

    class Meta:
        model = SkiResort

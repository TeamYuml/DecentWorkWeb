from django.utils.translation import gettext as _
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from decentwork.apps.cities.models import City
from decentwork.apps.cities.selectors import select_cities_starts_with_query_limit_5
from decentwork.apps.cities.serializers import CitySerializer


class CityLiveSearch(APIView):
    authentication_classes = ()

    def get(self, request, format=None) -> Response:
        """Gets cities started with entered queryset."""
        query = request.query_params.get('query', None)

        if query:
            cities = select_cities_starts_with_query_limit_5(query)

            if cities:
                serializer = CitySerializer(cities, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(_('No cities with this query'), status=status.HTTP_400_BAD_REQUEST)

        return Response(_('No query string was entered'), status=status.HTTP_400_BAD_REQUEST)


class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    authentication_classes = ()

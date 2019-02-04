from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from decentwork.apps.professions.models import Profession
from decentwork.apps.professions.selectors import select_professions_starts_with_query_limit_5
from decentwork.apps.professions.serializers import ProfessionSerializer


class ProfessionLiveSearch(APIView):
    authentication_classes = ()

    def get(self, request, format=None) -> Response:
        """Gets cities started with entered queryset."""
        query = request.query_params.get('query', None)

        if query:
            professions = select_professions_starts_with_query_limit_5(query)

            if professions:
                serializer = ProfessionSerializer(professions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(_('No cities with this query'), status=status.HTTP_400_BAD_REQUEST)

        return Response(_('No query string'), status=status.HTTP_400_BAD_REQUEST)

class ProfessionList(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes = ()

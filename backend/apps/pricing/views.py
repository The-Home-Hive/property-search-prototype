from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PriceRange
from .serializers import PriceRangeSerializer


class PriceRangeView(APIView):
    def get(self, request):
        country_id = request.query_params.get("country_id")
        listing_type = request.query_params.get("listing_type")

        price_range = PriceRange.objects.filter(
            country_id=country_id, listing_type=listing_type
        ).first()

        if price_range is None:
            return Response({})

        return Response(PriceRangeSerializer(price_range).data)

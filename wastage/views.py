from .serializers import WastageSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError

# Create your views here.

class DailyWastageView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        weekly_wastage = WastageSerializer.from_week_year(**data)
        return Response(weekly_wastage.data)

class DailyWastageAdd(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        wastage = WastageSerializer(data=data)
        if wastage.is_valid():
            try:
                wastage.save()
            except IntegrityError:
                return Response("Wastage for this day already exists", status=status.HTTP_400_BAD_REQUEST)
            return Response("Created successfully", status=status.HTTP_201_CREATED)
        return Response(wastage.errors, status=status.HTTP_400_BAD_REQUEST)


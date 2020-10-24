from .serializers import MenuViewSerializer, MenuAddSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Menu

# Create your views here.

class MenuByDay(APIView):
    def get(self, request):
        menus = MenuViewSerializer.from_date(datetime.now())
        return Response(menus.data)

    def post(self, request):
        data = JSONParser().parse(request)
        date = data.get("menu_date", None)
        if not date:
            date = datetime.now()
        else:
            date = datetime.fromisoformat(date)
        menus = MenuViewSerializer.from_date(date)
        return Response(menus.data)

class MenuAdd(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        menu = MenuAddSerializer(data=data)
        if menu.is_valid():
            menu.save()
            return Response("Menu Added successfully", status=status.HTTP_201_CREATED)
        return Response(menu.errors, status=status.HTTP_400_BAD_REQUEST)

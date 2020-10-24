from .serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError

# Create your views here.

class ExpenseView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            weekly_expense = ExpenseSerializer.from_week_year(**data)
        except TypeError:
            return Response({})
        return Response(weekly_expense.data)

class ExpenseAdd(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        expense = ExpenseSerializer(data=data)
        if expense.is_valid():
            try:
                expense.save()
            except IntegrityError:
                return Response("Expense for this week and year already exists", status=status.HTTP_400_BAD_REQUEST)
            return Response("Created successfully", status=status.HTTP_201_CREATED)
        return Response(expense.errors, status=status.HTTP_400_BAD_REQUEST)

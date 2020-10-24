from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.Serializer):
    week_number = serializers.IntegerField()
    year_number = serializers.IntegerField()
    amount = serializers.FloatField()

    def create(self, validated_data):
        expense = Expense(**validated_data)
        expense.save()
        return expense

    @classmethod
    def from_week_year(cls, week_number: int, year_number: int, **kwargs):
        return cls(Expense.from_week_year(week_number, year_number))

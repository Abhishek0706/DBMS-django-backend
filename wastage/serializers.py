from rest_framework import serializers
from .models import DailyWastage

class WastageSerializer(serializers.Serializer):
    curr_date = serializers.DateTimeField()
    amount = serializers.FloatField()
    waste_weight = serializers.FloatField()

    def create(self, validated_data):
        wastage = DailyWastage(**validated_data)
        wastage.save()
        return wastage


    @classmethod
    def from_week_year(cls, week_number: int, year_number: int, **kwargs):
        week_number = int(week_number)
        year_number = int(year_number)
        return cls(DailyWastage.from_week_year(week_number, year_number), many=True)

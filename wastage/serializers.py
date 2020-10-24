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
    def from_week_year(cls, week_no: int, year_no: int, **kwargs):
        week_no = int(week_no)
        year_no = int(year_no)
        return cls(DailyWastage.from_week_year(week_no, year_no), many=True)

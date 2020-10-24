from rest_framework import serializers
from datetime import datetime
from .models import Menu

class MenuViewSerializer(serializers.Serializer):
    menu_date = serializers.DateTimeField()
    title_id = serializers.IntegerField()
    items = serializers.ListField()
    title_name = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    @classmethod
    def from_date(cls, date: datetime):
        return cls(Menu.from_day(date), many=True)

class MenuAddSerializer(serializers.Serializer):
    menu_date = serializers.DateTimeField()
    title_name = serializers.CharField()
    items = serializers.ListField()

    def create(self, validated_data):
        menu = Menu(**validated_data)
        menu.save()
        return menu


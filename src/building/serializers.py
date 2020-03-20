from django.shortcuts import get_object_or_404
from rest_framework import serializers


from building.models import Building, BricksTask


class BuildingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Building
        fields = ['id', 'address', 'construction_year']


class BricksTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = BricksTask
        read_only_fields = ['building']
        fields = ['count', 'date']

    def create(self, validated_data):
        return BricksTask.objects.create(building=self.context['building'], **validated_data)


class BuildingStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField(source='brick_tasks__date')
    address = serializers.CharField()
    count = serializers.IntegerField(source='brick_tasks__count__sum')

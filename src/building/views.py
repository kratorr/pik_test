from collections import defaultdict

from django.shortcuts import get_object_or_404
from django.db.models import Sum

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from building.models import Building, BricksTask
from building.serializers import BuildingSerializer, BricksTaskSerializer, BuildingStatsSerializer


class BuildingViewSet(CreateModelMixin, GenericViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    @action(methods=['post'], detail=True, url_path='add-bricks')
    def add_bricks(self, request, pk=None):
        queryset = Building.objects.all()
        building = get_object_or_404(queryset, pk=pk)
        serializer = BricksTaskSerializer(data=request.data, context={'building': building})
        if serializer.is_valid(raise_exception=True):
            question = serializer.save()
        return Response(serializer.data)


class BuildingStats(viewsets.GenericViewSet):

    def list(self, request, format=None):
        queryset = Building.objects.values('address', 'id', 'brick_tasks__date'). \
            annotate(Sum('brick_tasks__count')).order_by('brick_tasks__date')
        serializer = BuildingStatsSerializer(queryset, many=True)
        
        grouped_data = defaultdict(list)
        for grouped_task in serializer.data:
            if grouped_task['id'] in grouped_data:
                grouped_data[grouped_task['id']]['bricks'].append(
                    {'count': grouped_task['count'], 'date': grouped_task['date']}
                )
            else:
                grouped_data[grouped_task['id']] = {
                    'address': grouped_task['address'], 'bricks': [
                        {'count':grouped_task['count'], 'date': grouped_task['date']}
                    ]
            }
        result = [data for data in grouped_data.values()]
        return Response(result)

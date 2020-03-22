from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from building.models import Building, BricksTask
from building.views import BuildingViewSet, BuildingStats
from django.http import response
import json

client = Client()


class CreateBuildingTest(TestCase):
    """ Test module for inserting a new building """
    def setUp(self):
        self.bulding_id = str(Building.objects.create(address= 'адрес',construction_year=1999).id)
        self.invalid_payload1 = {
            'address': 0,
            'construction_year': 'not_year'
        }
        self.view = BuildingViewSet.as_view({'post': 'create'})
        
    
    def test_create_valid_building(self):
        payload = {
            'address': 'адрес',
            'construction_year': 1999
        }
        factory = APIRequestFactory()
        request = factory.post(
            '/api/building/', 
            json.dumps(payload), 
            content_type='application/json'
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        
    def test_create_invalid_empty_building(self):
        payload = {
            'address': '',
            'construction_year': ''
        }
        factory = APIRequestFactory()
        request = factory.post(
            '/api/building/', 
            json.dumps(payload), 
            content_type='application/json'
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 400)


class AddBricksTest(TestCase):
    """ Test module for inserting brick task """
    def setUp(self):
        self.bulding_id = Building.objects.create(address= 'тестовый адрес',construction_year=1999).id
        self.invalid_build_id = 999
        self.view = BuildingViewSet.as_view({'post': 'add_bricks'})
        
    def test_add_bricks_valid(self):
        payload = {"count": 1000, "date":"2020-03-21"}
        factory = APIRequestFactory()
        request = factory.post(
            f'/api/building/{self.bulding_id}/add-bricks/',
            json.dumps(payload), content_type='application/json')
        response = self.view(request, self.bulding_id)
        self.assertEqual(response.status_code, 200)

    def test_add_bricks_invalid_build_id(self):
        payload = {"count": 1000, "date":"2020-03-21"}
        factory = APIRequestFactory()
        request = factory.post(
            f'/api/building/{self.invalid_build_id}/add-bricks/',
            json.dumps(payload), 
            content_type='application/json'
        )
        response = self.view(request, self.invalid_build_id)
        self.assertEqual(response.status_code, 404)

    def test_add_bricks_without_count(self):
        payload = {"date":"2020-03-21"}
        factory = APIRequestFactory()
        request = factory.post(
            f'/api/building/{self.bulding_id}/add-bricks/', 
            json.dumps(payload), 
            content_type='application/json'
        )
        response = self.view(request, self.bulding_id)
        self.assertEqual(response.status_code, 400)
    
    def test_add_bricks_without_date(self):
        payload = {"count": 1000}
        factory = APIRequestFactory()
        request = factory.post(
            f'/api/building/{self.bulding_id}/add-bricks/',
            json.dumps(payload),
            content_type='application/json'
        )
        response = self.view(request, self.bulding_id)
        self.assertEqual(response.status_code, 400)


class BuildingStatsTest(TestCase):
    """ Test module for getting buildings stats """
    def setUp(self):
        self.view = BuildingStats.as_view({'get': 'list'})
        
    def test_get_stats(self):
        factory = APIRequestFactory()
        request = factory.get(f'/api/building/stats/',)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

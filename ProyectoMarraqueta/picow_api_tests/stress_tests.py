import json
from django.http import HttpRequest
from django.utils import timezone

from picow_api import views as api_views
from core import models as core_models
from active_testing import assertBoleanEqual

from random import randrange

import time

TYPE="Stress TESTS"

def create_full_request(uuid, ip_address):
        """Create a full request to picow_api API endpoint

        Args:
            uuid (str): keychain UUID
            ip_address (str): esp32 module IP address

        Returns:
            HttpRequest: django http request object with full data for endpoint 
        """
        request = HttpRequest()
        request.method="POST"
        data = {
            "uuid": uuid, 
            "ip": ip_address
        }

        json_data = json.dumps(data)
        encoded_data = json_data.encode('utf-8')
        request._body=encoded_data
        return request


def test_creating_and_saving_50_bicycles():
    """
        This stress test consists in creating a BicycleHolder with 50 slots, and creating 50 users, 
        each one with its own bicycle and KeyChain.
        The test will attempt to save all 50 bicycles one after another into the holder.
    """
    start_time = time.time()
    failure_list = []
    
    capacity = 50
    location="LOL!#$%"
    nearest_building = "C"

    dummyHolder = core_models.BicycleHolder.objects.create(
        capacity=capacity,
        location=location,
        nearest_building=nearest_building,
    )

    ip_address = "192.168.100.1"
    dummyModule = core_models.EspModule.objects.create(
        ip_address=ip_address,
        latest_online=(timezone.now()),
        bicycleholder=dummyHolder,
    )
    i = 0
    for user in enumerate(range(50)):
        i+=1
        # Create Professor
        department = "DFIS"
        dummyUser = core_models.Professor.objects.create(
            department=department,
            username=f"User_attempt_{i}"
            )    
        
        uuid=randrange(100000000,999999999)
        dummyKeychain = core_models.KeyChain.objects.create(user=dummyUser, uuid=uuid)

        dummyBicycle = core_models.Bicycle.objects.create(
            model="TRX",
            colour="Magenta",
            bike_type = "TTB",
            bicy_user=dummyUser,
        )
        
        request = create_full_request(uuid, ip_address)
        response = api_views.recv(request)
        
        print(f"Response:\n\tstatus_code:{response.status_code}\n\theaders:{response.headers}\n\tdata:{response.content.decode()}")

        expected_object = {
            "code": "0.1",
            "slot_to_open": i-1
        }

        response_object = json.loads(response.content.decode())
        
        check1 = assertBoleanEqual(response.status_code, 200)
        check2 = assertBoleanEqual(response.headers, {"Content-Type": "application/json"})
        check3 = assertBoleanEqual(response.closed, True)
        check4 = assertBoleanEqual(response_object, expected_object)

        if (check1 and check2 and check3 and check4) == False:
            failure_list.append(i)
    
    end_time = time.time()

    for fail in failure_list:
        print(f"\tAttempt No:{fail}, has failed")
    
    print(f"ELAPSED TIME: {str(end_time-start_time).replace('.', ',')} s")

def test_creating_saving_and_removing_50_bicycles():
    """
        This stress test consists in creating a BicycleHolder with 50 slots, and creating 50 users, 
        each one with its own bicycle and KeyChain.
        The test will attempt to save all 50 bicycles one after another into the holder.
    """

    failure_list = []
    
    capacity = 50
    location="LOL!#$%"
    nearest_building = "C"

    dummyHolder = core_models.BicycleHolder.objects.create(
        capacity=capacity,
        location=location,
        nearest_building=nearest_building,
    )

    ip_address = "192.168.100.1"
    dummyModule = core_models.EspModule.objects.create(
        ip_address=ip_address,
        latest_online=(timezone.now()),
        bicycleholder=dummyHolder,
    )
    i = 0
    for user in enumerate(range(50)):
        i+=1
        # Create Professor
        department = "DFIS"
        dummyUser = core_models.Professor.objects.create(
            department=department,
            username=f"User_attempt_{i}"
            )    
        
        uuid=randrange(100000000,999999999)
        dummyKeychain = core_models.KeyChain.objects.create(user=dummyUser, uuid=uuid)

        dummyBicycle = core_models.Bicycle.objects.create(
            model="TRX",
            colour="Magenta",
            bike_type = "TTB",
            bicy_user=dummyUser,
        )
        # ATTEMP TO ADD THE USER'S BICYCLE
        request = create_full_request(uuid, ip_address)
        response = api_views.recv(request)

        print(f"Response:\n\tstatus_code:{response.status_code}\n\theaders:{response.headers}\n\tdata:{response.content.decode()}")

        expected_object = {
            "code": "0.1",
            "slot_to_open": 0
        }

        response_object = json.loads(response.content.decode())
        
        check1 = assertBoleanEqual(response.status_code, 200)
        check2 = assertBoleanEqual(response.headers, {"Content-Type": "application/json"})
        check3 = assertBoleanEqual(response.closed, True)
        check4 = assertBoleanEqual(response_object, expected_object)

        # ATTEMP TO REMOVE USER'S BICYCLE
        response = api_views.recv(request)

        print(f"Response:\n\tstatus_code:{response.status_code}\n\theaders:{response.headers}\n\tdata:{response.content.decode()}")

        expected_object = {
            "code": "1.1",
            "slot_to_open": 0
        }

        response_object = json.loads(response.content.decode())
        
        check5 = assertBoleanEqual(response.status_code, 200)
        check6 = assertBoleanEqual(response.headers, {"Content-Type": "application/json"})
        check7 = assertBoleanEqual(response.closed, True)
        check8 = assertBoleanEqual(response_object, expected_object)


        if (check1 and check2 and check3 and check4 and check5 and check6 and check7 and check8) == False:
            failure_list.append(i)
    

    for fail in failure_list:
        print(f"\tAttempt No:{fail}, has failed")


ALLOWED_TESTS = (test_creating_and_saving_50_bicycles,)

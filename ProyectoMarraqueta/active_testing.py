import os
import sys
import json
import django
from django.test import TestCase
from django.http import HttpRequest
from django.utils import timezone


sys.path.append('/home/technopy/Documents/Proyecto-Marraqueta/ProyectoMarraqueta')
#from django_project import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoMarraqueta.settings')
django.setup()

from picow_api import views as api_views
from core import models as core_models

from django.core.management.commands import flush
from django.core.management import call_command


def assertEqual(a, b):
    if a==b:
        print(" + OK +")
    else:
        print(" - Failure -")
    
    return a==b

def create_test(func):
    def inner1():
        print("// TEST //")
        func()
        print("// END TEST")
        print("\nFlushing DB...")
        flush_cmd = flush.Command()
        call_command(flush_cmd, verbosity=0, interactive=False)
        print("FLUSHED!\n")
    return inner1



def test_recv_not_post_request():
    """
        This test creates multiple requests with all the 
        available methods except POST method, those beign:
        GET, HEAD, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH.

        Hence the request to API is rejected
    """
    request = HttpRequest()
    request.method="GET"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)

    request = HttpRequest()
    request.method="HEAD"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)

    request = HttpRequest()
    request.method="PUT"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)

    request = HttpRequest()
    request.method="DELETE"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)
    
    request = HttpRequest()
    request.method="CONNECT"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)

    request = HttpRequest()
    request.method="OPTIONS"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)

    request = HttpRequest()
    request.method="TRACE"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)

    request = HttpRequest()
    request.method="PATCH"
    response = api_views.recv(request)

    assertEqual(response.status_code, 400)
    assertEqual(response.closed, True)


def test_invalid_json_data_format_post_request():
    """
        This test creates a request with a bad Json format,
        hence the request to API is rejected
    """

    request = HttpRequest()
    request.method="POST"
    data = {
        "data": "12345678910", # should be uuid to be correct
        "ipaddr": "192.168.100.1" # should be ip to be correct
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')
    request._body=encoded_data
    
    response = api_views.recv(request)

    assertEqual(response.status_code, 406)
    assertEqual(response.closed, True)


def test_valid_json_data_format_but_invalid_data():
    """
        This test creates a request with a valid Json data format, 
        but the data is invalid, hence the request to API is rejected
    """

    request = HttpRequest()
    request.method="POST"
    data = {
        "uuid": "12345678910", 
        "ip": "192.168.100.1"
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')
    request._body=encoded_data
    
    response = api_views.recv(request)

    assertEqual(response.status_code, 418)
    assertEqual(response.closed, True)


def test_valid_json_data_with_bad_uuid():
    """
        This test creates a valid Guard, BicycleHolder and EspModule,
        but there is no valid Keychain, hence, the request to API is rejected
    """

    dummyGuard = core_models.Guard.objects.create()
    
    capacity=5
    location="LOL!#$%"
    nearest_building = "C"
    dummyHolder = core_models.BicycleHolder.objects.create(
        capacity=capacity,
        location=location,
        nearest_building=nearest_building,
    )
    
    ip_addr = "192.168.100.1"

    dummyModule = core_models.EspModule.objects.create(
        ip_address=ip_addr,
        latest_online=timezone.now(),
        bicycleholder=dummyHolder
    )

    request = HttpRequest()
    request.method="POST"
    data = {
        "uuid": "12345678910", 
        "ip": ip_addr
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')
    request._body=encoded_data
    
    response = api_views.recv(request)

    assertEqual(response.status_code, 418)
    assertEqual(response.closed, True)


def test_valid_json_data_with_bad_ip_address():
    """
        This test creates a valid Guard, and Keychain,
        but there is no valid ESPModule, hence, the request to API is rejected
    """

    uuid=123456789
    dummyUser = core_models.Guard.objects.create()
    dummyKeychain = core_models.KeyChain.objects.create(user=dummyUser, uuid=uuid)
    
    request = HttpRequest()
    request.method="POST"
    data = {
        "uuid": dummyKeychain.uuid, 
        "ip": "192.168.100.1"
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')
    request._body=encoded_data
    
    response = api_views.recv(request)

    assertEqual(response.status_code, 418)
    assertEqual(response.closed, True)


def test_valid_request_but_no_bicycle():
    """
        This test creates a valid Guard, BicycleHolder, EspModule, and KeyChain
        but there is no bicycle, hence, the request in the API Fails
    """

    dummyGuard = core_models.Guard.objects.create()
    
    capacity=5
    location="LOL!#$%"
    nearest_building = "C"
    dummyHolder = core_models.BicycleHolder.objects.create(
        capacity=capacity,
        location=location,
        nearest_building=nearest_building,
    )
    
    dummyModule = core_models.EspModule.objects.create(
        ip_address="192.168.100.1",
        latest_online=timezone.now(),
        bicycleholder=dummyHolder
    )

    uuid=123456789
    dummyKeychain = core_models.KeyChain.objects.create(user=dummyGuard, uuid=uuid)
    
    request = HttpRequest()
    request.method="POST"
    data = {
        "uuid": dummyKeychain.uuid, 
        "ip": dummyModule.ip_address
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')
    request._body=encoded_data
    
    response = api_views.recv(request)

    assertEqual(response.status_code, 418)
    assertEqual(response.closed, True)


def test_valid_request_but_no_place():
    """
        This test creates a valid Guard, BicycleHolder, EspModule, KeyChain and Bicycle, hence, the request in the API is successful, but there are no empty places in BicycleHolder
    """
    department = "DFIS"
    dummyUser = core_models.Professor.objects.create(department=department)
    
    location="LOL!#$%"
    nearest_building = "C"
    dummyHolder = core_models.BicycleHolder.objects.create(
        capacity=0,
        location=location,
        nearest_building=nearest_building,
    )
    

    uuid=123456789
    dummyKeychain = core_models.KeyChain.objects.create(user=dummyUser, uuid=uuid)

    dummyBicycle = core_models.Bicycle.objects.create(
        model="TRX",
        colour="Magenta",
        bike_type = "TTB",
        bicy_user=dummyUser,
    )

    ip_address = "192.168.100.1"

    dummyModule = core_models.EspModule.objects.create(
        ip_address=ip_address,
        latest_online=(timezone.now()),
        bicycleholder=dummyHolder,
    )

    request = HttpRequest()
    request.method="POST"
    data = {
        "uuid": uuid, 
        "ip": ip_address
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')
    request._body=encoded_data
    
    response = api_views.recv(request)

    print(f"Response data:\n\tstatus_code:{response.status_code}\n\theaders:{response.headers}")

    assertEqual(response.status_code, 200)
    assertEqual(response.headers, {"Content-Type": "application/json"})
    assertEqual(response.closed, True)

    data_response = response.content

    print(data_response)
    print(type(data_response))


execute_test = create_test(test_valid_request_but_no_bicycle)

execute_test()
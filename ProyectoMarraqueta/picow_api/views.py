from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from core import models as core_models

def auth_user():
    pass


def controller(keychain_uuid, picow_ip_addr):
    # Receive keychain_uuid
    picow_module = core_models.PicowModule.objects.get(ip_address=picow_ip_addr)
    
    # Find the Bicycleholder instance corresponding to picow_ip_addr
    bicycle_holder = picow_module.bicycleholder_set.all()
    
    # Get the KeyChain object related to keychain_uuid
    keychain = core_models.KeyChain.objects.get(uuid=keychain_uuid)
    
    # Get the user related to KeyChain instance.
    user = keychain.user
    
    # Get a list which contains the user's bicycle's PKs
    bicycles = user.bicycle_set.all()
    
    # Check which of the PKs is in the Bicycleholder
    for bicycle in enumerate(bicycles):
        is_saved = bicycle_holder.check_bicycle(bicycle.pk)

        if is_saved == 0: # Case 1: if there is bicycle in bicycleholder.
            pass
        elif is_saved == 1: # Case 2: if there is not bicycle in bicycleholder.
            pass
        elif is_saved == -1: # Case 3: if bicycle.pk is not int.
            pass




def recv(request):
    if request.method == "POST":
        # Receive UUID
        post_data = str(request.body.decode())
        # Parse json data
        data = json.loads(post_data)
        
        # Obtain the uuid and ip data from json
        uuid = data['uuid']
        ipaddr = data['ip']

        # Print log C:
        print(f"UUID: {uuid}. FROM: {ipaddr}")

        # Pass UUID and pico_w's ip address, to controller function.
        controller(uuid, ipaddr)
        
    else:
        # Return 400 status code
        response = HttpResponse()
        response.status_code = 400
        response.closed = True

        return response
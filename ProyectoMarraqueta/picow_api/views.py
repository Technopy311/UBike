from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from core import models as core_models


def auth_user():
    pass


def controller(keychain_uuid, picow_ip_addr):
    # Get the picow instance with that ip_addr
    picow_module = core_models.PicowModule.objects.get(ip_address=picow_ip_addr)

    print(f"#######: {picow_module}")
    
    # Find the Bicycleholder instance corresponding to picow_module's instance
    bicycle_holder = picow_module.bicycleholder

    print(f"#######: {bicycle_holder}")
    
    # Get the KeyChain object related to keychain_uuid
    keychain = core_models.KeyChain.objects.get(uuid=keychain_uuid)
    
    # Get the user related to KeyChain instance.
    user = keychain.user
    print(f"#######: {user}")
    
    # Get a list which contains the user's bicycle's PKs
    bicycles = user.bicycle_set.all()
    
    # Check which of the PKs is in the Bicycleholder
    for bicycle in bicycles:
        is_saved = bicycle_holder.check_bicycle(bicycle)

        if is_saved == 0: # Case 1: if there is bicycle in bicycleholder.
            print("### Bicycle was registered, removing.")
            bicycle_holder.del_bicycle(bicycle)
        elif is_saved == 1: # Case 2: if there is not bicycle in bicycleholder.
            bicycle_holder.add_bicycle(bicycle)
            print("### Bicycle is not registered, adding.")
        elif is_saved == -1: # Case 3: if bicycle.pk is not int.
            print("Bicycle.pk is not integer")
    ## ONLY WORKS ASSUMING ONLY 1 BICYCLE PER PERSON

    print(f"#### Bicycleholder slots: {bicycle_holder.slots}")

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
        auth_data = controller(uuid, ipaddr)

        response = HttpResponse()
        response.status_code = 200

    else:
        # Return 400 status code
        response = HttpResponse()
        response.status_code = 400
        response.closed = True

    return response
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
    bicycle = user.bicycle_set.all()[0]
    
    in_holder = bicycle_holder.check_bicycle(bicycle)

    if in_holder == -1: 
        #check if bicycle is in another bicycleholder
        if bicycle.is_saved:
            print("Bicycle is in another holder")
        else:
            print("Bicycle is not in any holder - adding it")
            status = bicycle_holder.add_bicycle(bicycle)
            if status[0] == 0:
                print("Bicycle added C:")
                return status[1] #return available index
            elif status[0] == 1:
                print("Bicycle is not a real bicycle!")
            elif status[0] == 2:
                print("There is no empty place")
    else:
        print("There is bicycle C: - removing it")
        status = bicycle_holder.del_bicycle(bicycle)
        if status==0:
            print("Bicycle deleted succesfully")
        elif status==1:
            print("Bicycle not in holder")


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
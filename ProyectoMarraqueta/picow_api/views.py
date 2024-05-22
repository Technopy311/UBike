from django.shortcuts import redirect
from django.http import HttpResponse
import json
from core import models as core_models


def auth_user():
    pass


def controller(keychain_uuid, esp_ip_addr):
    """_summary_

    Args:
        keychain_uuid (int): keychain UUID
        esp_ip_addr (int): ESP32 ip address

    Returns:
        tuple:(code, index to open)
    """
    try:
        # Get the esp instance with that ip_addr
        esp_module = core_models.EspModule.objects.get(ip_address=esp_ip_addr)
        print(f"#######: {esp_module}")
    except core_models.EspModule.DoesNotExist:
        raise ValueError
    
    # Find the Bicycleholder instance corresponding to esp_module's instance
    bicycle_holder = esp_module.bicycleholder
    print(f"#######: {bicycle_holder}")

    try:
        # Get the KeyChain object related to keychain_uuid
        keychain = core_models.KeyChain.objects.get(uuid=keychain_uuid)
    except core_models.KeyChain.DoesNotExist:
        raise ValueError
    
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
            return ("-1", None)
        else:
            print("Bicycle is not in any holder - adding it")
            status = bicycle_holder.add_bicycle(bicycle)
            
            if status[0] == 0:
                print("Bicycle added C:")
                return ("0.1", status[1])
            elif status[0] == 1:
                print("Bicycle is not a real bicycle!")
                return ("0.2", None)
            elif status[0] == 2:
                print("There is no empty place")
                return ("0.3", None)
    else:
        print("There is bicycle C: - removing it")
        status = bicycle_holder.del_bicycle(bicycle)
        if status is not -1:
            print("Bicycle deleted succesfully")
            return ("1.1", status[1])
        else:
            print("Bicycle not in holder")
            return ("1.2", None)


def recv(request):
    if request.method == "POST":
        # Receive UUID
        post_data = str(request.body.decode())
        try:
            # Parse json data
            data = json.loads(post_data)
            # Obtain the uuid and ip data from json
            uuid = data['uuid']
            ipaddr = data['ip']
        except Exception:
            print("## Data received cannot be parsed")
            response = HttpResponse(
                status_code=406,
                closed=True
            )
            return response

        # Print log
        print(f"UUID: {uuid}. FROM: {ipaddr}")

        # Pass UUID and pico_w's ip address, to controller function.
        try:
            controller_data = controller(uuid, ipaddr)
        except ValueError:
            print("## Data given is not valid")
            response = HttpResponse(
                status_code=406,
                closed=True
            )
            return response

        json_data = {
            "code": controller_data[0],
            "slot_to_open": controller_data[1]
        }

        response = HttpResponse(
            json.dumps(json_data),
            headers={"Content-Type": "application/json",},
            status_code=200,
            closed=True
        )
        return response
    
    else:
        # Return 400 status code
        response = HttpResponse(
            status_code=400,
            close=True
        )

    return response
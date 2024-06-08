import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from core import models as core_models
from django.utils.timezone import make_aware

from django.views.decorators.csrf import csrf_exempt


def controller(keychain_uuid, esp_ip_addr):
    """_summary_

    Args:
        keychain_uuid (str): keychain UUID
        esp_ip_addr (str): ESP32 ip address

    Returns:
        tuple:(code, index to open)
    """
    try:
        keychain_uuid = str(keychain_uuid)
    except ValueError:
        print("Cannot cast keychain_uuid to string")
        raise ValueError

    try:
        esp_ip_addr = str(esp_ip_addr)
    except ValueError:
        print("Cannot cast esp_ip address to string")
        raise ValueError

    try:
        # Get the esp instance with that ip_addr
        esp_module = core_models.EspModule.objects.get(ip_address=esp_ip_addr)
        print(f"#######: Module: {esp_module}")
    except core_models.EspModule.DoesNotExist:
        print("### ESP Module does not exist")
        raise ValueError
    
    # Refresh esp_module latest_online time
    naive_datetime = datetime.now()
    awake_datetime = make_aware(naive_datetime)
    esp_module.latest_online = awake_datetime
    esp_module.save()

    try:
        # Get the KeyChain object related to keychain_uuid
        keychain = core_models.KeyChain.objects.get(uuid=keychain_uuid)
    except core_models.KeyChain.DoesNotExist:
        print("### Keychain does not exist")
        raise ValueError

    # Find the Bicycleholder instance corresponding to esp_module's instance
    bicycle_holder = esp_module.bicycleholder
    print(f"#######: Holder: {bicycle_holder}")

    # Get the user related to KeyChain instance.
    user = keychain.user
    print(f"#######: User: {user}")
    
    # Get a list which contains the user's bicycle's PKs
    try:
        bicycle = user.bicycle_set.all()[0]
    except IndexError:
        print("### No bicycle found associated with user")
        raise ValueError

    if not bicycle:
        print("## There are no bicycles associated with user")
        raise ValueError

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
                bicycle.is_saved=True
                bicycle.save()
                return ("0.1", status[1])
            elif status[0] == 1:
                print("Bicycle is not a real bicycle!")
                return ("0.2", None)
            elif status[0] == 2:
                print("There is no empty place")
                return ("0.3", None)
    else:
        print("There is bicycle C: - removing it")
        aval_index = bicycle_holder.del_bicycle(bicycle)
        if aval_index != -1:
            print("Bicycle deleted succesfully")
            bicycle.is_saved=False
            bicycle.save()
            return ("1.1", aval_index)
        else:
            print("Bicycle not in holder")
            return ("1.2", None)

@csrf_exempt
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
            print("\n## Data received cannot be parsed\n")
            response = HttpResponse()
            response.status_code=406
            response.close()
            return response

        # Print log
        print(f"\n## UUID: {uuid} FROM: {ipaddr}")

        # Pass UUID and pico_w's ip address, to controller function.
        try:
            controller_data = controller(uuid, ipaddr)
        except ValueError:
            print("## Data given is not valid\n")
            response = HttpResponse()
            response.status_code=418
            response.close()
            return response

        json_data = {
            "code": controller_data[0],
            "slot_to_open": controller_data[1]
        }

        response = HttpResponse(
            json.dumps(json_data),
        )
        response.headers={"Content-Type": "application/json"}
        response.status_code=200
        response.close()
        return response
    
    else:
        response = HttpResponse()
        response.status_code=400
        response.close()

    return response
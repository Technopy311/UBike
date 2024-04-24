from django.shortcuts import render, redirect
from django.http import HttpResponse


def auth_user():
    pass


def controller(keychain_uuid, picow_ip_addr):
    # Receive keychain_uuid
    # Find the Bicycleholder instance corresponding to picow_ip_addr
    # Get the KeyChain object related to kychain_uuid
    # Get the user related to KeyChain instance.
    # Create a list which contains the user's bicycle's PKs
    # Check which of the PKs is in the Bicycleholder
    
    pass


def recv(request):
    if request.method == "POST":
        # Receive UUID
        # Parse keychain UUID
        # Get the pico_w module's ip address.
        
        # Pass UUID and pico_w's ip address, 
        # to controller function.
        
        pass
    else:
        response = HttpResponse()
        response.status_code = 400
        response.closed = True

        return response
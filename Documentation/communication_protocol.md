# Communication Protocol between Server and ESP32 module

## Description
This document describes verbally how is established the communication 
through HTTP between the main Server and the ESP32 module, how it behaves
and the primitive protocol that has been created to allow this nexus.

### The concept

In first place, it is necessary to have in mind that this protocol has been
designed for a simple thing as objective, and it is to:

<ol> 
    <li>Allow the ESP32 module send the authentication data it gathers from the User's physical RFID Keychain, identify itself, and get the response back from the server.</li>
    <li>Allow the server tell the ESP32 if it needs to open a slot to permit the saving or remotion of bicycles if needed or pertinent.</li>
</ol>

Issues related to security will not be addressed by now, since it has been left for the last stage of the project, and could even not be included for the final delivery.

### First part: From ESP32 to the Server.

In this project, we have got to the necessity of identifying each user, so that way we can keep 
track of his bicycle and know his identity.

For such, we have decided to utilize a simple RFID Keychain. 
Why RFID? because it is very easy to implement this protocol in the ESP32 and other boards, through the use of libraries. 

In this consists the first step of the communication: Reading the Unique Identifier of the user's Keychain.
After performing such read, we save the value of it.

Now comes the second step, sending the data, to accomplish it, we first have to connect the board to Wifi, but that item is not covered in this documment; going forward and assuming Wifi connection, the board proceeds to create an HTTP POST request, an HTTP request is a petition to a web server, just like when a normal everyday user surfs the net, whenever this user wants to access a page (by clicking a link for example), the computer has to perform a request. The usual request, is to get something from the web server, and this kind of request is known as a GET request, but in this case, it is necessary to send data to the server, that is why the ESP32 has to perform a POST request. The HTTP communication is performed by already available libraries. 

For the POST request, there are a few things needed:
- URL: The "link" of the web server.
- UUID: The Unique Identifier of the Keychain.
- IP Address of the board.

This three elements allow us to start a connection to the server, by sending this data in a JSON format arbitrary set up by us (the developers). JSON you may ask, is a text format, which makes easy to standarize the access to information, you may think of it as a standard which allows you to say "Hey, I want the data to be in this order, and so on"

In this case, the JSON data we send, looks like this:
```{ "uuid": UUID OF THE KEYCHAIN, "ip": IP ADDRESS OF THE BOARD}```

That way, when receiving the data in the server, the server can inmediatly check the data with the name 'uuid' and 'ip', and access such elements.

### Second part: In the Server.

Assuming the request sent from the board has succesfully arrived at the web server, the server can now do things with this request, for the project's purposes, it is first mandatory to check if the data is the right data.

For this, we first make sure that the request is a POST request, if it isn't, we throw it away.
Then, we make sure that the JSON data (as show before) exists, and has the information we need, else we throw it away.

After this, we can perform a second step, the most important one, use the data!

#### Using the data

The flow is as follows:

<ol>
    <li>Check if the UUID is an integer value.</li>
    <li>Get the Keychain with such UUID from the Database (DB).</li>
    <li>Get the ESP32 module with the same IP Address from the DB.</li>
    <li>Access the Bicycle Holder associated with the ESP32 module.</li>
    <li>Access the user related to the Keychain.</li>
    <li>Try to get the user's Bicycle.</li>
    <li>Check if the Bicycle is in the Bicycle Holder.</li>
    <li>If the Bicycle is not in the Holder, check if its in another holder.</li>
    <li>If the Bicycle is not in another holder, add it to the Bicycle holder</li>
    <li>If the Bicycle is in the holder, then remove it from it.</li>
</ol>

Each time any step in this sequence fails, the server sends a response to the ESP32 telling it that it
failed... Well... almost.

In the steps 8, 9 and 10, the server sends some special responses to the board, allowing it to know that this
special cases have ocurred.

### Second part, part 2?: From the Server to the ESP32:

Keeping with the idea of the special cases, we have aggreed to create a special language to communicate and let know the board what has happened.

Since this is programming, we have chosen to use a tuple to make easier this task, it is like this "(elem1, elem2, elem3, ..., elemN)"

Why? Because once created you can't change them, this prevents from errors happening while the server is running; and because it is intuitive the way to access the data in them, like a list. For more details, use google.

The format for the tuple we use, is like so: ```(code, index_slot)```

The code, is the element which allows the board to know what situation has happened; and the index_slot is the number of slot that the ESP32 has to open.

This are the situations that could happen, and the tuple created for the case:

- Bicycle is in another holder: ("-1", None)
- Bicycle added to holder: ("0.1", slot_position)
- Bicycle is not a real bicycle: ("0.2", None)
- There is no empty place: ("0.3", None)
- Bicycle removed from holder: ("1.1", slot_position)
- Bicycle not in holder: ("1.2", None)

After this, we take the tuple data, and we give it to a JSON object which looks like so:
```
    {
      "code": controller_data[0],
      "slot_to_open": controller_data[1]
    }
```

In the "code" part, we put the first item of the tuple, and in the "slot_to_open" we put the second item of the tuple.

Then we send an HTTP response to the ESP32 Board, with the data, and a HTTP status code of 200, which lets know the ESP32 know that the connection has been successful.

### Third and last part: Back in the ESP32.

This element has not yet coded, but it is very trivial, something to be done after finishing tests in the communication, to make sure it works smoothly, fast and very robust.
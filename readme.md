# UBike IWG101 Project

## Brief description

This project created for Introduction to Engineering (IWG101), consists in the research and consequently development 
of an automated bicycle holder, this with the purpose of optimizing the saving process of a bicycle in the university.

## Technologies involved

### Software

Web:
- Django Framework (Backend)
- Bootstrap Library (Frontend)

Hardware:
- ESP32 C++/Arduino custom code.

### Hardware

- ESP32 Dev Kit 1, as microcontroller.
- RFID reader module (RC522).
- Red LED.
- Custom primary security system.
- Relay.
- Solenoid.

### Primary security system
Each module will have a security system, wich will activate in cases such:
- Improper module handling.
- Energy outage.
- Robbery attempt.

Under this events, this system will become active, this prevents the unlocking of the solenoide, unless a designated manager solves the conflict or issue


## Working process:
- A series of modules will be available, each one in a parking site.
- All the modules will connect through WiFi, to a centralized server, which will be in charge of managing the authentication, permissions, registering, among others.
- The authentication will be made through the Unique ID of each keychain (provided to each user, per bicycle).
- Once authenticated (and server-side confirmed), the solenoid will contract for a few seconds, allowing the user to save the bicycle.
- It is necessary perform the authentication to either save or take out the bicycle, this with the objective to improve security and backup records.
- The LED will indicate through blinking, the status of the solenoid.

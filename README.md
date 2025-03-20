# GPS-MAPS-Integration

## Overview
GPS-MAPS-Integration is a project that enables real-time GPS tracking using an Arduino and a Python-based desktop application. The system consists of an Arduino with a GPS module that transmits location coordinates to a PC via serial communication. The PC application then processes these coordinates and displays them as markers on an interactive map using `tkintermapview`.

## Features
- Real-time GPS coordinate tracking.
- Interactive map display using `tkintermapview`.
- Serial communication between Arduino and PC.
- Lightweight and easy-to-use interface.

## Hardware Requirements
- Arduino (e.g., Arduino Uno, Mega, or similar)
- GPS Module (e.g., NEO-6M)
- USB cable for Arduino-PC communication
- Computer with Python installed

## Software Dependencies
Ensure you have the following dependencies installed before running the Python script:
```bash
pip install tkintermapview pyserial customtkinter
```

## Installation & Usage
### 1. Setup the Arduino
1. Connect the GPS module to the Arduino:
   - **VCC** → 5V
   - **GND** → GND
   - **TX** → Arduino RX (Pin 4 or SoftwareSerial RX)
   - **RX** → Arduino TX (Pin 3 or SoftwareSerial TX)
2. Upload the provided Arduino sketch (`arduino_gps.ino`) to your Arduino.

### 2. Run the Python Application
1. Connect the Arduino to your PC via USB.
2. Run the Python script to start tracking:
   ```bash
   python Gui.py
   ```
3. The map interface should open, displaying the received GPS coordinates as markers.

## How It Works
1. The Arduino reads GPS data from the GPS module and extracts latitude and longitude.
2. The extracted coordinates are sent to the PC over serial communication.
3. The Python script reads the incoming data, parses the coordinates, and updates the map.
4. The map dynamically updates with each new coordinate received.

## Future Improvements
- Implement a route-tracking feature.
- Store GPS logs for analysis.
- Improve error handling for better stability.


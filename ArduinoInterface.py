import serial
import threading



def ddm_to_dd(ddm, is_longitude=False):
    degree_digits = 3 if is_longitude else 2
    degrees = int(ddm[:degree_digits])  
    minutes = float(ddm[degree_digits:])  
    return degrees + (minutes / 60)

def seperate_data(data: str):
    key = []
    value = []
    flag = False
    for char in data:
        if not flag and char != ":":
            key.append(char)
        elif flag and char != ":":
            value.append(char)
        else:
            flag = True
    key = "".join(key)
    try:
        value = float("".join(value).replace(" ", ""))
    except ValueError:
        direction = value[-1]
        value[-1] = " "
        value = "".join(value).replace(" ", "")
        if key == "Longitude":
            value = ddm_to_dd(value, True)
            value = -value if direction == "W" else value
        elif key == "Latitude":
            value = ddm_to_dd(value, False)
            value = -value if direction == "S" else value

    return key, value
            
        


class SerialRead:
    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        self.data_dictionary = {}
        self.comm_thread = threading.Thread(target=self.connect)
        self.comm_thread.start()
        
    
    def connect(self):
        try:
            self.link = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=1)
            print("Connection Successfull!")
            new_data_dictionary = {}
            while True:
                if self.link.in_waiting > 0:
                    data = self.link.readline().decode('utf-8').strip()
                    if data == "#":
                        self.data_dictionary = new_data_dictionary
                        new_data_dictionary = {}
                    elif data:
                        key, value = seperate_data(data)
                        new_data_dictionary[key] = value 
        except serial.SerialException as exception:
            print("Error:", exception)
        finally:
            self.link.close()
            print("Connection Closed!")





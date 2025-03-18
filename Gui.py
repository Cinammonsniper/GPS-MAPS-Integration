import tkinter as tk
from PIL import Image, ImageTk
from MapsAPI import MapFetcher
from ArduinoInterface import SerialRead

#TODO move this function to MapsAPI script
def ddm_to_dd(ddm, is_longitude=False):
    # Longitude has 3-degree digits, Latitude has 2
    degree_digits = 3 if is_longitude else 2
    
    # Extract degrees and minutes correctly
    degrees = int(ddm[:degree_digits])  
    minutes = float(ddm[degree_digits:])  
    return degrees + (minutes / 60)


#TODO add zoom and map size functionality 

class Gui:
    def __init__(self):
        self.maps = MapFetcher(20, (400,400), (24.840084,67.004673))
        self.arduino_data = SerialRead("/dev/ttyUSB0", 9600)

    def update_image(self):
        if self.arduino_data.data_dictionary:
            coordinates= (self.arduino_data.data_dictionary["Latitude"], self.arduino_data.data_dictionary["Longitude"])
            latitude_dd = ddm_to_dd(coordinates[0][:-1])  # Remove 'N'
            longitude_dd = ddm_to_dd(coordinates[1][:-1], is_longitude=True)  # Remove 'E'

            if coordinates[0][-1] == 'S':  
                latitude_dd = -latitude_dd
            if coordinates[1][-1] == 'W':  
                longitude_dd = -longitude_dd

            coordinates = (latitude_dd, longitude_dd)

            self.maps.update_coordinates(coordinates)
        self.display_image()
        self.root.after(1000, self.update_image)

    def display_image(self):
        image_path = "display_image.png"
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.Resampling.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.img_tk)

    def main(self):
        self.root = tk.Tk()
        self.root.title("MAP APP")
        self.root.geometry("400x400")
        self.image_label = tk.Label(self.root)
        self.update_image()
        self.display_image()
        self.image_label.pack()


        self.root.mainloop()

gui = Gui()
gui.main()# Given coordinates in DDM format

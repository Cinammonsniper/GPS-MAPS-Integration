import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
from MapsAPI import MapFetcher
from ArduinoInterface import SerialRead




class Gui:
    def __init__(self):
        self.maps = MapFetcher(20, (24.840084,67.004673))
        self.arduino_data = SerialRead("/dev/ttyUSB0", 9600)
        customtkinter.set_appearance_mode("light")

    def update_image(self):
        if self.arduino_data.data_dictionary:
            coordinates= (self.arduino_data.data_dictionary["Latitude"], self.arduino_data.data_dictionary["Longitude"])
            self.maps.update_coordinates(coordinates)
        self.display_image()
        self.root.after(1, self.update_image)

    def display_image(self):
        image_path = "display_image.png"
        img = Image.open(image_path)
        img = img.resize((600, 600), Image.Resampling.LANCZOS)
        self.img_tk = customtkinter.CTkImage(light_image=img,
                                  dark_image=img,
                                  size=(600, 600))
        self.image_label.configure(image=self.img_tk)

    def zoom(self, value):
        self.maps.change_parameters(int(value))

    def main(self):
        self.root = customtkinter.CTk()
        self.root.geometry("600x700")
        self.root.title("GPS-MAP-INTEGRATION")
        self.slider = customtkinter.CTkSlider(self.root, from_=0, to=30, number_of_steps=30, width=400, height=20, command=self.zoom)
        self.image_label = customtkinter.CTkLabel(self.root)
        self.update_image()
        self.display_image()
        self.image_label.grid(column=0, row=0)
        self.slider.grid(column=0, row=1, pady=35)

        self.root.mainloop()

gui = Gui()
gui.main()

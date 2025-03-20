import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
from ArduinoInterface import SerialRead
import tkintermapview




class Gui:
    def __init__(self):
        self.arduino_data = SerialRead("/dev/ttyUSB0", 9600)
        customtkinter.set_appearance_mode("light")
        self.follow = True

    def update_image(self):
        if self.arduino_data.data_dictionary:
            if self.follow:
                self.map_widget.set_position(self.arduino_data.data_dictionary["Latitude"], self.arduino_data.data_dictionary["Longitude"])
            self.my_pos.set_position(self.arduino_data.data_dictionary["Latitude"], self.arduino_data.data_dictionary["Longitude"])
        self.root.after(1, self.update_image)

    def change_value(self):
        if self.follow:
            self.switch.configure(text="OFF")
            self.follow = False
        else:
            self.switch.configure(text="ON")
            self.follow = True

    def main(self):
        self.root = customtkinter.CTk()
        self.root.geometry("650x500")
        self.r_font = customtkinter.CTkFont(family="Roboto", size=27)
        self.r_font_2 = customtkinter.CTkFont(family="Roboto", size=20)
        self.root.title("GPS-MAP-INTEGRATION")
        self.root.resizable(False, False)
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=500, height=600, corner_radius=0)
        self.my_pos = self.map_widget.set_marker(0, 0,text="My Position")
        self.lock_text = customtkinter.CTkLabel(self.root, text="Follow", width=150, font=self.r_font)
        self.switch = customtkinter.CTkSwitch(self.root, text="ON", command=self.change_value,
                                onvalue=True, offvalue=False, width=50, height=50, switch_width=50, switch_height=25, font=self.r_font_2)
        self.switch.select()
        self.map_widget.grid(row=0, column=0, rowspan=4)
        self.lock_text.grid(row=0, column=1)
        self.switch.grid(row=1, column=1, sticky="n")
        self.update_image()

        self.root.mainloop()

gui = Gui()
gui.main()

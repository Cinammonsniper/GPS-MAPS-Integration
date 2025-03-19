import googlemaps
import cv2
import math
from APIKey import APIKey as KEY
import threading


API_KEY = KEY().return_key() #Add your api key here as a string

def calculate_distance(old_coords: tuple[float], new_coords:tuple[float]):
    R = 6371000  # Earth radius in meters
    lat_1, long_1 = (math.radians(old_coords[0]), math.radians(old_coords[1]))
    lat_2, long_2 = (math.radians(new_coords[0]), math.radians(new_coords[1]))
    delta_lat = lat_1-lat_2
    delta_long = long_1-long_2
    a = math.sin(delta_lat/2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(delta_long/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance



class MapFetcher:
    def __init__(self, zoom: int, coordinates: tuple[int]):
        self.client = googlemaps.Client(key=API_KEY)
        self.zoom = zoom
        self.coordinates = coordinates
        self.image = "map.png"
        self.zoom_flag = False
        self.get_image()

    def change_parameters(self, zoom):
        self.zoom = zoom
        self.zoom_flag = True

    def get_image(self) -> None:
        image = open(self.image, 'wb')
        for chunk in self.client.static_map(size=(600,600),
                                    center=self.coordinates,
                                    zoom=self.zoom):
            if chunk:
                image.write(chunk)

        image.close()
        image = cv2.imread(self.image)

        height, width, _ = image.shape

        center = (width // 2, height // 2)

        cv2.circle(image, center, radius=4, color=(0, 0, 255), thickness=-1)
        cv2.imwrite("display_image.png", image)



    def update_coordinates(self, coordinates: tuple[int]):
        if self.zoom_flag:
            self.get_image()
            self.zoom_flag = False
        distance = calculate_distance(self.coordinates, coordinates)
        if distance > 5:
            print(distance)
            self.get_image()
            self.coordinates = coordinates



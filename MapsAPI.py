import googlemaps
import cv2
from APIKey import APIKey as KEY


API_KEY = KEY.return_key() #Add your api key here as a string


class MapFetcher:
    def __init__(self, zoom: int, size: tuple[int], coordinates: tuple[int]):
        self.client = googlemaps.Client(key=API_KEY)
        self.zoom = zoom
        self.size = size
        self.coordinates = coordinates
        self.image = "map.png"
        self.get_image()

    def change_parameters(self, zoom:int = -1, size:tuple[int] = (-1,-1)):
        flag = False
        if zoom != -1:
            self.zoom = zoom
            flag = True
        if size != (-1,-1):
            self.size = size
            flag = True
        
        if flag:
            return self.get_image()

    def get_image(self) -> None:
        image = open(self.image, 'wb')
        for chunk in self.client.static_map(size=self.size,
                                    center=self.coordinates,
                                    zoom=self.zoom):
            if chunk:
                image.write(chunk)

        image.close()
        image = cv2.imread(self.image)

        height, width, _ = image.shape

        center = (width // 2, height // 2)

        cv2.circle(image, center, radius=2, color=(0, 0, 255), thickness=-1)
        cv2.imwrite("display_image.png", image)



    def update_coordinates(self, coordinates: tuple[int]):
        self.coordinates = coordinates
        self.get_image()
        #TODO add the coordiante difference checker to minimize api calls



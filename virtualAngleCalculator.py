import argparse
import cv2
import math


class VirtualAngleCalculator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.coordinates = list()
        self.point = tuple()
        self.angle = 0
        cv2.namedWindow('Image')

    #Reading the image
    def read_image(self):
        self.image = cv2.imread(self.image_path)
        return self.image

    #Displaying the image
    def display_image(self):
        cv2.imshow('Image', self.image)
        return

    #Checking the mouse event and then storing or removing the coordinates based on the event
    def record_mouse_coordinates(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point = (x, y)
            self.coordinates.append(self.point)
            cv2.circle(self.image, self.point, 5, (0, 0, 255), cv2.FILLED)

        elif event == cv2.EVENT_RBUTTONDOWN and self.coordinates:   
            self.coordinates.pop()
            self.image = cv2.imread(self.image_path)
            for coordinate in self.coordinates:
                cv2.circle(self.image, coordinate, 5, (0, 0, 255), cv2.FILLED)      
        return 

    #Calculating the distance between two points using Euclidean formula
    def euclidean_distance(self, p1, p2):
        return math.sqrt(sum([(x - y) ** 2 for x, y in zip(p1, p2)]))

    #Finding the angle using the Law of Cosines
    def find_angle(self):
        origin, point1, point2 = self.coordinates[-3:]
        a = self.euclidean_distance(origin, point1)
        b = self.euclidean_distance(origin, point2)
        c = self.euclidean_distance(point1, point2)
        try:
            self.angle = round(math.degrees(math.acos(((a**2) +
                                             (b**2) - (c**2)) / (2*a*b))))
        except:
            self.angle = 0
        self.image = cv2.line(self.image, origin, point1, (0, 0, 255), 2) 
        self.image = cv2.line(self.image, origin, point2, (0, 0, 255), 2)
        cv2.putText(self.image, str(self.angle), (origin[0]+20, origin[1]-20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)


    def calculate(self):
        self.read_image()
        while(True):
            self.display_image()
            cv2.setMouseCallback('Image', self.record_mouse_coordinates)
            if self.coordinates and len(self.coordinates) % 3 == 0 :
                self.find_angle()
            #Resetting the image
            if cv2.waitKey(1) == ord('r') or cv2.waitKey(1) == ord('R'):
                self.coordinates = []
                self.image = cv2.imread(self.image_path)
            #Removing the previous point
            elif cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
                break

#Parsing the argument passed while executinig the program file to get the image path
def argument_parser():
    parser = argparse.ArgumentParser(description = "Find the Angle within any given image")
    parser.add_argument('--path',
                        metavar = 'image_path',
                        type = str,
                        help = 'Path to the image in which the angle need to be found',
                        required = True)
    args = parser.parse_args()
    return args.path


if __name__ == "__main__":
    imagePath = argument_parser()
    VirtualAngleCalculator(imagePath).calculate()
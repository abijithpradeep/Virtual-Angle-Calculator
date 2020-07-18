import argparse
import cv2
import math

#Parsing the argument to collect the image path
def argument_parser():
    parser = argparse.ArgumentParser(description = "Find the Angle within any given image")
    parser.add_argument('--path',
                        metavar = 'image_path',
                        type = str,
                        help = 'Path to the image in which the angle need to be found',
                        required = True)
    args = parser.parse_args()
    return args.path

#Saving or removing the point coordinates based on the event.
def record_mouse_coordinates(event, x, y, flags, param):
    global image
    #Saving the point coordinate
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        param[0].append(point)
        cv2.circle(image, point, 5, (0, 0, 255), cv2.FILLED)
    #Removing the previous point coordinate
    elif event == cv2.EVENT_RBUTTONDOWN and param[0]:   
        param[0].pop()
        image = cv2.imread(param[1])
        for p in param[0]:
            cv2.circle(image, p, 5, (0, 0, 255), cv2.FILLED)      
    return 

#Calculates distance between two points
def euclidean_distance(p1, p2):
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(p1, p2)]))

#Calculating angle based on Law of Cosines
def calculate_angle(points):
    global image
    origin, point1, point2 = points
    a = euclidean_distance(origin, point1)
    b = euclidean_distance(origin, point2)
    c = euclidean_distance(point1, point2)
    try:
        angle = round(math.degrees(math.acos(((a**2) + (b**2) - (c**2)) / (2*a*b))))
    except:
        angle = 0
    #Drawing lines
    image = cv2.line(image, origin, point1, (0, 0, 255), 2) 
    image = cv2.line(image, origin, point2, (0, 0, 255), 2)
    #Displaying the calculated angle
    cv2.putText(image, str(angle), (origin[0]+20, origin[1]-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

def main():
    global image
    image_path = argument_parser()
    image = cv2.imread(image_path)
    coordinates = list()
    cv2.namedWindow('Image')
    while(True):
        cv2.imshow('Image', image)
        cv2.setMouseCallback('Image', record_mouse_coordinates, param = [coordinates, image_path])
        if cv2.waitKey(1) == ord('r'):
            coordinates = []
            image = cv2.imread(image_path)
        elif cv2.waitKey(1) == ord('q'):
            break
        if coordinates and len(coordinates) % 3 == 0 :
            angle = calculate_angle(coordinates[-3:])
            

if __name__ == "__main__":
    main()

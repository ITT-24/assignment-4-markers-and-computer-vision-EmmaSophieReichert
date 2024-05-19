import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

INPUT_PATH = "sample_image.jpg"
OUTPUT_PATH = ""
RESULUTION = (3508,2480) #DIN A4: https://www.schlender.de/din-formate/

# get command line parameters
if len(sys.argv) > 1:
    INPUT_PATH = str(sys.argv[1])
    if len(sys.argv) > 2:
        OUTPUT_PATH = str(sys.argv[2])
        if len(sys.argv) > 3:
            RESULUTION = resolution = tuple(map(int, str(sys.argv[3]).split('x')))

#adjusted code from opencv_click.py

img = cv2.imread(INPUT_PATH)
img_to_draw = img.copy() #make a deep copy to draw points on
WINDOW_NAME = 'Selection Window'
RESULT_WINDOW_NAME = 'Result View'

result_view = False
current_result = img

selected_points = []

cv2.namedWindow(WINDOW_NAME)

def reset():
    global img_to_draw, selected_points, result_view
    cv2.imshow(WINDOW_NAME, img)
    img_to_draw = img.copy()
    selected_points = []
    result_view = False

# used GPT for this method - stores selected points in the right order
def order_points():
    global selected_points

    #sort upon x-axes
    selected_points.sort(key=lambda x: x[0])

    # Divide the coordinates into left and right groups
    left_coordinates = selected_points[:2]
    right_coordinates = selected_points[2:]

    # Sort each group based on the y-coordinate
    left_coordinates.sort(key=lambda x: x[1])
    right_coordinates.sort(key=lambda x: x[1])

    # Sort the coordinates from up left to right, to down left to right
    selected_points = [left_coordinates[0], right_coordinates[0], left_coordinates[1], right_coordinates[1]]

# used https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html Perspective Transform
def show_wrapped_result():
    global result_view, current_result

    order_points()
    pts1 = np.float32(selected_points)
    pts2 = np.float32([[0,0],[RESULUTION[0],0],[0,RESULUTION[1]],[RESULUTION[0],RESULUTION[1]]])
    
    M = cv2.getPerspectiveTransform(pts1, pts2)
    
    dst = cv2.warpPerspective(img,M,RESULUTION)
    
    cv2.imshow(WINDOW_NAME, dst)
    result_view = True
    current_result = dst

def mouse_callback(event, x, y, flags, param):
    global img_to_draw

    if event == cv2.EVENT_LBUTTONDOWN:
        img_to_draw = cv2.circle(img_to_draw, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(WINDOW_NAME, img_to_draw)
        selected_points.append([x, y])
        if(len(selected_points) >= 4):
            show_wrapped_result()

#save image to output path
def save_img():
    print("SAVE")
    global current_result
    output_filename = os.path.splitext(INPUT_PATH)[0] + "_transformed.jpg"
    cv2.imwrite(os.path.join(OUTPUT_PATH, output_filename), current_result) #https://stackoverflow.com/a/41587740

cv2.imshow(WINDOW_NAME, img)

cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

while True:
    key = cv2.waitKey(1)
    
    if key == 27: #ESC key: https://manivannan-ai.medium.com/keyboard-control-for-save-image-and-destroywindow-in-opencv-335c084fe742
        reset()

    elif key == ord('s'):
        print("SAVE")
        if(result_view):
            save_img()
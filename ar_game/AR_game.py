import pyglet
import sprite_getter
import random
import time
from opencv_pyglet import cv2glet
import cv2
import sys
import game_rectangle as gr

add_object_time = 10

#size of paper
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

WIDTH_SHIFT = 50

falling_objects = []

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

class Falling_Object:
    def __init__(self, type, position) -> None:
        self.type = type
        if(type == "fruit"):
            self.sprite = sprite_getter.get_fruit()
        else:
            self.sprite = sprite_getter.get_leaf()
        self.sprite.y = WINDOW_HEIGHT
        self.sprite.x = position
    
    def check_collision(self) -> bool:
        return False

    def draw(self) -> None:
        self.sprite.y -= 1 #move object down
        self.sprite.draw()

def add_new_falling_object(dt, position):
    global add_object_time

    add_object_time -= 0.01 #decrease time for next object

    type = "fruit"
    #produce a leaf every 4th time
    if(random.randint(1, 4) == 4):
        type = "leaf"

    falling_objects.append(Falling_Object(type, position +  random.uniform(-WIDTH_SHIFT, WIDTH_SHIFT)))
    pyglet.clock.schedule_once(add_new_falling_object, add_object_time + random.uniform(-1, 1), position = position)


add_new_falling_object(None, WINDOW_WIDTH * 0.25) #add some random value for generating and more fun
time.sleep(3)
add_new_falling_object(None, WINDOW_WIDTH * 0.75)
time.sleep(2)
add_new_falling_object(None, WINDOW_WIDTH * 0.5)

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

@window.event
def on_draw():
    global falling_objects
    window.clear()
    #ret, frame = cap.read()
    #img = cv2glet(frame, 'BGR')
    #img.blit(0, 0, 0)
    img = gr.get_game_rectangle(cap)
    img = cv2glet(img, 'BGR')
    img.blit(0, 0, 0)

    falling_objects_new = []
    for obj in falling_objects:
        obj.draw()
        if(obj.sprite.y > 0): #obj still visible
            falling_objects_new.append(obj)
    falling_objects = falling_objects_new #invisible objects are now deleted for better performance
    

pyglet.app.run()

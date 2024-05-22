import pyglet
import sprite_getter
import random
import time
from opencv_pyglet import cv2glet
import cv2
import sys
import game_rectangle as gr
import player

add_object_time = 10

WIDTH_SHIFT = 50

falling_objects = []

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
ret, frame = cap.read()
window_height, window_width, _ = frame.shape #should be webcam resolution
window = pyglet.window.Window(window_width, window_height)

class Falling_Object:
    def __init__(self, type, position) -> None:
        self.type = type
        if(type == "fruit"):
            self.sprite = sprite_getter.get_fruit()
        else:
            self.sprite = sprite_getter.get_leaf()
        self.sprite.y = window_height
        self.sprite.x = position
    
    def check_collision(self, pl) -> bool:
        x_mid_pos = int(self.sprite.x + sprite_getter.SPRITE_SIZE //2)
        y_mid_pos = int(self.sprite.y + sprite_getter.SPRITE_SIZE //2)
        if(window_height - y_mid_pos < len(pl) and x_mid_pos < len(pl[0])):
            #prevent form index out of bounds
            print(pl[window_height - y_mid_pos][x_mid_pos])
            if(pl[window_height - y_mid_pos][x_mid_pos] == 0): #changed window_height, because axis are different in cv2 and pyglet
                #it collides with the middle of the sprite
                return True
            return False

    def draw(self) -> None:
        self.sprite.y -= 1 #move object down
        self.sprite.draw()

def add_new_falling_object(dt, position):
    global add_object_time
    add_object_time -= 0.01 #decrease time for next object

    type = "fruit"
    #chance for a leaf is 1/4
    if(random.randint(1, 4) == 4):
        type = "leaf"

    falling_objects.append(Falling_Object(type, position +  random.uniform(-WIDTH_SHIFT, WIDTH_SHIFT)))
    pyglet.clock.schedule_once(add_new_falling_object, add_object_time + random.uniform(-1, 1), position = position)


add_new_falling_object(None, window_width * 0.25) #add some random value for generating and more fun
time.sleep(3)
add_new_falling_object(None, window_width * 0.75)
time.sleep(2)
add_new_falling_object(None, window_width * 0.5)

@window.event
def on_draw():
    global falling_objects
    window.clear()

    rect = gr.get_game_rectangle(cap)
    img = cv2glet(rect, 'BGR')
    img.blit(0, 0, 0)

    pl = player.get_player(rect)

    falling_objects_new = []
    for obj in falling_objects:
        collision = obj.check_collision(pl)
        obj.draw()
        if(obj.sprite.y > 0 and not collision): #obj still visible and has not collided
            falling_objects_new.append(obj)
    falling_objects = falling_objects_new #invisible objects are now deleted for better performance
    

pyglet.app.run()

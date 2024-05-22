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
FALL_DOWN_SPEED = 3

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
            #prevented form index out of bounds
            if(pl[window_height - y_mid_pos][x_mid_pos] == 0): #changed window_height, because axis are different in cv2 and pyglet
                #it collides with the middle of the sprite
                return True
            return False

    def draw(self) -> None:
        self.sprite.y -= FALL_DOWN_SPEED #move object down
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

def start_game():
    add_new_falling_object(None, window_width * 0.25)
    time.sleep(3)
    add_new_falling_object(None, window_width * 0.75)
    time.sleep(2)
    add_new_falling_object(None, window_width * 0.5)

score_label = pyglet.text.Label(str(0),
                                  x= 50, y=window.height - 50,
                                  anchor_x='center', anchor_y='center')
score_label.set_style('color', (0, 0, 0, 255))
score_label.set_style('font_name', 'Courier New')
score_label.set_style('font_size', 30) 
score_label.set_style('bold', True)

#variable for game start
first_detected = False 

game_score = 0

def restart_game():
    global game_score, first_detected, add_object_time, falling_objects
    game_score = 0
    first_detected = False 
    add_object_time = 10
    falling_objects = []
    sprite_getter.reset()
    gr.current_corners = []
    pyglet.clock.unschedule(add_new_falling_object)

def draw_end_screen():
    gratulations_label = pyglet.text.Label("WHOHOO, YOU REACHED " + str(game_score) + " POINTS",
                                  x=window.width // 2, y=(window.height // 2) + 50,
                                  anchor_x='center', anchor_y='center')
    gratulations_label.set_style('color', (255, 255, 255, 255))
    gratulations_label.set_style('font_name', 'Courier New')
    gratulations_label.set_style('font_size', 30) 
    gratulations_label.set_style('bold', True)
    gratulations_label.draw()

    play_again_label = pyglet.text.Label("Press R to play again!",
                                  x=window.width // 2, y=(window.height // 2) - 50,
                                  anchor_x='center', anchor_y='center')
    play_again_label.set_style('color', (255, 255, 255, 255))
    play_again_label.set_style('font_name', 'Courier New')
    play_again_label.set_style('font_size', 20) 
    play_again_label.set_style('bold', True)
    play_again_label.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.R:
        restart_game() #you can always press r to restart the game

@window.event
def on_draw():
    global falling_objects, first_detected, game_score
    window.clear()

    if not sprite_getter.is_end():
        rect, detection = gr.get_game_rectangle(cap)
        if(detection and not first_detected):
            start_game()
            first_detected = True
        img = cv2glet(rect, 'BGR')
        img.blit(0, 0, 0)

        pl = player.get_player(rect)

        falling_objects_new = []
        for obj in falling_objects:
            collision = obj.check_collision(pl)
            if(collision):
                if(obj.type == "fruit"):
                    game_score += 1
                elif(obj.type == "leaf"):
                    game_score -= 1
            obj.draw()
            if(obj.sprite.y > 0 and not collision): #obj still visible and has not collided
                falling_objects_new.append(obj)
        falling_objects = falling_objects_new #invisible objects are now deleted for better performance

        score_label.text = str(game_score)
        score_label.draw()
    else:
        draw_end_screen()

pyglet.app.run()

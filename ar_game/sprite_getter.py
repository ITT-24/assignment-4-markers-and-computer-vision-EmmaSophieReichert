import random
import os
import pyglet

FRUITS = ["06", "11", "08", "14", "07", "02", "04", "00", "10", "03"]
LEAFS = ["13", "33", "53", "46", "56"]
ENDING = ".png"
FRUIT_FOLDER_NAME = "sprites/fruit"
LEAF_FOLDER_NAME = "sprites/plants"

current_fruits = []
current_leafs = []

ADD_FRUIT_COUNTS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
ADD_LEAF_COUNTS = [0, 10, 20, 30, 40]

fruit_counter = 0
leaf_counter = 0

SPRITE_SIZE = 50

END_COUNT = 10 #adjust this, if you want the game to end earlier

def get_sprite(picture_path):
    img = pyglet.image.load(picture_path)
    img.anchor_x = img.width // 2 #set anchor to middle of the img
    img.anchor_y = img.height // 2
    sprite = pyglet.sprite.Sprite(img=img)
    sprite.update(scale_x=SPRITE_SIZE / img.width, scale_y=SPRITE_SIZE / img.height) #resize sprite
    return sprite

def get_fruit() -> str:
    global fruit_counter
    if(fruit_counter in ADD_FRUIT_COUNTS):
        #add a new fruit to the selection, when the counter reaches the defined counts
        current_fruits.append(FRUITS[len(current_fruits)])
    fruit_counter += 1
    fruit = random.choice(current_fruits)
    return get_sprite(os.path.join(FRUIT_FOLDER_NAME,fruit + ENDING))

def get_leaf() -> str:
    global leaf_counter
    if(leaf_counter in ADD_LEAF_COUNTS):
        #add a new fruit to the selection, when the counter reaches the defined counts
        current_leafs.append(LEAFS[len(current_leafs)])
    leaf_counter += 1
    leaf = random.choice(current_leafs)
    return get_sprite(os.path.join(LEAF_FOLDER_NAME, leaf + ENDING))

def is_end() -> bool:
    return fruit_counter >= END_COUNT

def reset() -> None:
    global current_fruits, current_leafs, fruit_counter, leaf_counter
    current_fruits = []
    current_leafs = []
    fruit_counter = 0
    leaf_counter = 0

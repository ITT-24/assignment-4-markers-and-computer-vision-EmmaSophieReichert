import cv2

#tried to find a fitting threshold for the paper and my hand
THRESHOLD = 175

def get_player(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #also flip the player img
    gray = cv2.flip(gray, 1)
    #used GPT for that line - THRESHOLD where it decides
    _, binary_frame = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY)
    return binary_frame
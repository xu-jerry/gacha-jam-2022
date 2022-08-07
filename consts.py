from enum import Enum

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 150
CELL_LENGTH = 64
SPRITE_SCALING = 1
MOVEMENT_SPEED = 5
PLAYER_STARTING_LOC = (6, 6)
MUSIC_VOLUME = 0.5
STARTING_HEALTH_POINTS = 3

class Direction(Enum):
    def __sub__(self, other):
        return self.value - other.value

    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def ypos(pos, factor):
    """ Returns y position based on pos # and scale factor """
    return SCREEN_HEIGHT - pos * factor + factor / 2

def xpos(pos, factor):
    """ Returns x position based on pos # and scale factor """
    return pos * factor + factor / 2

def top(factor):
    """ Returns top y position based on scale factor """
    return SCREEN_HEIGHT - factor / 2

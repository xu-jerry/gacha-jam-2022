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

class Direction(Enum):
    def __sub__(self, other):
        return self.value - other.value

    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
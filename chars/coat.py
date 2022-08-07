# Imports
import arcade
import time
from consts import *

class Coat(arcade.Sprite):
    """ Enemy Coats Class """

    def __init__(self, color, pos, dir=Direction.DOWN):
        """
        Spawns Coat enemy of color with direction and position
        - color (required): 'red', 'brown', 'tan'
        - pos (required): 1-14 for DOWN, 1-15 for LEFT/RIGHT
        - dir: Direction.DOWN (default), Direction.LEFT, Direction.RIGHT
        """

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = dir

        # --- Load Textures ---
        main_path = "./assets/coats/"

        # Load texture, DOWN by default
        self.texture = arcade.load_texture(f"{main_path}{color}coat.png")

        if dir == Direction.LEFT:
            self.texture = arcade.load_texture(f"{main_path}{color}coatleft.png")
        elif dir == Direction.RIGHT:
            self.texture = arcade.load_texture(f"{main_path}{color}coatright.png")

        # Spawn into pos
        if pos >= 1:
            if dir == Direction.DOWN and pos <= 14:
                self.center_x = pos * CELL_LENGTH + CELL_LENGTH / 2
                self.center_y = SCREEN_HEIGHT - CELL_LENGTH / 2
            elif (dir == Direction.LEFT or Direction.RIGHT) and pos <= 15:
                # X coordinate is either 1 * 960 for LEFT or 0 * 960 for RIGHT
                self.center_x = (Direction.LEFT - dir + 1) * 15 * CELL_LENGTH + CELL_LENGTH / 2
                self.center_y = SCREEN_HEIGHT - pos * CELL_LENGTH + CELL_LENGTH / 2

        # --- Fire fireballs ---
    

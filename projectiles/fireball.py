import arcade
import time
from consts import *

class Fireball(arcade.Sprite):
    """ Fireball projectile sprite """

    def __init__(self, pos, dir=Direction.DOWN, big=False):
        """ 
        Creates fireball
        - pos (required): 1-14 for DOWN, 1-15 for LEFT/RIGHT
        - dir: Direction.DOWN, Direction.LEFT, Direction.RIGHT
        - big: bool
        """

        super().__init__()

        # --- Load textures
        main_path = "./assets/"

        self.textures = []
        
        if big:
            main_path += "bigfire/"
            for i in range(2):
                self.textures.append(arcade.load_texture(f"{main_path}bigfire{i+1}.png"))
        else:
            main_path += "smolfire/"
            if dir == Direction.DOWN:
                for i in range(2):
                    self.textures.append(arcade.load_texture(f"{main_path}smolfiredown{i+1}.png"))
            elif dir == Direction.LEFT:
                for i in range(2):
                    self.textures.append(arcade.load_texture(f"{main_path}smolfireleft{i+1}.png"))
            elif dir == Direction.RIGHT:
                for i in range(2):
                    self.textures.append(arcade.load_texture(f"{main_path}smolfireright{i+1}.png"))

        # Spawn into pos
        if pos >= 1:
            if dir == Direction.DOWN and pos <= 14:
                self.center_x = xpos(pos, CELL_LENGTH)
                self.center_y = top(CELL_LENGTH) - CELL_LENGTH
            elif (dir == Direction.LEFT or Direction.RIGHT) and pos <= 15:
                # X coordinate is either 1 * 832 + 96 for LEFT or 96 for RIGHT
                self.center_x = (Direction.LEFT - dir + 1) * 13 * CELL_LENGTH + 3 * CELL_LENGTH / 2
                self.center_y = ypos(pos, CELL_LENGTH)

        self.texture = self.textures[0]

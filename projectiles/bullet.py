import arcade
import time
from consts import *

class Bullet(arcade.Sprite):
    """ Bullet projectile sprite """

    def __init__(self, pos, dir=Direction.DOWN):
        """ 
        Creates bullet
        - pos (required): tuple of location
        - dir: Direction.DOWN, Direction.LEFT, Direction.RIGHT
        """

        super().__init__()
        self.frame = 1  # Frame counter
        self.dir = dir
        self.anim_frame = 0

        # --- Load textures
        main_path = "./assets/bullet/bullet"

        self.textures = []
        if dir == Direction.DOWN or dir == Direction.UP:
            self.texture = arcade.load_texture(f"{main_path}vert.png")
        elif dir == Direction.LEFT or dir == Direction.RIGHT:
            self.texture = arcade.load_texture(f"{main_path}hor.png")

        # Spawn into pos
        self.center_x = xpos(pos[0], CELL_LENGTH)
        self.center_y = pos[1]* CELL_LENGTH + CELL_LENGTH / 2
    
    def update(self):
        if self.dir == Direction.DOWN:
            self.center_y -= CELL_LENGTH / 12
        elif self.dir == Direction.UP:
            self.center_y += CELL_LENGTH / 12
        elif self.dir == Direction.RIGHT:
            self.center_x += CELL_LENGTH / 12
        elif self.dir == Direction.LEFT:
            self.center_x -= CELL_LENGTH / 12

        if self.left > SCREEN_WIDTH or self.right < 0 or self.top < 0 or self.bottom > SCREEN_HEIGHT:
            self.kill()
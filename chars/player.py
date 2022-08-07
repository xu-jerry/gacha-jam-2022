import arcade
from consts import *

# Classes
class Player(arcade.Sprite):
    """ Player Class """

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-down
        self.direction = Direction.DOWN

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = SPRITE_SCALING

        # --- Load Textures ---
        main_path = "./assets/vanilla69/69"

        # Load textures for 4 directions
        self.down_textures = []
        self.up_textures = []
        self.left_textures = []
        self.right_textures = []

        for i in range(3):
            texture = arcade.load_texture(f"{main_path}down{i}.png")
            self.down_textures.append(texture)
        for i in range(3):
            texture = arcade.load_texture(f"{main_path}up{i}.png")
            self.up_textures.append(texture)
        for i in range(3):
            texture = arcade.load_texture(f"{main_path}left{i}.png")
            self.left_textures.append(texture)
        for i in range(3):
            texture = arcade.load_texture(f"{main_path}right{i}.png")
            self.right_textures.append(texture)

        # Set the initial texture
        self.texture = self.down_textures[0]
        self.prev_texture = 2

    def update(self):
        """ Move the player """
        # Move player.
        if self.dest_loc != self.cur_loc:
            self.change_x = (self.dest_loc[0] - self.cur_loc[0]) * MOVEMENT_SPEED
            self.change_y = (self.dest_loc[1] - self.cur_loc[1]) * MOVEMENT_SPEED

            # don't ask how I came up with these formulas ???
            if (self.left + self.change_x) // CELL_LENGTH != self.cur_loc[0] - 1 * (self.change_x < 0):
                self.cur_loc = self.dest_loc
                self.left = self.cur_loc[0] * CELL_LENGTH + 1
            else:
                self.left += self.change_x

            if (self.bottom + self.change_y) // CELL_LENGTH != self.cur_loc[1] - 1 * (self.change_y < 0):
                self.cur_loc = self.dest_loc
                self.bottom = self.cur_loc[1] * CELL_LENGTH + 1
            else:
                self.bottom += self.change_y

            # Check for out-of-bounds
            if self.left < 0:
                self.left = 0
            elif self.right > SCREEN_WIDTH - 1:
                self.right = SCREEN_WIDTH - 1

            if self.bottom < 0:
                self.bottom = 0
            elif self.top > SCREEN_HEIGHT - 1:
                self.top = SCREEN_HEIGHT - 1

            # change texture
            if self.direction == Direction.DOWN:
                if self.texture != self.down_textures[0]:
                    self.texture = self.down_textures[0]
                elif self.prev_texture == 2:
                    self.texture = self.down_textures[1]
                    self.prev_texture = 1
                else:
                    self.texture = self.down_textures[2]
                    self.prev_texture = 2
            elif self.direction == Direction.UP:
                if self.texture != self.up_textures[0]:
                    self.texture = self.up_textures[0]
                elif self.prev_texture == 2:
                    self.texture = self.up_textures[1]
                    self.prev_texture = 1
                else:
                    self.texture = self.up_textures[2]
                    self.prev_texture = 2
            elif self.direction == Direction.LEFT:
                if self.texture != self.left_textures[0]:
                    self.texture = self.left_textures[0]
                elif self.prev_texture == 2:
                    self.texture = self.left_textures[1]
                    self.prev_texture = 1
                else:
                    self.texture = self.left_textures[2]
                    self.prev_texture = 2
            else:
                if self.texture != self.right_textures[0]:
                    self.texture = self.right_textures[0]
                elif self.prev_texture == 2:
                    self.texture = self.right_textures[1]
                    self.prev_texture = 1
                else:
                    self.texture = self.right_textures[2]
                    self.prev_texture = 2

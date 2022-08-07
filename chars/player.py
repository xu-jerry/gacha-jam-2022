import arcade
from consts import *
from projectiles.bullet import Bullet

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
        self.main_path = "./assets/gun69/gun69"

        # Load textures for 4 directions
        self.down_textures = []
        self.up_textures = []
        self.left_textures = []
        self.right_textures = []

        for i in range(3):
            texture = arcade.load_texture(f"{self.main_path}down{i}.png")
            self.down_textures.append(texture)
        for i in range(3):
            texture = arcade.load_texture(f"{self.main_path}up{i}.png")
            self.up_textures.append(texture)
        for i in range(3):
            texture = arcade.load_texture(f"{self.main_path}left{i}.png")
            self.left_textures.append(texture)
        for i in range(3):
            texture = arcade.load_texture(f"{self.main_path}right{i}.png")
            self.right_textures.append(texture)

        # Set the initial texture
        self.texture = self.down_textures[0]
        self.prev_texture = 2

        # Health points
        self.health = STARTING_HEALTH_POINTS

        # Bullets
        self.bullets = []

    def update(self):
        """ Move the player """
        # Check if alive
        if (self.health <= 0):
            print("You died!")
            self.kill()
            arcade.close_window()

        # Move player.
        if self.dest_loc != self.cur_loc:
            if not self.in_grid(self.dest_loc):
                self.dest_loc = self.cur_loc
            self.change_x = (self.dest_loc[0] - self.cur_loc[0]) * MOVEMENT_SPEED
            self.change_y = (self.dest_loc[1] - self.cur_loc[1]) * MOVEMENT_SPEED

            # don't ask how I came up with these formulas ???
            if (self.center_x + self.change_x - CELL_LENGTH / 2) // CELL_LENGTH == self.dest_loc[0] - 1 * (self.change_x < 0):
                self.cur_loc = (self.dest_loc[0], self.cur_loc[1])
                self.center_x = self.cur_loc[0] * CELL_LENGTH + CELL_LENGTH / 2
            else:
                self.left += self.change_x

            if (self.center_y + self.change_y - CELL_LENGTH / 2) // CELL_LENGTH == self.dest_loc[1] - 1 * (self.change_y < 0):
                self.cur_loc = (self.cur_loc[0], self.dest_loc[1])
                self.center_y = self.cur_loc[1] * CELL_LENGTH + CELL_LENGTH / 2
            else:
                self.bottom += self.change_y

            # Check for out-of-bounds
            if self.center_x < CELL_LENGTH / 2:
                self.center_x = CELL_LENGTH / 2
            elif self.center_x > SCREEN_WIDTH - 1 - CELL_LENGTH / 2:
                self.center_x = SCREEN_WIDTH - 1 - CELL_LENGTH / 2

            if self.center_y < CELL_LENGTH / 2:
                self.center_y = CELL_LENGTH / 2
            elif self.center_y > SCREEN_HEIGHT - 1 - CELL_LENGTH / 2:
                self.center_y = SCREEN_HEIGHT - 1 - CELL_LENGTH / 2

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
        else:
            print("cur_loc", self.cur_loc)
            print("dest_loc", self.dest_loc)
            self.center_x = xpos(self.cur_loc[0], CELL_LENGTH)
            self.center_y = self.cur_loc[1] * CELL_LENGTH + CELL_LENGTH / 2
    
    def in_grid(self, loc):
        x, y = loc
        if x < 0 or x > 15:
            return False
        if y < 0 or y > 11:
            return False
        return True
    
    def shoot(self):
        self.bullets.append(Bullet(self.cur_loc, self.direction))
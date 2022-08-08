# Imports
import arcade
import time
import random
from consts import *
from projectiles.fireball import Fireball

class Madison(arcade.Sprite):
    """ Madison Class """

    def __init__(self):
        """
        Spawns the final boss: James Madison
        """

        # Set up parent class
        super().__init__()
        self.pos = 7.5
        self.dir = Direction.DOWN
        self.new_fireball = True
        self.health = 5

        # Load texture
        self.texture = arcade.load_texture(f"./assets/madison/madison.png")

        self.center_x = xpos(self.pos, CELL_LENGTH)
        self.center_y = top(128)

        self.fireball = Fireball(self.pos, self.dir, big=True)

    def update(self):
        self.new_fireball = False

        if self.fireball.center_y < -(CELL_LENGTH / 2):
            self.fireball.kill()
            self.new_fireball = True
            self.fireball = Fireball(self.pos, self.dir, big=True)
    
    def get_hit(self):
        self.health -= 1


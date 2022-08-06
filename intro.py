# Imports
import arcade

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 150
CELL_LENGTH = 64
SPRITE_SCALING = 1
MOVEMENT_SPEED = 5
PLAYER_STARTING_LOC = (6, 6)

# Classes
class Player(arcade.Sprite):
    """ Player Class """

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class Game(arcade.Window):
    """Main welcome window"""
    def __init__(self, width, height, title):
        """Initialize the window"""

        # Call the parent class constructor
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("./assets/69/neutral.png", SPRITE_SCALING)
        self.player_sprite.center_x = PLAYER_STARTING_LOC[0]*CELL_LENGTH + CELL_LENGTH/2
        self.player_sprite.center_y = PLAYER_STARTING_LOC[1]*CELL_LENGTH + CELL_LENGTH/2
        self.player_list.append(self.player_sprite)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()
    
    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        self.update_player_speed()

    def on_draw(self):
        """Called whenever you need to draw your window"""

        # Clear the screen and start drawing
        arcade.start_render()

        # This command has to happen before we start drawing
        self.clear()

        # horizontal lines
        for i in range(0, SCREEN_HEIGHT, CELL_LENGTH):
            arcade.draw_line(0, i, SCREEN_WIDTH, i, arcade.color.BLACK, 2)

        # vertical lines
        for i in range(0, SCREEN_WIDTH, CELL_LENGTH):
            arcade.draw_line(i, 0, i, SCREEN_HEIGHT, arcade.color.BLACK, 2)

        # Draw all the sprites.
        self.player_list.draw()

def main():
    """ Main function """
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
# Imports
import arcade
import time
from consts import *
from chars.player import Player
from chars.coat import Coat


class Game(arcade.Window):
    """Main welcome window"""
    
    def __init__(self, width, height, title):
        """Initialize the window"""

        # Call the parent class constructor
        super().__init__(width, height, title)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Set up coats info
        self.coats = []

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

        # Music
        self.bgm = None
        self.current_song_index = 0
        self.current_player = None
        self.music = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = PLAYER_STARTING_LOC[0]*CELL_LENGTH + CELL_LENGTH/2
        self.player_sprite.center_y = PLAYER_STARTING_LOC[1]*CELL_LENGTH + CELL_LENGTH/2
        self.player_sprite.cur_loc = PLAYER_STARTING_LOC
        self.player_sprite.dest_loc = PLAYER_STARTING_LOC
        self.player_list.append(self.player_sprite)

        # Set up coats
        self.coats.append(Coat('red', 1, Direction.DOWN))
        self.coats.append(Coat('brown', 4, Direction.DOWN))
        self.coats.append(Coat('red', 3, Direction.LEFT))
        self.coats.append(Coat('tan', 3, Direction.RIGHT))

        self.player_list.extend(self.coats)
        self.player_list.extend([coat.fireball for coat in self.coats])

        # List of music
        self.bgm = "./assets/music/marksmanship.wav"
        # Play the song
        self.play_song()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        if self.player_sprite.dest_loc == self.player_sprite.cur_loc:
            self.update_dest_loc()
        self.player_list.update()

        self.player_list.extend([coat.fireball for coat in self.coats if coat.new_fireball])

        # Music
        position = self.music.get_stream_position(self.current_player)

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.play_song()
    
    def update_dest_loc(self):
        # Calculate destination location based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.direction = Direction.UP
            self.player_sprite.dest_loc = (self.player_sprite.cur_loc[0], self.player_sprite.cur_loc[1] + 1)
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.direction = Direction.DOWN
            self.player_sprite.dest_loc = (self.player_sprite.cur_loc[0], self.player_sprite.cur_loc[1] - 1)
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.direction = Direction.LEFT
            self.player_sprite.dest_loc = (self.player_sprite.cur_loc[0] - 1, self.player_sprite.cur_loc[1])
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.direction = Direction.RIGHT
            self.player_sprite.dest_loc = (self.player_sprite.cur_loc[0] + 1, self.player_sprite.cur_loc[1])


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
    
    def play_song(self):
        """ Play the song. """
        self.music = arcade.Sound(self.bgm, streaming=True)
        self.current_player = self.music.play(MUSIC_VOLUME)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

def main():
    """ Main function """
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
# Imports
import arcade
import time
import random
from consts import *
from chars.player import Player
from chars.coat import Coat
from chars.madison import Madison

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

        # Set up the player info
        self.player_list = arcade.SpriteList()

        # Set up coats info
        self.coats = None

        # Set up enemy info
        self.enemy = None

        # Set up madison
        self.madison = None

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

        # Music
        self.bgm = None
        self.current_song_index = 0
        self.current_player = None
        self.music = None

        # Gacha
        self.gacha_roller = arcade.Sprite(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT /2)
        self.gacha_counter = 0
        self.helper_counter = 0
        self.gacha_start = False
        self.gacha_end = False
        self.setup_start = False

        random.seed()
        index = random.randint(1, 3)    # TODO: make rng actually work lol

        main_path = "./assets/"
        
        self.gacha_roller.textures = [arcade.load_texture(f"{main_path}big16/big16.png"),
                                    arcade.load_texture(f"{main_path}bigpistol/bigpistol.png"),
                                    arcade.load_texture(f"{main_path}gachafire/gachafire.png")]

        self.player_list.append(self.gacha_roller)
        
        self.gacha_music = arcade.Sound(f'{main_path}music/gacha roll.wav', streaming=True)
        self.gacha_player = self.gacha_music.play(volume=MUSIC_VOLUME)

        # End game
        self.end_game = False

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.coats = arcade.SpriteList()
        self.enemy = arcade.SpriteList()
        self.bullets = arcade.SpriteList()

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
        self.coats.append(Coat('red', 8, Direction.DOWN))
        self.coats.append(Coat('brown', 14, Direction.DOWN))
        self.coats.append(Coat('red', 9, Direction.LEFT))
        self.coats.append(Coat('tan', 10, Direction.RIGHT))
        self.player_list.extend(self.coats)

        # Initial fireballs
        self.player_list.extend([coat.fireball for coat in self.coats])
        self.enemy.extend([coat.fireball for coat in self.coats])

        # List of music
        self.bgm = "./assets/music/marksmanship.wav"
        # Play the song
        self.play_song()

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.end_game:
            return

        if not self.gacha_start or not self.setup_start:
            self.gacha_start = True

            if not self.gacha_end:
                self.gacha_roller.texture = self.gacha_roller.textures[self.gacha_counter % 3]

            if self.gacha_counter < 60:
                self.gacha_counter += 1
            elif self.gacha_counter < 66:
                if self.helper_counter == 5:
                    self.gacha_counter += 1
                    self.helper_counter = 0
                else:
                    self.helper_counter += 1
            elif self.gacha_counter < 75:
                if self.helper_counter == 10:
                    self.gacha_counter += 1
                    self.helper_counter = 0
                else:
                    self.helper_counter += 1
            elif self.gacha_counter == 200:
                self.gacha_roller.kill()
                self.setup_start = True
                self.setup()

                return
            else:
                self.gacha_end = True
                self.gacha_counter += 1

            return

        # check if died
        if self.player_sprite.collides_with_list(self.enemy):
            [sprite.kill() for sprite in self.player_sprite.collides_with_list(self.enemy)]
            self.player_sprite.health -= 1
            print("Your health is now", self.player_sprite.health)
        
        # Check if bullets hit coats
        for coat in self.coats:
            if coat.collides_with_list(self.bullets):
                [sprite.kill() for sprite in coat.collides_with_list(self.bullets)]
                coat.get_hit()

        # Move the player
        if self.player_sprite.dest_loc == self.player_sprite.cur_loc:
            self.update_dest_loc()
        self.player_list.update()

        # Add Madison when there are no more coats
        if len(self.coats) == 0:
            [sprite.kill() for sprite in self.player_list if sprite != self.player_sprite]

            self.coats.append(Coat('red', 1, Direction.DOWN))
            self.coats.append(Coat('brown', 14, Direction.DOWN))
            self.coats.append(Coat('red', 6, Direction.LEFT))
            self.coats.append(Coat('tan', 6, Direction.RIGHT))
            self.coats.append(Coat('red', 3, Direction.DOWN))
            self.coats.append(Coat('brown', 14, Direction.LEFT))
            self.coats.append(Coat('red', 9, Direction.LEFT))
            self.coats.append(Coat('tan', 12, Direction.RIGHT))
            self.player_list.extend(self.coats)
            self.enemy.extend(self.coats)
            
            if not self.madison:
                self.madison = Madison()
                self.player_list.append(self.madison)
                self.enemy.append(self.madison)
                self.music.stop(self.current_player)
                self.music.set_volume(0, self.current_player)
                self.current_player.delete()
                self.madison_music = arcade.Sound('./assets/music/james madison, eldritch terror.wav', streaming=True)
                self.madison_player = self.madison_music.play(MUSIC_VOLUME)
        
        if self.madison and self.madison.new_fireball:
            self.player_list.append(self.madison.fireball)
            self.enemy.append(self.madison.fireball)

        if self.madison and self.madison.collides_with_list(self.bullets):
            [bullet.kill() for bullet in self.madison.collides_with_list(self.bullets)]
            self.madison.get_hit()
            

        if self.madison and self.madison.health <= 0:
            self.madison.kill()
            self.madison_music.stop(self.current_player)
            self.madison_music.set_volume(0, self.current_player)
            self.madison_player.delete()
            self.m16_music = arcade.Sound('./assets/music/M-16 March.wav', streaming=True)
            self.m16_player = self.m16_music.play(MUSIC_VOLUME)

            for sprite in self.player_list:
                sprite.kill()

            self.player_list.append(Player())

            self.end_game = True

            return

        # Add new sprites if necessary
        self.player_list.extend([coat.fireball for coat in self.coats if coat.new_fireball])
        self.enemy.extend([coat.fireball for coat in self.coats if coat.new_fireball])
        for bullet in self.player_sprite.bullets:
            if bullet not in self.player_list:
                self.player_list.append(bullet)
            if bullet not in self.bullets:
                self.bullets.append(bullet)

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
        elif key == arcade.key.SPACE:
            self.player_sprite.shoot()
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
        # for i in range(0, SCREEN_HEIGHT, CELL_LENGTH):
        #     arcade.draw_line(0, i, SCREEN_WIDTH, i, arcade.color.BLACK, 2)

        # # vertical lines
        # for i in range(0, SCREEN_WIDTH, CELL_LENGTH):
        #     arcade.draw_line(i, 0, i, SCREEN_HEIGHT, arcade.color.BLACK, 2)

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
    arcade.run()

if __name__ == "__main__":
    main()
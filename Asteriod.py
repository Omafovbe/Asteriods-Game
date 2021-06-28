"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

'''
Additional Global Variables to 
get the asteriods to randomly begin from
offscreen
'''
OFFSCREEN_SPACE = 200
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE

# point class to position objects on the screen
class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

# velocity class to move the objects on the screen at a steady speed    
class Velocity:
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

# Moving Objects parent class to define certain methods and        
class MovingObject:
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx

    # method to ensure objects move through the screen from left to right and top to bottom
    def update(self):
        if self.center.x < 0:
            self.center.x = SCREEN_WIDTH

        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0

        if self.center.y < 0:
            self.center.y = SCREEN_HEIGHT

        if self.center.y > SCREEN_HEIGHT:
            self.center.y = 0

    # method to determine if objects are off screen or not (Boolean)  
    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        is_off_screen = False

        if self.center.x > SCREEN_WIDTH or self.center.x < 0:
            is_off_screen = True

        elif self.center.y > SCREEN_HEIGHT or self.center.y < 0:
            is_off_screen = True

        return is_off_screen

class Bullet(MovingObject):
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.img = "images/laserblue01.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self._size = 0
        self._angle = 0
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = value
        
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value
        
    
    def fire(self, angle, point):
        # Get the ship's position and angle
        # So as to position the bullet
        
        self.center.x = point.x
        self.center.y = point.y
        self.angle = angle
        
        # Set the velocity of the bullet
        self.velocity.dx = -math.sin(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.cos(math.radians(angle)) * BULLET_SPEED
    
"""
The Asteriod Class
++++++++++++++++++++
Inherits the movingObject class

:param: Rock size
    1 - Small Asteriod
    2 - Medium
    3 - Big
"""
class Asteriod(MovingObject):
    def __init__(self, rock_size):
        super().__init__()
        self.img = ""
        self.texture = 0
        self.width = 0.0
        self.height = 0.0
        self.alpha = 255
        self.size = rock_size
        self.radius = rock_size
        self.velocity.dx = random.random() * BIG_ROCK_SPEED
        self.velocity.dy = random.random() * BIG_ROCK_SPEED
        self.angle = math.degrees(math.atan2(self.velocity.dy, self.velocity.dx))
            
    '''
    Loads the appropriate meteors (Big, medium or small)
    To be drawn on the screen and gets the width and height
    '''
    def load_asteriod(self):
        if self.size == 3:
            self.img = "images/meteorGrey_big1.png"
        elif self.size == 2:
            self.img = "images/meteorGrey_med1.png"
        elif self.size == 1:
            self.img = "images/meteorGrey_small1.png"
        
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)

    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value == 3:
            self._radius = BIG_ROCK_RADIUS
        elif value == 2:
            self._radius = MEDIUM_ROCK_RADIUS
        elif value == 1:
            self._radius = SMALL_ROCK_RADIUS
    
    # change angle so as to spin the rock
    def change_angle(self):
        if self.size == 3:
            self.angle += BIG_ROCK_SPIN
        elif self.size == 2:
            self.angle += MEDIUM_ROCK_SPIN
        elif self.size == 1:
            self.angle += SMALL_ROCK_SPIN
            
    def hit(self):
        self.alive = False
        return 1
        


class Ship(MovingObject):
    def __init__(self):
        super().__init__()
        self.img = "images/playerShip1_orange.png"
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.speed = 0
        self.respawning = 0
        self.alpha = 0
        self.radius = SHIP_RADIUS
        self.respawn()
        
    def respawn(self):
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2
        self.angle = 0
        self.respawning = 1
        
    # Draw the ship on the center of screen      
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, self.alpha)
    
    def updateShip(self):
        if self.respawning > 0:
            for i in range(1, 300, 10):
                self.respawning += i
                self.alpha = self.respawning
                if self.respawning > 250:
                    self.respawning = 0
                    self.alpha = 255
                break
                 
        self.advance()
    # move the ship forward
    def move(self, thrust):
        
        # increase the acceleration of the ship
        if thrust == 0:
            self.speed = 0
            
        else:
            self.speed += thrust
                   
        self.velocity.dx = -math.sin(math.radians(self.angle)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.angle)) * self.speed

        #print(self.speed)
        self.advance()

    # Steer the ship to the right by reducing the angle
    def turn_right(self):
        self.angle -= SHIP_TURN_AMOUNT

    # steer the ship to the left by increasing the angle
    def turn_left(self):
        self.angle += SHIP_TURN_AMOUNT
        
 



class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        self.score = 0

        # Declare anything here you need the game class to track
        self.asteriods = []
        self.ship = Ship()
        self.bullets = []
        self.lives = 5
        self.frame_count = 0
        self.game_over = False

        # Sounds
        self.laser_sound = arcade.load_sound("sounds/laser2.wav")
        self.hit_sound1 = arcade.load_sound("sounds/hit1.wav")
        self.hit_sound2 = arcade.load_sound("sounds/hit2.wav")
        self.hit_sound3 = arcade.load_sound("sounds/hit3.wav")
        self.game_over_sound = arcade.load_sound("sounds/gameover5.wav")
        
        # loads 5 big meteors to the asteriod list
        for i in range(INITIAL_ROCK_COUNT):
            # Load large rocks
            rock = Asteriod(3)
            rock.load_asteriod()

            rock.center.y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            rock.center.x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)
               
            self.asteriods.append(rock)
        
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        for asteriod in self.asteriods:
            asteriod.draw()
            
        for bullet in self.bullets:
            bullet.draw()
            
                    
        self.ship.draw()
        self.draw_score()
        
    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

        # Draw the number of lives left for player
        if self.lives > 0:
            lives_text = "Lives: {}".format(self.lives)
        else:
            lives_text = "Lives: Game Over"
        
        arcade.draw_text(lives_text, start_x=start_x, start_y=start_y-20, font_size=12, color=arcade.color.WHITE)


    def on_update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        

        if not self.game_over:
            
            self.check_keys()
            self.ship.updateShip()
            
            
            
                    
            # Fire(Move) the bullets
            for fire in self.bullets:
                fire.advance()
                self.frame_count += 1
                # print(self.frame_count)

                # Remove bullets after 60 frames
                if self.frame_count > 60:
                    self.bullets.remove(fire)
                    self.frame_count = 0

            # Check for collisions
            self.check_collisions()

            # Tell everything to advance or move forward one step in time
                
            for asteriod in self.asteriods:
                asteriod.advance()
                asteriod.change_angle()

            self.check_off_screen()


    def check_off_screen(self):
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                bullet.update()
                # self.bullets.remove(bullet)
                
        for asteriod in self.asteriods:
            if asteriod.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                asteriod.update()

        if self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            self.ship.update()
        
    def check_collisions(self):
        """
        Checks to see if bullets have hit an asteriod.
        Updates scores and removes debris.
        :return:
        """
        for bullet in self.bullets:
            for asteriod in self.asteriods:
                
                if bullet.alive and asteriod.alive:
                    too_close = bullet.radius + asteriod.radius
                    #print(asteriod.radius)
                    
                    if (abs(bullet.center.x - asteriod.center.x) < too_close and
                                abs(bullet.center.y - asteriod.center.y) < too_close):
                        
                        # its a hit!
                        bullet.alive = False
                        
                        # TODO: Split the asteriod into smaller pieces
                        self.split_asteriod(asteriod)
                        self.score += asteriod.hit()
                        
        
        # Shipwreaked
        if self.ship.respawning == 0:
            # We still have more ship/player live
            if self.lives > 0:
                for asteriod in self.asteriods:
                    if asteriod.alive:
                        ship_wreck = asteriod.radius + self.ship.radius

                        if (abs(asteriod.center.x - self.ship.center.x) < ship_wreck and 
                                    abs(asteriod.center.y - self.ship.center.y) < ship_wreck):
                            
                            self.ship.respawn()
                            self.split_asteriod(asteriod)
                            asteriod.hit()
                            self.lives -= 1
                            self.hit_sound3.play()
            # No more ship/player lives
            else:
                self.ship.alive = False
                self.game_over = True
                self.game_over_sound.play()
        # Clear off the meteors from the screen
        self.clear_debris()
    
    '''
    Split asteriod method
    
    splits the asteriod into 3 smaller meteors as the case maybe when hit
    by the laser
    
    :param: asteriod

    '''
    def split_asteriod(self, asteriod):
        point_x = asteriod.center.x
        point_y = asteriod.center.y
        
        if asteriod.size == 3:
            for i in range(3):
                if i == 0:
                    rock = Asteriod(1)
                else:
                    rock = Asteriod(2)
                rock.load_asteriod()
                rock.center.x = point_x
                rock.center.y = point_y
                
                self.asteriods.append(rock)
                self.hit_sound1.play()
                
        elif asteriod.size == 2:
            for i in range(3):
                rock = Asteriod(1)
                rock.load_asteriod()
                rock.center.x = point_x
                rock.center.y = point_y
                
                self.asteriods.append(rock)
                self.hit_sound2.play()
        
    # remove destroyed ship, laser and dead meteors from the screen
    def clear_debris(self):
        
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
                
        for asteriod in self.asteriods:
            if not asteriod.alive:
                self.asteriods.remove(asteriod)
        
        # if not self.ship.alive:
        #     self.ship.respawn()
    
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn_right()

        if arcade.key.UP in self.held_keys:
            self.ship.move(SHIP_THRUST_AMOUNT)

        if arcade.key.DOWN in self.held_keys:
            self.ship.move(-SHIP_THRUST_AMOUNT)

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # Fire the bullet here!
                
                bullet = Bullet()
                bullet.fire(self.ship.angle, self.ship.center)
                
                self.bullets.append(bullet)
                arcade.play_sound(self.laser_sound)

            if key == arcade.key.RIGHT:
                self.ship.turn_right()

            if key == arcade.key.LEFT:
                self.ship.turn_left()

            if key == arcade.key.UP:
                self.ship.move(SHIP_THRUST_AMOUNT)

            if key == arcade.key.DOWN:
                self.ship.move(-SHIP_THRUST_AMOUNT)
                        

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
                        
        if key in self.held_keys:
            self.ship.move(0)
            self.held_keys.remove(key)
            
                    



# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
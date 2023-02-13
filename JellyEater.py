
"""This a game called Jelly Eater. Player moves the mouse to move the croc to eat
the jellyfish appearing randomly on screen. Player scores 5 points for each jelly eaten.
Game over if more than 10 jellyfish appear on the screen.

I need an opening screen explaining game play and scoring
I would like a button to play again
Images and sounds from opengameart.org"""

# Import and initialize pygame
import pygame

# path for assets
from pathlib import Path

from typing import Tuple

# Width / height window (pixels)
WIDTH = 800
HEIGHT = 600

# How quickly will the jellyfish appear? Time is in milliseconds
jelly_countdown = 1000
jelly_interval = 100

# To randomize jelly placement
from random import randint

# Maximum amount of jellyfish on screen before game terminated?
JELLY_COUNT = 10
# load pygame mixer for sounds and music
pygame.mixer.init()
# Load and play background music
pygame.mixer.music.load("Adventure Music!.mp3")
pygame.mixer.music.play(loops=-1)

# Define Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() #Initialise player sprite

        # player image - png downloaded from opengameart.org
        player_image = ("croc.png")
        # image load, alpha channel used to key transparent background 
        self.surf = pygame.image.load(player_image).convert_alpha()
        # Save Player rect so you can move it around the window
        self.rect = self.surf.get_rect()

    def update(self, pos: Tuple): #updates position of player with mouse movements
        self.rect.center = pos

# Define the jellyfish sprite
class Jelly(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the jelly sprite"""
        super(Jelly, self).__init__()

        # Get the image to draw the Jellyfish
        jelly_image = ("jellyfish-large1.png")

        # Load the image, preserve alpha channel for transparency
        self.surf = pygame.image.load(jelly_image).convert_alpha()

        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                randint(10, WIDTH - 10),
                randint(10, HEIGHT - 10),
            )
        )

# Initialize the Pygame engine
pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])
pygame.display.set_caption("Jelly Eater: Move your croc with the mouse to get 5 points per jellyfish eaten. 10 Jellies onscreen means game over.")
# initialise pygame clock
clock = pygame.time.Clock()

# Create custom event for adding new jelly
ADDJELLY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDJELLY, jelly_countdown)

# Set up the jelly_list
jelly_list = pygame.sprite.Group()

# Initialize the score
score = 0

# Set up the croc eating jellfish pickup sound
jelly_pickup_sound = pygame.mixer.Sound("snap.wav")

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# Create player sprite (croc) and set its starting position
player = Player()
player.update(pygame.mouse.get_pos())

# Run until you get to an end condition
running = True
while running:

    # if window close button clicked...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # To add a new jelly
        elif event.type == ADDJELLY:
            # Create  new jelly and add to the jelly_list
            new_jelly = Jelly()
            jelly_list.add(new_jelly)

            # increase jelly instance appearance if less than three jellfish are on-screen: improves gameplay
            if len(jelly_list) < 3:
                jelly_countdown -= jelly_interval
            # Set the interval
            if jelly_countdown < 100:
                jelly_countdown = 100

            # Stop the previous timer by setting the interval to 0
            pygame.time.set_timer(ADDJELLY, 0)

            # Start a new timer
            pygame.time.set_timer(ADDJELLY, jelly_countdown)

    # Update the player position
    player.update(pygame.mouse.get_pos())

    # Check if the player has collided with a jelly, remove jelly from window if True
    jellys_collected = pygame.sprite.spritecollide(
        sprite=player, group=jelly_list, dokill=True
    )
    for jelly in jellys_collected:
        # Each jelly is worth 5 points
        score += 5
        # Play the jelly eaten pickup sound
        jelly_pickup_sound.play()

    # If too many jellfish amass on the screen this will end the game loop
    if len(jelly_list) >= JELLY_COUNT:
        running = False

    # To render the screen, fill the background with blue (RGB values)
    screen.fill((101, 159, 165))

    # Draw the jellyfish next
    for jelly in jelly_list:
        screen.blit(jelly.surf, jelly.rect)

    # Then draw the player
    screen.blit(player.surf, player.rect)

    # Finally, draw the score at the bottom left
    score_font = pygame.font.SysFont("any_font", 36)
    score_block = score_font.render(f"Score: {score}", False, (246, 234, 0))
    screen.blit(score_block, (50, HEIGHT - 50))

    # Use flip to make everything appear in window
    pygame.display.flip()

    # Keeps 30 frames per second framerate
    clock.tick(30)

# Print  final score
print(f"Game over! Final score: {score}")
# I want a screen for game over final score
# Make the mouse visible again
pygame.mouse.set_visible(True)
# stop and quit pygame mixer
pygame.mixer.music.stop()
pygame.mixer.quit()

#Quit the game
#pygame.quit()

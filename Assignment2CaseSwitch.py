####
# STUDENT NAME: Kathleen Johnston and Huang YU
# STUDENT NUMBER: 981492
####

userchoice = 1
userchoice = input("Please enter 1 to run Car Race Game, 2 to run Jelly Eater Game: ", )
while userchoice != 0:

    if int(userchoice) == 1:
        
        import pygame
        import os
        import random
        import pygame
        from sys import exit
        from pygame.locals import *

        #initialize Pygame
        pygame.init()

        #count the score
        def display_score():
            current_time = int((pygame.time.get_ticks()-start_time)/1000)
            score_surf = test_font.render("Score:{}".format(current_time),False,'Black')
            score_rect = score_surf.get_rect(center = (400,30))
            screen.blit(score_surf,score_rect)
            return current_time 

        def set_Obstacle(Obstacle_list):
            if Obstacle_list: 
                for car_rect in Obstacle_list:
                    if car_rect.x >= -100:
                        n = random.randint(200,500)
                        if car_rect.x > n:
                            car_rect.x -= 4
                            car_rect.y -= 1
                        elif car_rect.x <= n:
                            car_rect.x -= 4
                            car_rect.y += 1
                        screen.blit(redcar_surf,car_rect)
                    else: Obstacle_list.remove(car_rect)

                return(Obstacle_list)
            return[]
                
        #set the screen size
        screen = pygame.display.set_mode([800,400])

        #set the clock
        clock = pygame.time.Clock()
        start_time = 0
        score = 0

        # change the relative directory
        base_path = os.path.dirname(__file__)
        test_font = pygame.font.Font(os.path.join(base_path,'font/pixeltype/Pixeltype.ttf'),50)

        #load the image
        bg_surf = pygame.image.load(os.path.join(base_path, 'Graphic/road.png')).convert()
        bg_rect = bg_surf.get_rect(center = (400,200))
        redcar_surf = pygame.image.load(os.path.join(base_path,'Graphic/redcar.png')).convert_alpha()
        bluecar_surf = pygame.image.load(os.path.join(base_path,'Graphic/bluecar.png')).convert_alpha()

        player_surf = pygame.image.load(os.path.join(base_path,'Graphic/yellowcar.png')).convert_alpha()
        player_rect = player_surf.get_rect(midbottom =(80,365))
        player_direction = 0

        #intro screen
        intro_car = pygame.image.load(os.path.join(base_path,'Graphic/yellowcar.png'))
        intro_car = pygame.transform.rotozoom(intro_car,45,2)
        intro_car_rect = intro_car.get_rect(center = (400,170))

        game_name = test_font.render('My Car Race: use arrow keys to move the yellow car', False,'#420D09')
        game_name_rect = game_name.get_rect(center = (400,50))

        game_message = test_font.render("PRESS SPACE TO RESTART THE GAME",False,"#420D09")
        game_message_rect = game_message.get_rect(midbottom =(400,350))
        # Load the sound file
        sound = pygame.mixer.Sound(os.path.join(base_path,'audio/bg.mp3'))

        # Set the volume of the sound
        sound.set_volume(0.1)

        # Create a custome event, Schedule the event to be triggered every 1 seconds
        Obstacle_event = USEREVENT + 1
        pygame.time.set_timer(Obstacle_event,1500)

        Obstacle_list = []

        #main game loop
        running = True
        game_active = False
        bg_speed = 2
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sound.stop()
                    pygame.quit()
                    exit()
                
                if game_active:
                    # Play the sound in a loop
                    sound.play(-1)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            player_direction = -2
                        elif event.key == pygame.K_DOWN:
                            player_direction = 2
                    if event.type == Obstacle_event:
                        Obstacle_list.append(redcar_surf.get_rect(midbottom =(random.randint(900,1100),random.randint(200,365))))
                        Obstacle_list.append(bluecar_surf.get_rect(midbottom =(random.randint(900,1100),random.randint(50,300))))
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        running = True
                        game_active = True
                        start_time = pygame.time.get_ticks()
            if game_active:
                # Move the background
                bg_rect.x -= bg_speed
                if bg_rect.x <= -800:
                    bg_rect.x = 0
                screen.blit(bg_surf,bg_rect)
                
                # Display score
                display_score()
                
                # Set obstacle car
                set_Obstacle(Obstacle_list)
                
                # Move the player car
                player_rect.y += player_direction
                screen.blit(player_surf,player_rect)
                # Collision
                for car_rect in Obstacle_list:
                    if car_rect.colliderect(player_rect) or player_rect.y < 0 or player_rect.y > 380 :
                        score = display_score()
                        game_active = False
                        sound.stop()
                        Obstacle_list=[]
                        player_rect = player_surf.get_rect(midbottom =(80,165))
            else:
                # Game pause and display information
                screen.fill("#EEDC82")
                screen.blit(intro_car,intro_car_rect)
                screen.blit(game_name,game_name_rect)
                if score == 0:
                    screen.blit(game_message,game_message_rect)
                else:
                    score_message = test_font.render("Score:{}".format(score),False,'#420D09')
                    score_message_rect=score_message.get_rect(center=(400,350))
                    screen.blit(score_message,score_message_rect)
            pygame.display.update()
            clock.tick(70)   
            
        pygame.QUIT()

    elif int(userchoice) == 2:
            
        """This a game called Jelly Eater. Player moves the mouse to move the crocodile to eat
        the jellyfish appearing randomly on screen. Player scores 5 points for each jelly eaten.
        Game over if more than 10 jellyfish appear on the screen.

        Images and sounds from opengameart.org"""

        # Import and initialize pygame
        import pygame
        import pygame.freetype
        import pygame.draw
        from pygame.sprite import Sprite
        from pygame.rect import Rect

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
        pygame.display.set_caption("Jelly Eater: Move your croc with the mouse to get 5 points per jellyfish eaten. 10 Jellies onscreen means game over")

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

        # Draw the final score at the bottom right
        final_score_font = pygame.font.SysFont("any_font", 36)
        final_score_block = final_score_font.render(f"Final Score: {score}", False, (246, 234, 0))
        screen.blit(final_score_block, (350, HEIGHT - 50))
        # Use flip to make everything appear in window
        pygame.display.flip()

        pygame.display.update()
        clock.tick(70)


        # Make the mouse visible again
        pygame.mouse.set_visible(True)
        # stop and quit pygame mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        #Quit the game
        pygame.QUIT()

        





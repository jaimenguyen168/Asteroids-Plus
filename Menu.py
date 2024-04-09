import pygame
from AsteroidsRound import *
from shipSelectScreen import *
from button import *

class Menu:
    def __init__(self):
        pygame.init()
        # load screen and images for background
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))
        self.shipicon = pygame.image.load('Images/ships/ship-a/ship-a-damaged.png')
        
        # init vars for background movement
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH
        # init clock for FPS
        self.clock = pygame.time.Clock()

        self.running = True
        self.playButton = Button((WIN_WIDTH/2 - 50, WIN_HEIGHT/2 - 150), (100, 100), WHITE, "PLAY")
        self.shipSelect = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2), (100, 100), WHITE, "SHIP", 'Images/ships/ship-a/ship-a-damaged.png')
        self.exitButton = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2 + 150), (100, 100), WHITE, "EXIT")
        
        
    def scoreBoard():
        # load the previous score if it exists
        try:
            with open('score.dat', 'rb') as file:
                score = pickle.load(file)
        except:
            score = 0

        print "High score: %d" % score

        # your game code goes here
        # let's say the user scores a new high-score of 10
        score = 10;

        # save the score
        with open('score.dat', 'wb') as file:
            pickle.dump(score, file)
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
       
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)
        
        self.playButton.draw(self.screen, BLACK)
        self.shipSelect.draw(self.screen, BLACK)
        self.exitButton.draw(self.screen, BLACK)
    
        pygame.display.update()

    def update_background(self):
        # Move backgrounds to the left
        self.bg_stars_x1 -= 1  # Adjust speed as necessary
        self.bg_stars_x2 -= 1
        
        # If the first image is completely off-screen
        if self.bg_stars_x1 + WIN_WIDTH < 0:
            self.bg_stars_x1 = WIN_WIDTH
            
        # If the second image is completely off-screen
        if self.bg_stars_x2 + WIN_WIDTH < 0:
            self.bg_stars_x2 = WIN_WIDTH

    def play(self):
        selected_ship = 0
        while True:
            m.draw()
            m.update_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                if self.playButton.is_clicked(event):
                        g = Game(selected_ship) #init Game class
                        g.new() #create a new game everytime we run
                        while g.running:
                            g.main()
                if self.shipSelect.is_clicked(event):
                    select = ShipSelection()
                    selected_ship = select.main()
                    while select.running:
                        select.main()

                if self.exitButton.is_clicked(event):
                    # exit
                    pygame.quit()
                    exit()
        
        
m = Menu()
while m.running:
    m.play()

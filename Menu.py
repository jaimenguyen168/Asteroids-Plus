import pygame
from AsteroidsRound import *
from shipSelectScreen import *
from button import *
from leaderboard import *
from instructions import *
from CoOp import *
import pygame.font

class Menu:
    def __init__(self):
        pygame.init()
        self.title = "Asteroids   Plus"
        self.title_font = pygame.font.Font('Galaxus-z8Mow.ttf', 100)
        self.title_text = self.title_font.render(self.title, True, WHITE)
        self.title_y = 150
        self.title_y_velocity = 0.20
        # load screen and images for background
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
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

    def resize_window(self, new_width, new_height):
        """Update global dimensions and rescale elements."""
        global WIN_WIDTH, WIN_HEIGHT
        min_size = 800
        new_width = max(new_width, min_size)
        new_height = max(new_height, min_size)
        WIN_WIDTH, WIN_HEIGHT = new_width, new_height

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)

        # Rescale the images
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        self.bg_stars = pygame.transform.scale(self.bg_stars, (WIN_WIDTH, WIN_HEIGHT))

        # Update button positions dynamically based on new size
        self.draw() 

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        
        self.title_y = int(WIN_HEIGHT * 0.2)  # Fixed position above the buttons

        # Add the following lines
        title_rect = self.title_text.get_rect(center=(WIN_WIDTH/2, self.title_y)) 
        self.screen.blit(self.title_text, title_rect)

        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)

        self.playButton = Button((int(WIN_WIDTH * 0.45), int(WIN_HEIGHT * 0.3)), (int(WIN_WIDTH * 0.12), int(WIN_HEIGHT * 0.1)), WHITE, "PLAY")
        self.shipSelect = Button((int(WIN_WIDTH * 0.45), int(WIN_HEIGHT * 0.42)), (int(WIN_WIDTH * 0.12), int(WIN_HEIGHT * 0.1)), WHITE, "SHIP", 'Images/ships/ship-a/ship-a-damaged.png')
        self.exitButton = Button((int(WIN_WIDTH * 0.45),int(WIN_HEIGHT * 0.54)), (int(WIN_WIDTH * 0.12), int(WIN_HEIGHT * 0.1)), WHITE, "EXIT")
        self.statButton = Button((int(WIN_WIDTH * 0.45), int(WIN_HEIGHT * 0.66)), (int(WIN_WIDTH * 0.12), int(WIN_HEIGHT * 0.1)), WHITE, "STATS")
        self.instructionsButton = Button((int(WIN_WIDTH * 0.8), int(WIN_HEIGHT * 0.78)), (int(WIN_WIDTH * 0.12), int(WIN_HEIGHT * 0.1)), WHITE, "Help")
        self.coOpButton = Button((int(WIN_WIDTH * 0.45), int(WIN_HEIGHT * 0.78)), (int(WIN_WIDTH * 0.12), int(WIN_HEIGHT * 0.1)), WHITE, "CO-OP")
        
        self.playButton.draw(self.screen, BLACK)
        self.shipSelect.draw(self.screen, BLACK)
        self.exitButton.draw(self.screen, BLACK)
        self.statButton.draw(self.screen,BLACK)
        self.instructionsButton.draw(self.screen,BLACK)
        self.coOpButton.draw(self.screen,BLACK)
    
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
    
    def show_instructions(self):
        inst_menu = InstructionsMenu(self.screen)
        inst_menu.run()

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
                elif event.type == pygame.VIDEORESIZE:
                    self.resize_window(event.w, event.h)

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

                if self.instructionsButton.is_clicked(event):
                    self.show_instructions()

                if self.statButton.is_clicked(event):
                    # exit
                    leaderboard = LeaderBoard()
                    while leaderboard.running:
                        leaderboard.view()
                        
                if self.coOpButton.is_clicked(event):
                        c = CoOp(selected_ship) #init Game class
                        c.new() #create a new game everytime we run
                        while c.running:
                            c.main()

                if self.exitButton.is_clicked(event):
                    # exit
                    pygame.quit()
                    exit()
        
        
m = Menu()
while m.running:
    m.play()

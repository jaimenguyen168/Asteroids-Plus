import pygame
from AsteroidsRound import *
from shipSelectScreen import *
from button import *
from leaderboard import *
from instructions import *
from CoOp import *
import pygame.font
from news import *;

class Menu:

    def __init__(self):
        pygame.init()
        self.title = "Asteroids   Plus"
        self.title_font = pygame.font.Font('Galaxus-z8Mow.ttf', 100)
        self.title_text = self.title_font.render(self.title, True, WHITE)
        self.title_y = 150
        self.title_y_velocity = 0.20
        # load screen and images for background
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))

        # add background and change background index --Jie
        '''
        self.backgrounds = [
            self.background,
            pygame.transform.scale(pygame.image.load('Images/backgrounds/background1.jpg').convert_alpha(), (WIN_WIDTH, WIN_HEIGHT)),
            pygame.transform.scale(pygame.image.load('Images/backgrounds/background2.jpg').convert_alpha(), (WIN_WIDTH, WIN_HEIGHT)),
            pygame.transform.scale(pygame.image.load('Images/backgrounds/background3.jpg').convert_alpha(), (WIN_WIDTH, WIN_HEIGHT))
        ]
        self.current_background_index = 0
        '''

        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))
        self.shipicon = pygame.image.load('Images/ships/ship-a/ship-a-damaged.png')
        
        # init vars for background movement
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH
        # init clock for FPS
        self.clock = pygame.time.Clock()

        self.running = True
        self.playButton = Button((WIN_WIDTH/2 - 130, WIN_HEIGHT/2 - 150), (100, 100), WHITE, "PLAY")
        self.shipSelect = Button((WIN_WIDTH/2 -130, WIN_HEIGHT/2), (100, 100), WHITE, "SHIP", 'Images/ships/ship-a/ship-a-damaged.png')
        self.exitButton = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2 + 150), (100, 100), WHITE, "EXIT")
        self.statButton = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2 + 300), (100, 100), WHITE, "STATS")
        self.newsButton = Button((WIN_WIDTH/2 +20, WIN_HEIGHT/2), (100, 100), WHITE, "NEWS")
        self.instructionsButton = Button((WIN_WIDTH - 120, WIN_HEIGHT - 70), (100, 50), WHITE, "Help")
        self.coOpButton = Button((WIN_WIDTH/2 + 20, WIN_HEIGHT/2 - 150), (100, 100), WHITE, "CO-OP")

        # add the change background button --Jie
        '''
        self.change_bg_button = Button((WIN_WIDTH/2 -180, WIN_HEIGHT/2 - 150), (100, 100), WHITE, 'Theme')
        '''
        
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        
        self.title_y += self.title_y_velocity
        if self.title_y >= WIN_HEIGHT - 635:
            self.title_y = WIN_HEIGHT - 635  # Limit the title's position to the bottom of the screen
            self.title_y_velocity = -0.20  # Reverse direction when reaching bottom
        elif self.title_y <= 150:
            self.title_y = 150  # Limit the title's position to the top of the screen
            self.title_y_velocity = 0.20 

        # Add the following lines
        title_rect = self.title_text.get_rect(center=(WIN_WIDTH/2, self.title_y)) 
        self.screen.blit(self.title_text, title_rect)

        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)
        
        self.playButton.draw(self.screen, (128,128,128))
        self.shipSelect.draw(self.screen, (128,128,128))
        self.exitButton.draw(self.screen, (128,128,128))
        self.statButton.draw(self.screen, (128,128,128))
        self.newsButton.draw(self.screen, (128,128,128))
        self.instructionsButton.draw(self.screen, (128,128,128))
        self.coOpButton.draw(self.screen, (128,128,128))

        # add the change background button --Jie
        '''
        self.change_bg_button.draw(self.screen,BLACK)
        '''
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
        
    def show_news(self):
        news_menu = NewsMenu(self.screen)
        news_menu.run()

    # change background by change background index --Jie
    '''
    def change_background(self):
        self.current_background_index = (self.current_background_index + 1) % len(self.backgrounds)
        self.background = self.backgrounds[self.current_background_index]
    '''

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
                
                if self.newsButton.is_clicked(event):
                    self.show_news()
                
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

                # click change background button to change the background --Jie
                '''
                if self.change_bg_button.is_clicked(event):
                    self.change_background()
                '''


m = Menu()
while m.running:
    m.play()

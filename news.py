import pygame
from button import *
import pygame.font
import config
from datetime import datetime, timedelta
import requests

class NewsMenu:

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        # Semi-transparent background for submenu
        self.submenu_bg = pygame.Surface((500, 600))  # Smaller than the full screen
        self.submenu_bg.fill((50, 50, 50))  # Dark grey background
        self.submenu_bg.set_alpha(180)  # Semi-transparent
        self.submenu_rect = self.submenu_bg.get_rect(center=(config.WIN_WIDTH // 2, config.WIN_HEIGHT // 2))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 24)

        # init vars for background movement
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = config.WIN_WIDTH

        # Semi-transparent background for submenu
        self.message_box = pygame.Surface((340, 500))  # Smaller width, enough for text
        self.message_box.fill((50, 50, 50))  # Dark grey background
        self.message_box.set_alpha(180)  # Semi-transparent
        self.message_box_rect = self.message_box.get_rect(topright=(config.WIN_WIDTH - 50, 100))
        self.current_message = None  # Store the current message to display

        # Define buttons
        button_y_start = 100  # Starting y-position of the return button
        self.exitButton = Button((100, button_y_start + 360), (200, 50), WHITE, 'Return')

        # Initial visibility of other buttons is False
        self.initial_buttons_visible = True
        self.self_button_visible = False
        self.control_visible = False
        
        self.news_cache = None
        self.last_fetch_time = None
        self.cache_duration = timedelta(minutes=15)  # Cache news for 15 minutes
        
    def run(self):
        while self.running:
            if not self.is_cache_valid():
                self.fetch_news()  # Fetch news when the menu is opened
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exitButton.is_clicked(event):
                        self.running = False
                            
            self.update_background()
            self.screen.fill((0, 0, 0))  # Clear the screen or fill with base color
            self.screen.blit(self.bg_stars, (self.bg_stars_x1, 0))
            self.screen.blit(self.bg_stars, (self.bg_stars_x2, 0))

            self.draw_transparent_overlay()  # Draw the transparent overlay

            if self.news_cache:
                self.display_message(self.news_cache)
            else:
                self.display_message(["No news available"])
                
            # Control visibility of each button group
            if self.initial_buttons_visible:
                self.exitButton.draw(self.screen, (128,128,128))
                
            pygame.display.update()

    def update_background(self):
        self.bg_stars_x1 -= 1  # Adjust speed as necessary
        self.bg_stars_x2 -= 1
        
        # Reset positions to loop the background
        if self.bg_stars_x1 + config.WIN_WIDTH < 0:
            self.bg_stars_x1 = config.WIN_WIDTH
            
        if self.bg_stars_x2 + config.WIN_WIDTH < 0:
            self.bg_stars_x2 = config.WIN_WIDTH 
            
    def fetch_news(self):
        params = {
            'q': '"Temple Owls" OR "Temple Football"',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': API_KEY
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status() 
            
            data = response.json()
 #           print(f"API Response: {data}")

            if data['status'] == 'ok' and 'articles' in data and data['articles']:
                self.news_cache = [f"{article['title']}" for article in data['articles'][:2]]
                self.last_fetch_time = datetime.now()
#                print(f"Fetched news: {self.news_cache}")
            else:
                print("No articles found in the API response")
                self.news_cache = ["No articles found about Temple University"]

        except requests.RequestException as e:
            print(f"Error fetching news: {str(e)}")
            self.news_cache = ["Error fetching news"]

    def is_cache_valid(self):
        if self.news_cache is None or self.last_fetch_time is None:
            return False
        return datetime.now() - self.last_fetch_time < self.cache_duration
            
    def display_message(self, articles):
        max_width = self.message_box_rect.width - 20
        line_spacing = 5
        y_offset = 20
        max_lines_per_article = 6

        self.message_box.fill((50, 50, 50))
        self.message_box.set_alpha(180)

        for article in articles:
            words = article.split()
            current_line = ""
            line_count = 0
            for word in words:
                test_line = current_line + word + ' '
                if self.font.size(test_line)[0] < max_width:
                    current_line = test_line
                else:
                    text_surface = self.font.render(current_line, True, (255, 255, 255))
                    self.message_box.blit(text_surface, (10, y_offset))
                    y_offset += text_surface.get_height() + line_spacing
                    current_line = word + ' '
                    line_count += 1
                    
                    if line_count >= max_lines_per_article:
                        ellipsis_surface = self.font.render("...", True, (255, 255, 255))
                        self.message_box.blit(ellipsis_surface, (10, y_offset))
                        y_offset += ellipsis_surface.get_height() + line_spacing
                        break
            
            if current_line and line_count < max_lines_per_article:
                text_surface = self.font.render(current_line, True, (255, 255, 255))
                self.message_box.blit(text_surface, (10, y_offset))
                y_offset += text_surface.get_height() + line_spacing
            
            y_offset += 20  # Add space between articles

        self.screen.blit(self.message_box, self.message_box_rect)

    def draw_transparent_overlay(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
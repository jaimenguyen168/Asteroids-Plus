import math
import pygame
import random
from config import *
import sys

class Powerups(pygame.sprite.Sprite):

    # create the powerups
    def __init__(self, all_sprites, player):
        super().__init__()
        self.all_sprites = all_sprites
        self.player = player
        self.collision = False

        #load all powerup images and random chooses one
        image_paths = ['Images/powerups/shield.png', 'Images/powerups/plus.png', 'Images/powerups/bomb.png']
        self.images = [pygame.image.load(path) for path in image_paths]
        self.image_size = (40, 40)  # Change the size as needed
        self.images = [pygame.transform.scale(image, self.image_size) for image in self.images]
        self.image = random.choice(self.images)  # Randomly choose one image
        self.rect = self.image.get_rect()
        self.rand_placement()

    def rand_placement(self):
        self.rect.x = random.randint(0, WIN_WIDTH)
        self.rect.y = random.randint(0, WIN_HEIGHT)

    def shield_funct(self):
        current_time = pygame.time.get_ticks()
        self.player.damage_loop = current_time + 5000 # allows 5 seconds of invulnerability
        self.player.update()
    
    def plus_funct(self):
        self.player.lives += 1
    
    def bomb_funct(self):
        # destroys all objects besides the player
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()

    def check_score_and_scale(self):
        new_size = (int(self.player.rect.width * 1.5), int(self.player.rect.height * 1.5))
        self.player.image = pygame.transform.scale(self.player.image, new_size)
        self.player.rect = self.player.image.get_rect(center=self.player.rect.center)
        # for milestone in self.player.milestones:
        #     if self.player.score >= milestone and milestone not in self.player.reached_milestones:
        #         # Increase player ship size
        #         new_size = (int(self.player.rect.width * 1.5), int(self.player.rect.height * 1.5))
        #         self.player.image = pygame.transform.scale(self.player.image, new_size)
        #         self.player.rect = self.player.image.get_rect(center=self.player.rect.center)
        #         self.player.reached_milestones.add(milestone)
        #         print("Player size increased to", new_size)

    def update(self):
        distance = math.sqrt((self.rect.centerx - self.player.rect.centerx) ** 2 + (self.rect.centery - self.player.rect.centery) ** 2)
        collision_threshold = max(self.rect.width, self.rect.height) / 2 + max(self.player.rect.width, self.player.rect.height) / 2 - 2 * TILESIZE

        self.check_score_and_scale()
            
        # check if within collision threshold to obtain the powerup
        if distance < collision_threshold:
            if self.image == self.images[0]:
                POWERUP_CHANNEL.play(POWERUP_MUSIC)
                self.shield_funct()
            elif self.image == self.images[1]:
                POWERUP_CHANNEL.play(POWERUP_MUSIC)
                self.plus_funct()
            elif self.image == self.images[2]:
                POWERUP_CHANNEL.play(BOMB_MUSIC)
                self.bomb_funct()
            self.kill()  # Remove the powerup sprite after collision
                




import pygame


class Background():

    def __init__(self):
        self.image = pygame.image.load('images/bg0.png')
        self.rect = self.image.get_rect()
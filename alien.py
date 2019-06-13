import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, game_settings, screen):
        """Initialize the alien and its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien at the top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien at its current position."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True of alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """"Move the alien."""
        self.x += (self.game_settings.alien_speed_factor *
                   self.game_settings.fleet_direction)
        self.rect.x = self.x

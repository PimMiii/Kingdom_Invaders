import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """This is the player's ship."""
    def __init__(self, game_settings, screen):
        """Initialize the ship and set it's starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load(self.get_ship_path(game_settings))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store decimal value for the center of the ship
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def get_ship_path(self, game_settings):
        """Get the path to the ship.png image."""
        if game_settings.legacy_flag:
            ship_path = 'images/ship0.png'
        else:
            ship_path = 'images/ship1.png'
        return ship_path

    def update(self):
        """Update the ship's position based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship and it's current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

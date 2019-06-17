import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = False

        # Create a bullet rect at (0,0) and then set correct position.
        # Check if legacy_flag == True
        if game_settings.legacy_flag:
            self.rect = pygame.Rect(0, 0,
                    game_settings.bullet_width, game_settings.bullet_height)
        else:
            self.image = self.get_bullet_image()
            self.rect = self.image.get_rect()

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet's position as decimal value
        self.y = float(self.rect.y)

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen."""
        # If there is a self.image , we cant draw but have to blit.
        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)

    def get_bullet_image(self):
        """Get a drawable image for the bullet."""
        bullet_image = pygame.image.load(self.get_bullet_path())
        return bullet_image

    def get_bullet_path(self):
        """Get the path for the bullet's image."""
        bullet_path = 'images/bullet0.png'
        return bullet_path

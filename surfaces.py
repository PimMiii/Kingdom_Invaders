import os
import pygame


class GameSurfaces:
    """Class to load all surfaces for the game into memory."""

    def __init__(self):
        """Initialize the surfaces dicts."""
        self.alien_surfaces = {}
        self.get_alien_surfaces()

    def alien_surface_path(self, i):
        path = 'images/aliens/alien' + str(i) + '.png'
        surface = pygame.image.load(path)
        return surface

    def get_alien_surfaces(self):
        # get number of files in the aliens dir.
        file_list = os.listdir('images/aliens')
        files = len(file_list)

        # Place surfaces in alien_surfaces dict.
        for i in range(files):
            self.alien_surfaces[i] = self.alien_surface_path(i)

        return self.alien_surfaces



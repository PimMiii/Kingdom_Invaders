import pygame


def window_set_mode(game_settings):
    """initialize the game window."""
    window = pygame.display.set_mode((game_settings.screen_width,
                                      game_settings.screen_height))
    window_set_caption(game_settings)
    return window


def window_set_caption(game_settings):
    """Set the window caption, depending on legacy_flag"""
    if game_settings.legacy_flag:
        pygame.display.set_caption("Alien Invaders")
    else:
        pygame.display.set_caption("Kingdom Invaders")


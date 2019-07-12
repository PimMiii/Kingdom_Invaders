import pygame
from pygame.sprite import Group

from settings import Settings
from background import Background
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from surfaces import GameSurfaces
import game_functions as gf
import window


def run_game():
    # Initialize game and create screen object.
    pygame.init()
    game_settings = Settings()
    screen = window.window_set_mode(game_settings)
    bg = Background()

    # Make the play button.
    play_button = Button(game_settings, screen, "Play")

    # Create an instance to store game statistics, and create a scoreboard.
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)

    # Make a ship, a group of aliens and a group of bullet
    ship = Ship(game_settings, screen)
    aliens = Group()
    bullets = Group()

    # Create an instance of the Surfaces
    game_surfaces = GameSurfaces()

    # Create the fleet of aliens.
    gf.create_fleet(game_settings, game_surfaces, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(game_settings, game_surfaces, screen, stats, sb,
                        play_button, ship, aliens, bullets)
        if stats.game_active:
            gf.update_ship(ship)
            gf.update_bullets(game_settings, game_surfaces, screen, stats, sb,
                              ship, aliens, bullets)
            gf.update_aliens(game_settings, game_surfaces, screen, stats, sb,
                             ship, aliens, bullets)

        gf.update_screen(game_settings, screen, bg, stats, sb, ship, aliens,
                         bullets, play_button)


run_game()

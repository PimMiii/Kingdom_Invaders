import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, game_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(game_settings, screen, ship, bullets):
    """Fire bullet if limit not reached."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False


def check_events(game_settings, game_surfaces, screen, stats, sb, play_button,
                 ship, aliens, bullets):
    """"Respond to keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, game_surfaces, screen, stats, sb,
                              play_button, ship, aliens, bullets, mouse_x,
                              mouse_y)


def check_play_button(game_settings, game_surfaces, screen, stats, sb,
                      play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reset the game settings.
        game_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty bullets and aliens.
        aliens.empty()
        bullets.empty()

        # Create new fleet , and center ship
        create_fleet(game_settings, game_surfaces, screen, ship, aliens)
        ship.center_ship()


def update_screen(game_settings, screen, bg, stats, sb, ship, aliens, bullets,
                  play_button):
    """Update images on te screen and flip the new screen"""
    # Redraw the screen on each pass through of the loop.
    if game_settings.legacy_flag or game_settings.no_background:
        screen.fill(game_settings.bg_color)
    else:
        screen.fill(game_settings.bg_color)
        screen.blit(bg.image, bg.rect)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_ship(ship):
    """Update the position of the player's ship."""
    ship.update()


def update_bullets(game_settings, game_surfaces, screen, stats, sb, ship,
                   aliens, bullets):
    """Update position of bullets and get rid of old ones"""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_alien_bullet_collisions(game_settings, game_surfaces, screen, stats,
                                  sb, ship, aliens, bullets)


def check_alien_bullet_collisions(game_settings, game_surfaces, screen, stats,
                                  sb, ship, aliens, bullets):
    """Respond to alien-bullet collisions"""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        game_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(game_settings, game_surfaces, screen, ship, aliens)


def get_number_aliens_x(game_settings, alien_width):
    """Determine number of aliens that fit on a row."""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(game_settings, ship_height, alien_height):
    """Determine number of rows of aliens will fit on screen."""
    available_space_y = (game_settings.screen_height -
                         (3 * alien_height - ship_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_settings, game_surfaces, screen, aliens, alien_number,
                 row_number):
    """Create an alien and place it in its row."""
    alien = Alien(game_settings, game_surfaces, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, game_surfaces, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(game_settings,game_surfaces, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height,
                                  alien.rect.height)

    # Create first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, game_surfaces, screen, aliens,
                         alien_number, row_number)


def check_fleet_edges(game_settings, aliens):
    """Respond appropriately if any alien hits the edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def ship_hit(game_settings, game_surfaces, screen, stats, sb, ship, aliens,
             bullets):
    """Respond to the ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty bullets and aliens.
        aliens.empty()
        bullets.empty()

        # Create new fleet , and center ship
        create_fleet(game_settings, game_surfaces, screen, ship, aliens)
        ship.center_ship()

        # Pause the game briefly.
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game_settings, game_surfaces, screen, stats, sb, ship,
                        aliens, bullets):
    """Check if any aliens have hit the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship is hit by an alien.
            ship_hit(game_settings, game_surfaces, screen, stats, sb, ship,
                     aliens, bullets)
            break


def update_aliens(game_settings, game_surfaces, screen, stats, sb, ship,
                  aliens, bullets):
    """
    Check if the fleet is at an edge,
     and then update the position of all aliens in the fleet.
    """
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, game_surfaces, screen, stats, sb, ship, aliens,
                 bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(game_settings, game_surfaces, screen, stats, sb, ship,
                        aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
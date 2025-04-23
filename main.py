from classes.classes import Player, simulate_day
import pygame

def display_health_bar(screen, player):
    bar_width = 200
    bar_height = 20
    filled_width = int(bar_width * (player.hp / 100))
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, filled_width, bar_height))  # Filled part
    pygame.draw.rect(screen, (255, 255, 255), (50, 50, bar_width, bar_height), 2)  # Outline

def display_day(screen, day):
    font = pygame.font.Font(None, 36)
    day_text = font.render(f"Day: {day}", True, (255, 255, 255))
    screen.blit(day_text, (300, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("The Adventures of Discrete Math")

    player_name = input("Enter your player name: ")
    player = Player(player_name)

    clock = pygame.time.Clock()
    running = True
    day = 1

    while running and player.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen
        simulate_day(player, day)
        display_health_bar(screen, player)
        display_day(screen, day)
        pygame.display.flip()

        day += 1
        clock.tick(30)  # Limit frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
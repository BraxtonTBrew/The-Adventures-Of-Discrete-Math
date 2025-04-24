import os
import pygame
import random
from classes.classes import Player, Enemy

# ─────────────────────────────────────────
# Setup
# ─────────────────────────────────────────
WIDTH, HEIGHT = 800, 600
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0)
DEFAULT_BTN_W, BTN_H = 120, 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Combat")
clock = pygame.time.Clock()

# ─────────────────────────────────────────
# Font with fallback
# ─────────────────────────────────────────
font_path = "images/fonts/PressStart2P-Regular.ttf"
if os.path.exists(font_path):
    font    = pygame.font.Font(font_path, 24)
    bigfont = pygame.font.Font(font_path, 48)
else:
    print(f"⚠️ Warning: '{font_path}' not found—using default font.")
    font    = pygame.font.Font(None, 36)
    bigfont = pygame.font.Font(None, 72)

# ─────────────────────────────────────────
# Load Images
# ─────────────────────────────────────────
background_img = pygame.transform.scale(
    pygame.image.load("images/title_screen.png"), (WIDTH, HEIGHT)
)
campfire_background = pygame.transform.scale(
    pygame.image.load("images/title_screenf.png"), (WIDTH, HEIGHT)
)
death_image = pygame.transform.scale(
    pygame.image.load("images/death.png"), (WIDTH, HEIGHT)
)
hero_img = pygame.transform.scale(
    pygame.image.load("images/hero.png"), (100, 100)
)
chest_img = pygame.transform.scale(
    pygame.image.load("images/chest.png"), (100, 100)
)

enemy_image_paths = [
    "images/enemies/calc.png",
    "images/enemies/pencil.png",
    "images/enemies/ruler.png",
    "images/enemies/enemy.png",
    "images/enemies/inter.png"
]
enemy_imgs = [
    pygame.transform.scale(pygame.image.load(path), (100, 100))
    for path in enemy_image_paths
]

# ─────────────────────────────────────────
# Player Stats
# ─────────────────────────────────────────
base_hp     = 100
base_attack = 10
base_defense= 5
stat_points = 0  # persists across runs

# ─────────────────────────────────────────
# State Flags
# ─────────────────────────────────────────
campfire_event       = False
campfire_choice_made = False
chest_event          = False
chest_choice_made    = False

# ─────────────────────────────────────────
# Enemy Factory
# ─────────────────────────────────────────
def create_enemy(day):
    hp_val     = 40 + day * 5
    attack_val = 10 + day

    if day % 10 == 0:
        return Enemy(
            f"Boss {day}", hp=hp_val, attack=attack_val, defense=0
        )

    return Enemy(
        f"Monster {day}", hp=hp_val, attack=attack_val, defense=0
    )

# ─────────────────────────────────────────
# Button Class
# ─────────────────────────────────────────
class Button:
    def __init__(self, text, x, y, width=DEFAULT_BTN_W):
        self.text_surf = font.render(text, True, WHITE)
        w = max(width, self.text_surf.get_width() + 20)
        self.rect      = pygame.Rect(x, y, w, BTN_H)
        self.text_rect = self.text_surf.get_rect(
            center=self.rect.center
        )

    def draw(self, surface):
        hover = self.rect.collidepoint(
            pygame.mouse.get_pos()
        )
        color = (70, 70, 250) if not hover else (120, 120, 255)
        pygame.draw.rect(
            surface, color, self.rect,
            border_radius=8
        )
        pygame.draw.rect(
            surface, WHITE, self.rect, 3,
            border_radius=8
        )
        surface.blit(
            self.text_surf, self.text_rect
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ─────────────────────────────────────────
# UI Helpers
# ─────────────────────────────────────────
def draw_health_bar(
    x, y, hp, max_hp, label,
    center_over=None
):
    bar_w = 200
    fill  = int(bar_w * (hp / max_hp))

    if center_over:
        sprite_x, sprite_w = center_over
        x = sprite_x + (sprite_w - bar_w) // 2

    pygame.draw.rect(
        screen, RED, (x, y, bar_w, 20)
    )
    pygame.draw.rect(
        screen, GREEN, (x, y, fill, 20)
    )

    txt   = font.render(
        f"{label} ({int(hp)}/{int(max_hp)})",
        True, BLACK
    )
    txt_x = x if x + txt.get_width() < WIDTH else (
        WIDTH - txt.get_width() - 10
    )
    screen.blit(txt, (txt_x, y - 30))


def draw_text(
    text, x, y,
    color=BLACK,
    use_big=False
):
    surf = (bigfont if use_big else font).render(
        text, True, color
    )
    screen.blit(surf, (x, y))


def draw_panel():
    panel = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    screen.blit(panel, (0, HEIGHT - 200))

# ─────────────────────────────────────────
# Death / Customize Screen
# ─────────────────────────────────────────
def draw_death_screen():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    fade.set_alpha(200)
    screen.blit(fade, (0, 0))

    stat_x   = WIDTH // 2 - 200
    stat_y   = HEIGHT // 2
    spacing  = 60

    title = bigfont.render(
        "GAME OVER", True, WHITE
    )
    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH//2, stat_y - 2*spacing)
        )
    )

    sub = font.render(
        "Customize Your Stats", True, WHITE
    )
    screen.blit(
        sub,
        sub.get_rect(
            center=(WIDTH//2, stat_y - spacing)
        )
    )

    # Attack line
    atk_surf = font.render(
        f"Atk: {base_attack}", True, WHITE
    )
    screen.blit(atk_surf, (stat_x, stat_y))
    attack_plus.rect.topleft = (
        stat_x + atk_surf.get_width() + 15,
        stat_y - attack_plus.rect.height//4
    )
    attack_plus.text_rect = (
        attack_plus.text_surf.get_rect(
            center=attack_plus.rect.center
        )
    )
    attack_plus.draw(screen)

    # HP line
    hp_y    = stat_y + spacing
    hp_surf = font.render(
        f"HP:  {base_hp}", True, WHITE
    )
    screen.blit(hp_surf, (stat_x, hp_y))
    hp_plus.rect.topleft = (
        stat_x + hp_surf.get_width() + 15,
        hp_y - hp_plus.rect.height//4
    )
    hp_plus.text_rect = hp_plus.text_surf.get_rect(
        center=hp_plus.rect.center
    )
    hp_plus.draw(screen)

    # Points
    pts = font.render(
        f"Pts: {stat_points}", True, WHITE
    )
    screen.blit(
        pts,
        pts.get_rect(
            center=(WIDTH//2, stat_y + 2*spacing)
        )
    )

    # Play Again / Quit
    play_again_button.rect.center = (
        WIDTH//2 - 100, HEIGHT - 80
    )
    play_again_button.text_rect = (
        play_again_button.text_surf.get_rect(
            center=play_again_button.rect.center
        )
    )
    quit_button.rect.center = (
        WIDTH//2 + 100, HEIGHT - 80
    )
    quit_button.text_rect = (
        quit_button.text_surf.get_rect(
            center=quit_button.rect.center
        )
    )
    play_again_button.draw(screen)
    quit_button.draw(screen)

# ─────────────────────────────────────────
# Reset Game
# ─────────────────────────────────────────
def reset_game():
    p = Player("Hero")
    p.hp, p.max_hp     = base_hp, base_hp
    p.attack, p.defense= base_attack, base_defense
    p.run_count        = 0
    day                = 1
    e                  = create_enemy(day)
    img                = random.choice(enemy_imgs)
    return p, day, e, img

player, day, enemy, current_enemy_img = reset_game()
reward_message    = ""
game_over         = False

# ─────────────────────────────────────────
# Buttons
# ─────────────────────────────────────────
fight_button      = Button("Fight", 550, 450)
run_button        = Button("Run",   550, 520)
heal_button       = Button("Heal",  300, 450)
buff_button       = Button("Buff",  450, 450)
play_again_button = Button("Play Again", 0, 0, width=200)
quit_button       = Button("Quit",        0, 0)
attack_plus       = Button("+Atk", 0, 0, width=80)
hp_plus           = Button("+HP",  0, 0, width=80)
open_chest        = Button("Open (5)", 300, 350)
skip_chest        = Button("Skip",      450, 350)

# ─────────────────────────────────────────
# Main Loop
# ─────────────────────────────────────────
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Death / Customize ---
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (stat_points > 0 and
                    attack_plus.is_clicked(pos)):
                    base_attack += 1
                    stat_points -= 1
                elif (stat_points > 0 and
                      hp_plus.is_clicked(pos)):
                    base_hp += 5
                    stat_points -= 1
                elif play_again_button.is_clicked(pos):
                    game_over = False
                    player, day, enemy, current_enemy_img = reset_game()
                elif quit_button.is_clicked(pos):
                    running = False
            continue

        # --- Chest Event ---
        if chest_event:
            if (event.type == pygame.MOUSEBUTTONDOWN and
                not chest_choice_made):
                pos = pygame.mouse.get_pos()
                if (open_chest.is_clicked(pos) and
                    stat_points >= 5):
                    stat_points -= 5
                    buff = random.choice([
                        "HP", "Attack", "Defense"
                    ])
                    amt = (random.randint(1,10)
                           if buff == "Defense"
                           else random.randint(5,15))
                    player.add_reward(buff, amt)
                    reward_message = f"+{amt} {buff}!"
                    day += 1
                    enemy, current_enemy_img = (
                        create_enemy(day),
                        random.choice(enemy_imgs)
                    )
                    chest_choice_made = True
                elif skip_chest.is_clicked(pos):
                    stat_points += 1
                    day += 1
                    enemy, current_enemy_img = (
                        create_enemy(day),
                        random.choice(enemy_imgs)
                    )
                    chest_choice_made = True
            continue

        # --- Gameplay Input ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Campfire
            if (campfire_event and
                not campfire_choice_made):
                if heal_button.is_clicked(pos):
                    amt = int((player.max_hp - player.hp)
                              * random.uniform(0.35,1))
                    player.hp += amt
                    reward_message = f"Healed +{amt}!"
                    campfire_choice_made = True
                elif buff_button.is_clicked(pos):
                    buff = random.choice([
                        "HP", "Attack", "Defense"
                    ])
                    amt = (random.randint(1,10)
                           if buff == "Defense"
                           else random.randint(5,15))
                    player.add_reward(buff, amt)
                    reward_message = f"+{amt} {buff}!"
                    campfire_choice_made = True

            # Fight
            elif (fight_button.is_clicked(pos) and
                  not campfire_event):
                if enemy.is_alive():
                    enemy.take_damage(player.attack)
                    if enemy.is_alive():
                        player.take_damage(enemy.attack)
                    else:
                        buff = random.choice([
                            "HP", "Attack", "Defense"
                        ])
                        amt = (random.randint(1,10)
                               if buff == "Defense"
                               else random.randint(5,15))
                        player.add_reward(buff, amt)
                        reward_message = f"+{amt} {buff}!"
                        stat_points += 1
                        day += 1
                        roll = random.random()
                        if roll < 0.25:
                            campfire_event = True
                            campfire_choice_made = False
                        elif roll < 0.35:
                            chest_event = True
                            chest_choice_made = False
                        else:
                            enemy, current_enemy_img = (
                                create_enemy(day),
                                random.choice(enemy_imgs)
                            )

            # Run
            elif (run_button.is_clicked(pos) and
                  player.run_count < 3 and
                  not campfire_event):
                player.run_count += 1
                reward_message = "Ran away!"
                stat_points   += 1
                day           += 1
                roll = random.random()
                if roll < 0.25:
                    campfire_event = True
                    campfire_choice_made = False
                elif roll < 0.35:
                    chest_event = True
                    chest_choice_made = False
                else:
                    enemy, current_enemy_img = (
                        create_enemy(day),
                        random.choice(enemy_imgs)
                    )

    # Death Check
    if not player.is_alive() and not game_over:
        game_over = True
        reward_message = ""

    # ─ Drawing ─
    screen.fill(BLACK)  # clear screen


    # Show reward at bottom middle
    if (reward_message and not game_over and
        not campfire_event and not chest_event):
        msg_surf = font.render(
            reward_message, True, BLACK
        )
        msg_rect = msg_surf.get_rect(
            center=(WIDTH//2, HEIGHT-100)
        )
        screen.blit(msg_surf, msg_rect)

    # Show reward at bottom middle
    if (reward_message and not game_over and
        not campfire_event and not chest_event):
        msg_surf = font.render(
            reward_message, True, BLACK
        )
        msg_rect = msg_surf.get_rect(
            center=(WIDTH//2, HEIGHT-100)
        )
        screen.blit(msg_surf, msg_rect)

    # Death Screen
    if game_over:
        draw_death_screen()

        # Chest Screen
    elif chest_event:
        screen.blit(background_img, (0, 0))
        screen.blit(hero_img,       (100, 300))
        screen.blit(chest_img,      (500, 100))

        # prompt
        prompt = "Chest! Spend 5 pts?"
        pw, _   = font.size(prompt)
        draw_text(prompt, (WIDTH - pw) // 2,  80)

        # ── reposition the two buttons so they never overlap ──
        gap = 20
        w1  = open_chest.rect.width
        w2  = skip_chest.rect.width
        total_w = w1 + gap + w2
        start_x = (WIDTH - total_w) // 2
        y       = 350

        open_chest.rect.topleft = (start_x, y)
        open_chest.text_rect    = open_chest.text_surf.get_rect(center=open_chest.rect.center)

        skip_chest.rect.topleft = (start_x + w1 + gap, y)
        skip_chest.text_rect     = skip_chest.text_surf.get_rect(center=skip_chest.rect.center)

        # finally draw them
        open_chest.draw(screen)
        skip_chest.draw(screen)

        if chest_choice_made:
            chest_event = False

    else:
        screen.blit(
            campfire_background if campfire_event else
            background_img, (0,0)
        )

        # HUD
        draw_text(f"Day: {day}", 10, 10)
        draw_text(f"Points: {stat_points}", WIDTH-150, 10)

        if campfire_event:
            draw_text("Campfire: Choose", 250, 100)
            if not campfire_choice_made:
                heal_button.draw(screen)
                buff_button.draw(screen)
            else:
                draw_text("Click to Continue", 320, 200)
                if pygame.mouse.get_pressed()[0]:
                    campfire_event = False
                    campfire_choice_made = False
                    enemy, current_enemy_img = (
                        create_enemy(day),
                        random.choice(enemy_imgs)
                    )
        else:
            screen.blit(hero_img,            (100,300))
            screen.blit(current_enemy_img,   (500,100))

            draw_health_bar(
                100, 270,
                player.hp, player.max_hp,
                player.name
            )
            draw_health_bar(
                500,  80,
                enemy.hp,   enemy.max_hp,
                enemy.name,
                center_over=(500,100)
            )

            draw_panel()
            fight_button.draw(screen)
            if player.run_count < 3:
                run_button.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
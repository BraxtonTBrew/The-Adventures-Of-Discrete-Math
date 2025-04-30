
import os
import pygame
import random
from classes.classes import Player, Enemy, BossEnemy, Button, StatReward, PointReward, ChestEvent, CampfireEvent

# Setup
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)
DEFAULT_BTN_W, BTN_H = 120, 50
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Combat")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 72)

# Load Images
def safe_load_image(path, size):
    try:
        return pygame.transform.scale(pygame.image.load(path), size)
    except:
        return pygame.Surface(size)

bg_img = safe_load_image("images/title_screen.png", (WIDTH, HEIGHT))
campfire_bg = safe_load_image("images/title_screenf.png", (WIDTH, HEIGHT))
death_img = safe_load_image("images/death.png", (WIDTH, HEIGHT))
hero_img = safe_load_image("images/hero.png", (100, 100))
chest_img = safe_load_image("images/chest.png", (100, 100))

enemy_imgs = [safe_load_image(path, (100, 100)) for path in [
    "images/enemies/calc.png", "images/enemies/pencil.png",
    "images/enemies/ruler.png", "images/enemies/enemy.png",
    "images/enemies/inter.png"
]]

boss_imgs = [safe_load_image("images/boss/jonathan-craton.png", (100, 100))]

# Globals
base_hp, base_attack, base_defense = 100, 10, 5
stat_points = 0
campfire_event = chest_event = None
game_over = False
reward_message = ""

# UI Buttons
fight_button = Button("Fight", 550, 400)
run_button = Button("Run", 550, 460)
heal_button = Button("Heal", 300, 450)
buff_button = Button("Buff", 450, 450)
play_again_button = Button("Play Again", 0, 0, width=200)
quit_button = Button("Quit", 0, 0)
attack_plus = Button("+Atk", 0, 0, width=80)
hp_plus = Button("+HP", 0, 0, width=80)
open_chest = Button("Open (5)", 300, 350)
skip_chest = Button("Skip", 450, 350)

# Enemy Factory
def create_enemy(day):
    hp = 40 + day * 5
    attack = 10 + day
    if day % 10 == 0:
        return BossEnemy(f"Boss {day}", hp, attack), boss_imgs
    return Enemy(f"Monster {day}", hp, attack, 0), random.choice(enemy_imgs)

# Game Reset
def reset_game():
    p = Player("Hero")
    p.hp = p.max_hp = base_hp
    p.attack, p.defense = base_attack, base_defense
    p.run_count = 0
    d = 1
    e, img = create_enemy(d)
    return p, d, e, img

player, day, enemy, current_enemy_img = reset_game()
boss_frame_index = boss_frame_timer = 0


def draw_text(text, x, y, color=BLACK, use_big=False):
    surf = (bigfont if use_big else font).render(text, True, color)
    screen.blit(surf, (x, y))

def draw_health_bar(x, y, hp, max_hp, label):
    bar_w = 200
    fill = int(bar_w * (hp / max_hp))
    pygame.draw.rect(screen, RED, (x, y, bar_w, 20))
    pygame.draw.rect(screen, GREEN, (x, y, fill, 20))
    txt = font.render(f"{label} ({int(hp)}/{int(max_hp)})", True, BLACK)
    screen.blit(txt, (x, y - 30))

def draw_panel():
    panel = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    screen.blit(panel, (0, HEIGHT - 200))

def draw_death_screen():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    fade.set_alpha(200)
    screen.blit(fade, (0, 0))

    sx, sy, sp = WIDTH // 2 - 200, HEIGHT // 2, 60
    draw_text("GAME OVER", WIDTH // 2 - 120, sy - 2 * sp, WHITE, use_big=True)
    draw_text("Customize Your Stats", WIDTH // 2 - 140, sy - sp, WHITE)

    atk_s = font.render(f"Atk: {base_attack}", True, WHITE)
    screen.blit(atk_s, (sx, sy))
    attack_plus.rect.topleft = (sx + atk_s.get_width() + 15, sy - attack_plus.rect.height // 4)
    attack_plus.text_rect = attack_plus.text_surf.get_rect(center=attack_plus.rect.center)
    attack_plus.draw(screen)

    hp_y = sy + sp
    hp_s = font.render(f"HP: {base_hp}", True, WHITE)
    screen.blit(hp_s, (sx, hp_y))
    hp_plus.rect.topleft = (sx + hp_s.get_width() + 15, hp_y - hp_plus.rect.height // 4)
    hp_plus.text_rect = hp_plus.text_surf.get_rect(center=hp_plus.rect.center)
    hp_plus.draw(screen)

    pts = font.render(f"Pts: {stat_points}", True, WHITE)
    screen.blit(pts, pts.get_rect(center=(WIDTH // 2, sy + 2 * sp)))

    play_again_button.rect.center = (WIDTH // 2 - 100, HEIGHT - 80)
    play_again_button.text_rect = play_again_button.text_surf.get_rect(center=play_again_button.rect.center)
    play_again_button.draw(screen)

    quit_button.rect.center = (WIDTH // 2 + 100, HEIGHT - 80)
    quit_button.text_rect = quit_button.text_surf.get_rect(center=quit_button.rect.center)
    quit_button.draw(screen)

def draw_everything():
    global boss_frame_timer, boss_frame_index
    screen.fill(BLACK)

    if game_over:
        draw_death_screen()
    elif chest_event:
        screen.blit(bg_img, (0, 0))
        screen.blit(hero_img, (100, 300))
        screen.blit(chest_img, (500, 100))
        draw_text("Chest! Spend 5 pts?", 300, 80)
        open_chest.draw(screen)
        skip_chest.draw(screen)
    else:
        screen.blit(campfire_bg if campfire_event else bg_img, (0, 0))
        draw_text(f"Day: {day}", 10, 10)
        draw_text(f"Points: {stat_points}", WIDTH - 150, 10)

        if campfire_event:
            draw_text("Campfire: Choose", 250, 100)
            if not campfire_event.choice_made:
                heal_button.draw(screen)
                buff_button.draw(screen)
            else:
                draw_text("Click to Continue", 320, 200)
        else:
            screen.blit(hero_img, (100, 300))
            img = current_enemy_img[boss_frame_index] if isinstance(current_enemy_img, list) else current_enemy_img
            screen.blit(img, (500, 100))
            draw_health_bar(100, 270, player.hp, player.max_hp, player.name)
            draw_health_bar(500, 80, enemy.hp, enemy.max_hp, enemy.name)
            draw_panel()
            fight_button.draw(screen)
            if player.run_count < 3:
                run_button.draw(screen)

        if reward_message:
            msg = font.render(reward_message, True, BLACK)
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            screen.blit(msg, rect)

    draw_text(f"ATK: {player.attack}  DEF: {player.defense}  HP: {int(player.hp)}/{int(player.max_hp)}", 20, HEIGHT - 40)

    pygame.display.flip()
    if isinstance(current_enemy_img, list):
        boss_frame_timer += 1
        if boss_frame_timer >= 15:
            boss_frame_timer = 0
            boss_frame_index = (boss_frame_index + 1) % len(current_enemy_img)
    clock.tick(30)

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if stat_points > 0 and attack_plus.is_clicked(pos):
                    base_attack += 1
                    stat_points -= 1
                elif stat_points > 0 and hp_plus.is_clicked(pos):
                    base_hp += 5
                    stat_points -= 1
                elif play_again_button.is_clicked(pos):
                    game_over = False
                    player, day, enemy, current_enemy_img = reset_game()
                elif quit_button.is_clicked(pos):
                    running = False
            continue

        if chest_event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not chest_event.choice_made:
                    if open_chest.is_clicked(pos) and stat_points >= 5:
                        stat_points -= 5
                        chest_event.process_choice(player)
                        reward_message = f"+{chest_event.buff.amount} {chest_event.buff.stat}!"
                    elif skip_chest.is_clicked(pos):
                        stat_points += 1
                        reward_message = "Skipped chest +1 Point"
                        chest_event.choice_made = True
                else:
                    chest_event = None
                    day += 1
                    enemy, current_enemy_img = create_enemy(day)
            continue

        if campfire_event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not campfire_event.choice_made:
                    if heal_button.is_clicked(pos):
                        campfire_event.process_choice(player)
                        reward_message = "Healed!"
                    elif buff_button.is_clicked(pos):
                        campfire_event = ChestEvent()
                        campfire_event.process_choice(player)
                        reward_message = f"+{campfire_event.buff.amount} {campfire_event.buff.stat}!"
                else:
                    campfire_event = None
                    day += 1
                    enemy, current_enemy_img = create_enemy(day)
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if fight_button.is_clicked(pos):
                if enemy.is_alive():
                    enemy.take_damage(player.attack)
                    if enemy.is_alive():
                        player.take_damage(enemy.attack)
                    else:
                        reward = StatReward(random.choice(["HP", "Attack", "Defense"]), random.randint(5, 15))
                        reward.apply(player)
                        reward_message = f"+{reward.amount} {reward.stat}!"
                        stat_points += 1
                        day += 1
                        roll = random.random()
                        if roll < 0.25:
                            campfire_event = CampfireEvent()
                        elif roll < 0.35:
                            chest_event = ChestEvent()
                        else:
                            enemy, current_enemy_img = create_enemy(day)
            elif run_button.is_clicked(pos) and player.run_count < 3:
                player.run_count += 1
                reward_message = "Ran away!"
                stat_points += 1
                day += 1
                roll = random.random()
                if roll < 0.25:
                    campfire_event = CampfireEvent()
                elif roll < 0.35:
                    chest_event = ChestEvent()
                else:
                    enemy, current_enemy_img = create_enemy(day)

    if not player.is_alive() and not game_over:
        game_over = True
        reward_message = ""

    draw_everything()

pygame.quit()
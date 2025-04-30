
import pygame
import os
import random
from abc import ABC, abstractmethod




WIDTH, HEIGHT = 800, 600
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0)
DEFAULT_BTN_W, BTN_H = 120, 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Combat")
clock = pygame.time.Clock()

font_path = "images/fonts/PressStart2P-Regular.ttf"
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 24)
    bigfont = pygame.font.Font(font_path, 48)
else:
    print(f" Warning: '{font_path}' not found—using default font.")
    font = pygame.font.Font(None, 36)
    bigfont = pygame.font.Font(None, 72)




def safe_load_image(path, size):
    try:
        return pygame.transform.scale(pygame.image.load(path), size)
    except Exception as e:
        print(f" Could not load image: {path} ({e})")
        return pygame.Surface(size)


# Abstract Base Classes

class Character(ABC):
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.max_hp = hp

    @abstractmethod
    def take_damage(self, damage):
        pass

    def is_alive(self):
        return self.hp > 0

class Item(ABC):
    @abstractmethod
    def apply(self, player):
        pass


# Character Classes

class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 10, 5)
        self.run_count = 0

    def take_damage(self, damage):
        reduction = 0.2 * self.defense
        mitigated = max(0, damage - reduction)
        self.hp = max(0, self.hp - mitigated)

    def add_reward(self, reward_type, amount):
        if reward_type == "HP":
            self.hp = min(self.hp + amount, self.max_hp)
        elif reward_type == "Attack":
            self.attack += amount
        elif reward_type == "Defense":
            self.defense += amount
class Enemy(Character):
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)

    def take_damage(self, damage):
        reduction = 0.2 * self.defense
        mitigated = max(0, damage - reduction)
        self.hp = max(0, self.hp - mitigated)

class BossEnemy(Enemy):
    def __init__(self, name, hp, attack):
        super().__init__(name, hp * 2, attack + 5, 5)


# Reward and Item System

class Reward:
    def apply(self, player):
        pass

class StatReward(Reward):
    def __init__(self, stat, amount):
        self.stat = stat
        self.amount = amount

    def apply(self, player):
        player.add_reward(self.stat, self.amount)

class PointReward(Reward):
    def __init__(self, points):
        self.points = points

    def apply(self, player):
        pass  # Points are handled by external stat counter

class HealthItem(Item):
    def __init__(self, heal_percent):
        self.heal_percent = heal_percent

    def apply(self, player):
        heal = int((player.max_hp - player.hp) * self.heal_percent)
        player.hp = min(player.max_hp, player.hp + heal)

class BuffItem(Item):
    def __init__(self, stat, amount):
        self.stat = stat
        self.amount = amount

    def apply(self, player):
        player.add_reward(self.stat, self.amount)


# Game Events

class GameEvent:
    def __init__(self):
        self.choice_made = False

    def process_choice(self, player):
        pass

class ChestEvent(GameEvent):
    def __init__(self):
        super().__init__()
        self.buff = BuffItem(random.choice(["HP", "Attack", "Defense"]), random.randint(5, 15))

    def process_choice(self, player):
        self.buff.apply(player)
        self.choice_made = True

class CampfireEvent(GameEvent):
    def __init__(self):
        super().__init__()
        self.heal = HealthItem(random.uniform(0.35, 1))

    def process_choice(self, player):
        self.heal.apply(player)
        self.choice_made = True


# Button Class (UI Component)

class Button:
    def __init__(self, text, x, y, width=DEFAULT_BTN_W):
        self.text_surf = font.render(text, True, WHITE)
        w = max(width, self.text_surf.get_width() + 20)
        self.rect = pygame.Rect(x, y, w, BTN_H)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = (120, 120, 255) if hover else (70, 70, 250)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=8)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

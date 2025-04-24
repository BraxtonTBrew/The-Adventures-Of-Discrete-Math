import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.defense = 5

    def take_damage(self, damage):
        damage_reduction = 0.2 * self.defense
        mitigated_damage = max(0, damage - damage_reduction)
        self.hp -= mitigated_damage
        self.hp = max(0, self.hp)
        print(f"{self.name} takes {mitigated_damage} damage. HP is now {self.hp}")

    def is_alive(self):
        return self.hp > 0

    def add_reward(self, reward_type, amount):
        if reward_type == "HP":
            self.hp += amount
            self.hp = min(self.hp, 100)
        elif reward_type == "Attack":
            self.attack += amount
        elif reward_type == "Defense":
            self.defense += amount
        print(f"{reward_type} increased by {amount}. New stats - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}")

class Enemy:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.max_hp = hp

    def take_damage(self, damage):
        damage_reduction = 0.2 * self.defense
        mitigated_damage = max(0, damage - damage_reduction)
        self.hp -= mitigated_damage
        self.hp = max(0, self.hp)
        print(f"{self.name} takes {mitigated_damage} damage. HP is now {self.hp}")

    def is_alive(self):
        return self.hp > 0

def simulate_day(player, day):
    print(f"Day {day} begins!")
    enemy = Enemy(f"Monster {day}", hp=random.randint(30, 70), attack=random.randint(5, 15), defense=random.randint(3, 8))
    print(f"A wild {enemy.name} appears! Stats - HP: {enemy.hp}, Attack: {enemy.attack}, Defense: {enemy.defense}")

    while player.is_alive() and enemy.is_alive():
        enemy.take_damage(player.attack)
        if not enemy.is_alive():
            print(f"{enemy.name} has been defeated!")
            break

        player.take_damage(enemy.attack)
        if not player.is_alive():
            print(f"{player.name} has fallen!")
            return False

    if player.is_alive():
        reward_type = random.choice(["HP", "Attack", "Defense"])
        reward_amount = random.randint(5, 15)
        player.add_reward(reward_type, reward_amount)
        print(f"Day {day} ends. Prepare for the next challenge!")

    return True

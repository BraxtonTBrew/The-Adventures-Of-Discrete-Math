class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.defense = 5

    def take_damage(self, damage):
        mitigated_damage = max(0, damage - self.defense)
        self.hp -= mitigated_damage
        print(f"{self.name} takes {mitigated_damage} damage. HP is now {self.hp}")

    def is_alive(self):
        return self.hp > 0

    def add_reward(self, reward_type, amount):
        if reward_type == "HP":
            self.hp += amount
        elif reward_type == "Attack":
            self.attack += amount
        elif reward_type == "Defense":
            self.defense += amount
        print(f"{reward_type} increased by {amount}. New stats - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}")
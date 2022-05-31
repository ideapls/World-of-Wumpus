class Character:

    def __init__(self, arrow, gold, action):
        self.arrow = arrow
        self.gold = gold
        self.action = action

    def shoot(self):
        self.arrow = self.arrow - 1

    def take_gold(self):
        self.gold = self.gold + 1000

    def lose_gold(self):  # Se for devorado pelo monstro ou cair no poço
        self.gold = self.gold - 1000

    def lose_one_action(self):
        self.action = self.action - 1

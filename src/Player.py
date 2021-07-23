from Trade_Card import Trade_Card
from Place import Place
from Station import Station

class Player:

    max_cards = {0:{"YELLOW":3, "RED":3,
        "ORANGE":3, "PINK":3, "BLUE":3,
        "BROWN":2, "PURPLE":2, "GREEN":3}, 1:2, 2:4}

    def __init__(self, name:str, id:int, balance = 1500, jail_cards = 0):
        self.name = name
        self.id = id
        self.balance = balance
        self.jail_cards = jail_cards
        self.count_cards = {0:{"YELLOW":0, "RED":0,
            "ORANGE":0, "PINK":0, "BLUE":0,
            "BROWN":0, "PURPLE":0, "GREEN":0}, 1:0, 2:0}
        self.cards = {}
    
    def __str__(self):
        return self.name + ' (bal: ${})'.format(self.balance)
    
    def __eq__(self, other_player):
        return self.id == other_player.id
    
    def _buy_card_helper(self, card:Trade_Card):
        card.sold = True
        card.player = self.id
        card_type = card.get_type()
        if (card_type):
            self.count_cards[card_type] += 1
        else:
            self.count_cards[card_type][card.color] += 1
        self.cards[card.id] = card
    
    # 0: succesfull, 1: Insufficient funds
    def buy_card(self, card:Trade_Card, purchase_price = 0) -> int:
        if purchase_price:
            rem_balance = self.balance - purchase_price
        else:
            rem_balance = self.balance - card.purchase_price
        if (rem_balance < 0):
            return 1
        self.balance = rem_balance
        self._buy_card_helper(card)
        return 0

    # 0: successful, 1: Insufficient funds, 2: not full set
    # 3: Mortgaged card 4: Inequal distribution of houses and hotels
    # 5: Invalid id 6: Invalid card type
    def build(self, id) -> int:
        if (id not in self.cards):
            return 5
        card = self.cards[id]
        if (card.get_type()):
            return 6
        rem_balance = self.balance - card.build_cost
        if (rem_balance < 0):
            return 1
        if (not self.count_cards[0][card.color] == 
            Player.max_cards[0][card.color]):
            return 2
        if (self._color_in_mortgaged(card.color)):
            return 3
        tmp_houses = card.houses + 1
        for i in self._get_cards_of_color(card.color):
            if ((tmp_houses-i.houses)%5 > 1):
                return 4
        if (tmp_houses == 5):
            card.houses = 0
            card.hotels += 1
        else:
            card.houses = tmp_houses
        self.balance = rem_balance
        return 0
    
    def is_hotel_ready(self, color:str) -> bool:
        if (color in self.count_cards[0] and 
            self.count_cards[0][color] == Player.max_cards[0][color]):
            return not self._color_in_mortgaged(color)
        return False
    
    def _color_in_mortgaged(self, color) -> bool:
        for i in self._get_cards_of_color(color):
            if i.mortgaged:
                return True
        return False

    def _get_cards_of_color(self, color:str):
        color_cards = []
        for key, val in self.cards.items():
            if (val.color == color):
                color_cards.append(val)
        return color_cards
    
    
    # 2: Invalid id, 1: Insufficinet funds, 0: Successful
    # 3: already mortgaged
    def demortgage_card(self, id) -> int:
        if (id not in self.cards):
            return 2
        card = self.cards[id]
        if not card.mortgaged:
            return 3
        rem_balance = self.balance - card.get_demortgage_value()
        if (rem_balance < 0):
            return 1
        self.balance = rem_balance
        card.mortgaged = False
        return 0
    
    # strip before printing
    def get_cards(self):
        s = ""
        i = 0
        for key, val in self.cards.items():
            if (i%2==0):
                s += '\t{:02d}. {:45s}'.format(key, 
                    str(val).replace('_', ' ')) + '\t'
            else:
                s += '{:02d}. {:45s}'.format(key, 
                    str(val).replace('_', ' ')) + '\n'
            i += 1
        if s == '':
            s = 'No cards to display!'
        return s[:-1]
    
    def _house_on_color(self, color):
        for i in self._get_cards_of_color(color):
            if i.houses or i.hotels:
                return True
        return False

    def check_trade(self, card_out):
        if (isinstance(card_out, str)):
            return 1
        if (card_out):
            if card_out.id not in self.cards:
                return 2
            elif self._house_on_color(card_out.color):
                return 3
        else:
            return 1
        return 0

    def check_money(self, money_in = 0, money_out = 0):
        if money_out-money_in > self.balance:
            return 1
        return 0

    def trade_money(self, money_in = 0, money_out = 0):
        if (self.check_money(money_in, money_out)):
            return 1
        self.balance += money_in - money_out
        return 0
    
    def _remove_card(self, card:Trade_Card):
        trade_check = self.check_trade(card)
        if trade_check:
            return trade_check
        self.cards.pop(card.id)
        card_type = card.get_type()
        if card_type:
            self.count_cards[card_type] -= 1
        else:
            self.count_cards[card_type][card.color] -= 1
        return 0
    

    def is_bankurpt(self, pay = 0):
        net_worth = self.balance - pay
        for key, val in self.cards.items():
            if not val.mortgaged:
                net_worth += val.mortgage_value
        return net_worth <= 0

    def pay_rent(self, rent:int):
        if self.balance < rent:
            if (self.is_bankurpt(rent)):
                print('You could not afford rent! You\'re bankurpt:(')
                return 1
            print('You need to raise some money or quit!')
            quit_option = input('Do you want to quit? [y/n]').lower()
            if (quit_option == 'y'):
                return 1
            print('Great! Select properties to sell houses or mortgage')
            while (self.balance < rent):
                print(str(self))
                print(self.get_cards())
                try:
                    property_id = int(input('Select property: '))
                    self.raise_money(property_id)
                except:
                    print('Invalid input!')    
        self.balance -= rent
        return 0
    
    # 1: card not present, 2: cannot mortgage card with hotel
    # 0: successful 3: card already mortgaged
    def mortgage_card(self, id) -> int:
        if (id not in self.cards):
            return 1
        card = self.cards[id]
        if (card.mortgaged):
            return 3
        if not card.get_type():
            for i in self._get_cards_of_color(card.color):
                if (i.houses or i.hotels):
                    return 2
        card.mortgaged = True
        self.balance += card.mortgage_value
        return 0
    
    def sell_house(self, id):
        if id in self.cards:
            card = self.cards[id]
        else:
            return 1
        if (card.houses):
            card.houses -= 1
            self.balance += card.build_cost / 2
        elif (card.hotels):
            card.hotels -= 1
            self.balance += card.build_cost / 2
        else:
            return 4
        return 0
    
    #add checks
    def raise_money(self, id):
        if id in self.cards:
            card = self.cards[id]
        else:
            return 1
        if (card.houses or card.hotels):
            return self.sell_house(id)
        else:
            return self.mortgage_card(id)
    

        


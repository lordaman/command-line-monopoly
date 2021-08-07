from Trade_Card import Trade_Card
from bcolors import bcolors

class Station( Trade_Card ):

    def __init__(self, name:str, id:int, purchase_price = 200, 
        mortgage_value = 100, rent_cards = [25, 50, 100, 200]):
        Trade_Card.__init__(self, name, purchase_price, mortgage_value, id)
        self.rent_cards = rent_cards
    
    def get_type(self) -> int:
        return 2
    
    def __str__(self):
        return '{}{:25} ${:3d}'.format(
            bcolors.UNDERLINE, self.name, 
            self.purchase_price) + (
            ' O{}'.format(self.player) if self.sold else '') + (
            ' M' if self.mortgaged else '') + (
            ' {}h'.format(self.houses) if self.houses else '') + (
            ' {}H'.format(self.hotels) if self.hotels else '') + f' {bcolors.ENDC}'
    
    def __repr__(self):
        curtain = '=' * 40
        purchase_price = 'PURCHASE PRICE: ${}'.format(self.purchase_price)
        rent = 'RENT: ${}'.format(self.rent_cards[0])
        line1 = 'If 2 R.R\'s are owned: ${}'.format(self.rent_cards[1])
        line2 = 'If 3 R.R\'s are owned: ${}'.format(self.rent_cards[2])
        line3 = 'If 4 R.R\'s are owned: ${}'.format(self.rent_cards[3])
        mortgage_val = 'MORTGAGE VALUE ${}'.format(self.mortgage_value)
        s = '{:^120}\n\n{:^120}\n{:^120}\n{:^120}\n'.format(
            curtain, self.name.replace('_', ' '), purchase_price, rent
        ) + '{:^120}\n{:^120}\n{:^120}\n{:^120}\n\n{:^120}'.format(
            line1, line2, line3, mortgage_val, curtain
        )
        return s


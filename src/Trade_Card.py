from bcolors import bcolors
# parent class and alias class for UTILITIES
class Trade_Card:

    def __init__(self, name:str, purchase_price:int, mortgage_value:int, id:int):
        self.name = name
        self.purchase_price = purchase_price
        self.mortgage_value = mortgage_value
        self.id = id
        self.sold = False
        self.player = -1
        self.mortgaged = False
        self.hotels = 0
        self.houses = 0
        self.color = 'WHITE'
    
    def __eq__(self, another_card) -> bool:
        return self.name == another_card.name
    
    def __str__(self):
        return '{}{:16} ${:3d}'.format(
            Trade_Card.get_color_code(self.color), self.name, 
            self.purchase_price) + (
            ' O{}'.format(self.player) if self.sold else '') + (
            ' M' if self.mortgaged else '') + (
            ' {}h'.format(self.houses) if self.houses else '') + (
            ' {}H'.format(self.hotels) if self.hotels else '') + f'{bcolors.ENDC}'
    
    def __repr__(self):
        curtain = '=' * 40
        purchase_price = 'PURCHASE PRICE: ${}'.format(self.purchase_price)
        line1 = 'If one \'Utility\' is owned'
        line2 = 'rent is 4 times amount shown on dice.'
        line3 = 'If both \'Utilities\' are owned'
        line4 = 'rent is 10 times amount shown on dice.'
        mortgage_val = 'MORTGAGE VALUE  ${}'.format(self.mortgage_value)
        s = '{:^120}\n\n{}{:^120}{}\n{:^120}\n'.format(
                curtain, Trade_Card.get_color_code(self.color), 
                self.name, bcolors.ENDC, purchase_price) + (
            '{:^120}\n{:^120}\n{:^120}\n{:^120}\n{:^120}\n\n{:^120}'.format(
                line1, line2, line3, line4, mortgage_val, curtain
            ))
        return s

    def get_type(self) -> int:
        return 1
    
    def get_demortgage_value(self) -> int:
        return int((110 * self.mortgage_value) / 100)
    
    @classmethod
    def get_color_code(cls, color):
        if color == 'YELLOW':
            return bcolors.YELLOW
        elif color == 'RED':
            return bcolors.RED
        elif color == 'ORANGE':
            return bcolors.ORANGE
        elif color == 'PINK':
            return bcolors.PURPLE
        elif color == 'BLUE':
            return bcolors.CYAN
        elif color == 'BROWN':
            return bcolors.BROWN
        elif color == 'PURPLE':
            return bcolors.BLUE
        elif color == 'GREEN':
            return bcolors.GREEN
        return bcolors.BOLD

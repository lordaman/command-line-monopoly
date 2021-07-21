from Trade_Card import Trade_Card
from bcolors import bcolors


class Place( Trade_Card ):

    def __init__(self, name:str, purchase_price:int, mortgage_value:int, id:int, 
        color:str, rent:int, rent_houses:list, rent_hotel:int, build_cost:int):
        Trade_Card.__init__(self, name, purchase_price, mortgage_value, id)
        self.color = color
        self.rent = rent
        self.rent_houses = rent_houses
        self.rent_hotel = rent_hotel
        self.build_cost = build_cost
    
    def get_type(self) -> int:
        return 0
    
    def __repr__(self):
        curtain = '=' * 40
        purchase_price = 'PURCHASE PRICE: ${}'.format(self.purchase_price)
        rent = 'RENT: ${}'.format(self.rent)
        rent_house1 = 'WITH 1 HOUSE:  ${}'.format(self.rent_houses[0])
        rent_house2 = 'WITH 2 HOUSES:  ${}'.format(self.rent_houses[1])
        rent_house3 = 'WITH 3 HOUSES:  ${}'.format(self.rent_houses[2])
        rent_house4 = 'WITH 4 HOUSES:  ${}'.format(self.rent_houses[3])
        rent_hotel = 'WITH HOTEL: ${}'.format(self.rent_hotel)
        mortgage_value = 'MORTGAGE VALUE ${}'.format(self.mortgage_value)
        build_cost = 'BUILD COST ${}'.format(self.build_cost)

        s = '{:^120}\n\n{}{:^120}{}\n{:^120}\n{:^120}\n'.format(
                curtain, Trade_Card.get_color_code(self.color), 
                self.name, bcolors.ENDC, purchase_price, rent) + (
            '{:^120}\n{:^120}\n{:^120}\n{:^120}\n'.format(
                rent_house1, rent_house2, rent_house3, rent_house4)) +(
            '{:^120}\n{:^120}\n{:^120}\n\n{:^120}'.format(
                rent_hotel, mortgage_value, build_cost, curtain))
        return s
    
    




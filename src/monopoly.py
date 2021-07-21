#!/usr/bin/env python3

from Board import Board
from Trade_Card import Trade_Card
from Station import Station
from Place import Place
from Player import Player
from os import system, name
from bcolors import bcolors

class monopoly:
    def __init__(self, roll_choice):
        super().__init__()
        self.board = Board()
        self.board._parse_board()
        self.curr_player = 0
        self.num_rolls = 0
        self.roll_choice = roll_choice

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def print_players(self):
        print('Players:')
        for i in self.board.players:
            print('\t{}. {}'.format(i.id, str(i)))

    def clear_and_print(self):
        self.clear()
        print(self.board.print_board())
        print('{:^120}'.format(self.board.get_balances()))
    
    def get_rent(self, rent):
        player_tmp = self.board.players[self.curr_player]
        if (player_tmp.pay_rent(rent)):
            self.board._remove_player(player_tmp.id)
            self.curr_player = (self.curr_player) % len(self.board.players)
            self.num_rolls = 0
            rent = min(rent, player_tmp.balance)
        return rent
    
    def go_to_jail(self):
        self.board.jail_players[self.board.players[self.curr_player].id] = 3
        self.curr_player = (self.curr_player + 1) % len(self.board.players)
        self.num_rolls = 0

    def roll_action_place(self, card_owner, forward_land):
        rent = forward_land.rent
        if (forward_land.houses or forward_land.hotels):
            rent = forward_land.rent_houses[
                forward_land.houses-1] + (
                forward_land.hotels * forward_land.rent_hotel)
        elif (card_owner.count_cards[0][forward_land.color] == 
            Player.max_cards[0][forward_land.color]):
            rent *= 2
        return rent

    def roll_action_utility(self, card_owner, forward_land, roll_number):
        rent = roll_number * 4
        if (card_owner.count_cards[1] == 2):
            rent = roll_number * 10
        return rent
        
    def roll_action_station(self, card_owner, forward_land):
        rent = forward_land.rent_cards[card_owner.count_cards[2]-1]
        return rent
        
    def roll_action_card(self, forward_land, roll_number):
        if forward_land.sold:
            player_tmp = self.board.players[self.curr_player]
            if (forward_land.player == player_tmp.id):
                print("Yayy! You own this property.")
            elif (forward_land.mortgaged):
                print('Yay! No rent since property is mortgaged.')
            else:
                card_owner = self.board._get_player_using_id(forward_land.player)[1]
                forward_type = forward_land.get_type()
                if (forward_type == 0):
                    rent = self.roll_action_place(card_owner, forward_land)
                elif (forward_type == 1):
                    rent = self.roll_action_utility(card_owner, forward_land, roll_number)
                elif (forward_type == 2):
                    rent = self.roll_action_station(card_owner, forward_land)
                    if roll_number == -1:
                        rent *= 2
                else:
                    return
                rent = self.get_rent(rent)
                card_owner.balance += rent
                print('You paid ${} to {}'.format(rent, card_owner.name))
        else:
            while True:
                print(repr(forward_land))
                buy_option = input('Do you want to buy {}? {}[y/n]{}: '.format(
                    forward_land.name, bcolors.YELLOW, bcolors.ENDC)).lower()
                if (len(buy_option) < 1):
                    continue
                if buy_option[0] == 'y':
                    if (self.board.players[self.curr_player].buy_card(forward_land)):
                        print('You do not have sufficient funds! It\'s a bidding war')
                        self.board.bid_war(forward_land)
                    else:
                        print('You have bought {}!'.format(forward_land.name))
                    break
                elif buy_option[0] == 'n':
                    self.board.bid_war(forward_land)
                    break
                else:
                    print('Invalid input')

    def community_function(self):
        val = self.board.get_community_or_chance()
        cplayer = self.board.players[self.curr_player]
        print(self.board.print_chance_community(Board.cc[val]))
        if val == 0:
            cplayer.balance += 100
        elif val == 1:
            self.get_rent(50)
        elif val == 2:
            self.get_rent(150)
        elif val == 3:
            cplayer.balance += 100
        elif val == 4:
            self.go_to_jail()
        elif val == 5:
            cplayer.balance += 45
        elif val == 6:
            curr_id = cplayer.id
            curr_pos = (self.curr_player + 1) % len(self.board.players)
            rent = 0
            player_tmp = self.board.players[curr_pos]
            while not player_tmp.id == curr_id:
                if (player_tmp.pay_rent(50)):
                    self.board._remove_player(player_tmp.id)
                    curr_pos = (curr_pos) % len(self.board.players)
                    rent += min(rent, player_tmp.balance)
                else:
                    curr_pos = (curr_pos+1) % len(self.board.players)
                    rent += 50
                player_tmp = self.board.players[curr_pos]
            self.curr_player = curr_pos
            player_tmp.balance += rent        
        elif val == 7:
            player_houses = player_hotels = 0
            for key, val in cplayer.cards.items():
                player_hotels += val.hotels
                player_houses += val.houses
            self.get_rent(40*player_houses + 115*player_hotels)
        elif val == 8:
            cplayer.balance += 20
        elif val == 9:
            cplayer.balance += 200
        elif val == 10:
            cplayer.jail_cards += 1
        elif val == 11:
            cplayer.balance += 10
        elif val == 12:
            cplayer.balance += 100
        elif val == 13:
            self.board.player_positions[self.curr_player] = 0
            cplayer.balance += 200
        elif val == 14:
            self.get_rent(100)
        elif val == 15:
            cplayer.balance += 25
    
    def jump_to_place(self, jump_pos, double_rent):
        if (jump_pos < 
            self.board.player_positions[self.curr_player]):
            self.receive_salary()
        self.board.player_positions[self.curr_player] = jump_pos
        forward_land = self.board.board[jump_pos]
        print('You have landed on {}!'.format(
            forward_land.name.replace('_', ' ')))
        roll_number = 0
        if (forward_land.get_type() == 1):
            roll_number = Board.roll_dice() + Board.roll_dice()
            print('You rolled a {}'.format(roll_number))
        if (double_rent):
            self.roll_action_card(forward_land, -1)
        else:
            self.roll_action_card(forward_land, roll_number)

    
    def chance_function(self):
        # val = self.board.get_community_or_chance()
        val = 15
        cplayer = self.board.players[self.curr_player]
        print(self.board.print_chance_community(Board.chance[val]))
        if val == 0:
            self.jump_to_place(5, False)
        elif val == 1:
            cplayer.balance += 50
        elif val == 2:
            cplayer.jail_cards += 1
        elif val == 3:
            player_houses = player_hotels = 0
            for key, val in cplayer.cards.items():
                player_hotels += val.hotels
                player_houses += val.houses
            self.get_rent(25*player_houses + 100*player_hotels)
        elif val == 4:
            self.get_rent(15)
        elif val == 5:
            jump_pos = ((self.board.
                player_positions[
                self.curr_player]+5)/10)*10 + 5
            self.jump_to_place(jump_pos, True)
        elif val == 6:
            rent = (len(self.board.players) - 1) * 50
            player_tmp = self.board.players[self.curr_player]
            self.get_rent(rent)
            for i in self.board.players:
                if not i.id == player_tmp.id:
                    i.balance += 50
        elif val == 7:
            pos = self.board.player_positions[self.curr_player]
            if pos == 7:
                self.board.player_positions[self.curr_player] = 4
                print('You have landed on Income Tax:(')
                rent = self.get_rent(50)
                print('You paid ${} to Income Tax!'.format(rent))
            elif pos == 22:
                self.jump_to_place(19, False)
            elif pos == 36:
                self.board.player_positions[self.curr_player] = 33
                print('You have landed on Community Chest!')
                self.community_function()
        elif val == 8:
            self.go_to_jail()
        elif val == 9:
            self.jump_to_place(24, False)
        elif val == 10:
            self.board.player_positions[self.curr_player] = 0
            cplayer.balance += 200
        elif val == 11:
            pos = self.board.player_positions[self.curr_player]
            if pos > 12 and pos < 28:
                self.jump_to_place(28)
            else:
                self.jump_to_place(12)
        elif val == 12:
            cplayer.balance += 150
        elif val == 13:
            self.jump_to_place(11, False)
        elif val == 14:
            self.jump_to_place(39, False)
        elif val == 15:
            jump_pos = ((self.board.
                player_positions[
                self.curr_player]+5)//10)*10 + 5
            self.jump_to_place(jump_pos, True)

    def check_strings(self, s):
        if (s == 'COMMUNITY_CHEST'):
            self.community_function()
        elif (s == 'INCOME_TAX'):
            self.get_rent(50)
            print('You paid income tax of $50!')
        elif (s == 'CHANCE'):
            self.chance_function()
        elif (s == 'GO_TO_JAIL'):
            self.go_to_jail()
            print('You have gone to jail!')
        elif (s == 'LUXURY_TAX'):
            self.get_rent(75)
            print('You paid luxury tax of $75!')
    
    def receive_salary(self):
        print('Congrtulations! You recieved a salary of $200.')
        self.board.players[self.curr_player].balance += 200
    
    def roll(self):
        if not self.roll_choice:
            return self.board.roll_dice_for_curr_player(self.curr_player)
        while True:
            try:
                roll_num = int(input('Enter value of dice rolled: '))
                return self.board.roll_dice_for_curr_player(
                    self.curr_player, roll_num)
            except:
                print('Please enter valid number.')
    
    
    def run_game(self):
        try:
            num_players = int(input('Number of players: ').strip())
        except:
            print('Ya dumb!')
            exit()
        for i in range(num_players):
            player_name = input('Name of player {}: '.format(i)).strip()
            self.board._add_player(player_name)
        
        self.num_rolls = 0

        self.clear_and_print()
        while (len(self.board.players) > 1):
            if (self.board.jail_players[self.board.players[self.curr_player].id]):
                if (self.board.players[self.curr_player].jail_cards):
                    check = input(
                        '{}\'s turn >> Do you want to use your get out of jail card? {}[y/n]{} '.format(
                        self.board.players[self.curr_player].name, bcolors.YELLOW, bcolors.ENDC
                    )).lower()
                    if (len(check) < 1):
                        continue
                    if (check[0] == 'y'):
                        self.board.players[self.curr_player].jail_cards -= 1
                        self.board.jail_players[self.board.players[self.curr_player].id] = 0
                        continue
                check = input(
                    '{}\'s turn >> Do you want to pay $50 to come out of jail? {}[y/n]{} '.format(
                    self.board.players[self.curr_player].name, bcolors.YELLOW, bcolors.ENDC
                )).lower()
                if (len(check) < 1):
                    continue
                if (check[0] == 'y'):
                    self.get_rent(50)
                    self.board.jail_players[self.board.players[self.curr_player].id] = 0
                    continue
                else:
                    self.board.jail_players[self.board.players[self.curr_player].id] -= 1
                    print('{} is in jail for {} more turns!'.format(
                        self.board.players[self.curr_player].name, 
                        self.board.jail_players[self.board.players[self.curr_player].id]))
                    self.curr_player = (self.curr_player + 1) % len(self.board.players)
                    self.num_rolls = 0
                    continue
            action = input('{}\'s turn {}>>{} '.format(
                self.board.players[self.curr_player].name, bcolors.YELLOW,
                bcolors.ENDC)).strip()

            if (action == 'end' or action == '11'):
                print('Bye!')
                break

            elif action == 'players' or action == '2':
                self.print_players()

            elif action == 'stats' or action == '3':
                self.print_players()
                try:
                    player_pos = int(
                        input('Which player\'s (enter number) cards do you want to see: ').strip())
                    player = self.board._get_player_using_id(player_pos)[1]
                    print(player.get_cards())
                except:
                    print('Invalid input! Try again.')
                    continue

            elif action == 'roll' or action == '1':
                if self.num_rolls:
                    print('You have already rolled once!')
                    continue
                self.num_rolls += 1
                salary = self.roll()
                print('You rolled a {}'.format(salary[0]))
                if (salary[1]):
                    self.receive_salary()
                forward_land = self.board.board[self.board.player_positions[self.curr_player]]
                if (isinstance(forward_land, str)):
                    print('You have landed on {}!'.format(
                        forward_land.replace('_', ' ')))
                    self.check_strings(forward_land)
                else:
                    print('You have landed on {}!'.format(
                        forward_land.name.replace('_', ' ')))
                    self.roll_action_card(forward_land, salary[0])

            elif action == 'done' or action == '8':
                if not self.num_rolls:
                    print('You haven\'t rolled yet!')
                    continue
                self.num_rolls = 0
                self.curr_player = (self.curr_player + 1) % len(self.board.players)
                self.clear_and_print()

            elif action == 'refresh' or action == '4':
                self.clear_and_print()

            elif action == 'build' or action == '5':
                print(self.board.players[self.curr_player].get_cards())
                try:
                    property_id = int(input('Input property ID number to raise money on: ').strip())
                except:
                    print('Invalid property ID number')
                    continue
                player_tmp = self.board.players[self.curr_player]
                tmp = player_tmp.build(property_id)
                if (tmp == 0):
                    print('You have successfully upgraded your property!')
                    print(str(self.board.board[property_id]))
                elif tmp == 5:
                    print('Property ID was not found in your cards.')
                elif tmp == 6:
                    print('This property cannot be upgraded.')
                elif tmp == 1:
                    print('Insufficient funds to upgrade property!')
                elif tmp == 2:
                    print('You do not have all the cards in the color set:(')
                elif tmp == 3:
                    print('A card in your color set is mortgaged. Cannot upgrade!')
                elif tmp == 4:
                    print('Inequal distribution of property! Try another card in this color set.')

            elif action == 'trade' or action == '6':
                try:
                    self.print_players()
                    player2_id = int(
    input('Input ID number of player you want to trade with? (Enter number): ').strip())
                    player2_pos, player2_tmp = self.board._get_player_using_id(player2_id)
                    if player2_pos == -1 or self.curr_player == player2_pos:
                        print('Invalid player ID. Try trade again:(')
                        continue
                    money_offer = int(input('Enter amount of money offered: $').strip())
                    money_request = int(input('Enter amount of money requested: $').strip())
                    player_tmp = self.board.players[self.curr_player]
                    if (player2_tmp.check_money(money_in = money_offer, money_out = money_request)):
                        print('Requested player does not have sufficient funds to make trade:(')
                        continue
                    if (player_tmp.check_money(money_in = money_request, money_out = money_offer)):
                        print('You do not have sufficient funds to make transaction:(')
                        continue
                    print('Your cards:')
                    print(player_tmp.get_cards())
                    card_offer_pos = input('Entry property ID of card you want to offer (or leave empty): ').strip()
                    if (len(card_offer_pos)):
                        card_offer = int(card_offer_pos)
                        check = player_tmp.check_trade(self.board.board[card_offer])
                        if (check == 2):
                            print('You do not own this property.')
                            continue
                        elif (check == 3):
                            print('You have upgraded property on this color set. Cannot sell!')
                            continue
                        elif check == 1:
                            print('You cannot trade this property:(')
                            continue
                        else:
                            print(repr(self.board.board[card_offer]))
                    print('Requested player\'s cards:')
                    print(player2_tmp.get_cards())
                    card_request_pos = input('Entry property ID of card you want to request (or leave empty): ').strip()
                    if (len(card_request_pos)):
                        card_request = int(card_request_pos)
                        check = player2_tmp.check_trade(self.board.board[card_request])
                        if (check == 2):
                            print('Requested player does not own this property.')
                            continue
                        elif (check == 3):
                            print('Requested player has upgraded property on this color set. Cannot sell!')
                            continue
                        elif check == 1:
                            print('You cannot trade this property:(')
                            continue
                        else:
                            print(repr(self.board.board[card_request]))
                    player2_tmp.trade_money(money_in = money_offer, money_out = money_request)
                    player_tmp.trade_money(money_in = money_request, money_out = money_offer)
                    if (len(card_offer_pos)):
                        player_tmp._remove_card(self.board.board[card_offer])
                        player2_tmp._buy_card_helper(self.board.board[card_offer])
                    if (len(card_request_pos)):
                        player2_tmp._remove_card(self.board.board[card_request])
                        player_tmp._buy_card_helper(self.board.board[card_request])
                    print('Trade Successful!')
                except ValueError:
                    print('Invalid entry. Try trade again:(')
                    continue
                except IndexError:
                    print('Property ID does not exist. Try trade again:(')
                    continue
                
            elif action == 'raise' or action == '7':
                print(self.board.players[self.curr_player].get_cards())
                try:
                    property_id = int(input('Input property ID number to raise money on: ').strip())
                except:
                    print('Invalid property ID number')
                    continue
                player_tmp = self.board.players[self.curr_player]
                bal_tmp = player_tmp.balance
                tmp = player_tmp.raise_money(property_id)
                if (tmp == 0):
                    print('${} was raised on the property!'.format(
                        player_tmp.balance - bal_tmp))
                    print(str(player_tmp))
                elif (tmp == 1):
                    print('Property ID was not found in your cards.')
                elif (tmp == 3):
                    print('Property is already mortgaged. No money can be raised.')

            elif action == 'demort' or action == '9':
                print(self.board.players[self.curr_player].get_cards())
                try:
                    property_id = int(input('Input property ID number to raise money on: ').strip())
                except:
                    print('Invalid property ID number')
                    continue
                player_tmp = self.board.players[self.curr_player]
                tmp = player_tmp.demortgage_card(property_id)
                if tmp == 0:
                    print('Property has been demortgaged!')
                elif tmp == 2:
                    print('Property ID was not found in your cards.')
                elif tmp == 1:
                    print('Insufficient funds to demortgage property:(')

            elif action == 'card' or action == '10':
                try:
                    property_id = int(input('Input property ID number to raise money on: ').strip())
                except:
                    print('Invalid property ID number')
                    continue
                if (property_id < len(self.board.board)) and (property_id > 0):
                    card = self.board.board[property_id]
                else:
                    print('Invalid ID:( Try again')
                    continue
                if (isinstance(card, str)):
                    print('{}{:^120}{}'.format(
                        bcolors.BOLD, card.replace('_', ' '), bcolors.ENDC))
                else:
                    print(repr(card))
            
            elif action == 'help' or action == '0':
                print('\t0/help    : Print all options')
                print('\t1/roll    : To roll the dice')
                print('\t2/players : Get all the players and their balances')
                print('\t3/stats   : To look at your and somebody else\'s cards')
                print('\t4/refresh : Clear and print the board again')
                print('\t5/build   : Build a house or hotel')
                print('\t6/trade   : Trade cards or money with another player.')
                print('\t7/raise   : Sell houses & hotels or mortgage properties to raise money')
                print('\t8/done    : Done with your turn')
                print('\t9/demort  : Demortgage card')
                print('\t10/card   : Get card statistics')
                print('\t11/end    : To end the game')
            else:
                print('Couldn\'t recognise input! Type \'help\' or \'0\' for more options.')
        else:
            print('Game Over!')
            print('{} wins the game! Congratulations!'.format(self.board.players[0].name))
            print('The final order after the winner:')
            for i in self.board.players_out:
                print('\t{}'.format(i.name))

while True:
    r_choice = input('Do you have dice to play with? {}[y/n]{} '.format(
        bcolors.YELLOW, bcolors.ENDC)).lower()
    if len(r_choice) < 1:
        continue
    if (r_choice[0] == 'y'):
        mo = monopoly(True)
    else:
        mo = monopoly(False)
    break
mo.run_game()        

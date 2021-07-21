# PLACE: 0
# UTILITY: 1
# STATION: 2
from Trade_Card import Trade_Card
from Station import Station
from Place import Place
from Player import Player
import random
from bcolors import bcolors
from collections import defaultdict

class Board:

    cc = {0: 'Life insurnace matures! Collect $100',
        1: 'Doctor\'s fee. Pay $50',
        2: 'Pay school tax of $150',
        3: 'XMAS fund matures! Collect $100',
        4: 'Go to Jail',
        5: 'From sale of stock you get $45',
        6: 'Collect $50 from every  player!',
        7: 'Street repairs. $40 per house, $115 per hotel',
        8: 'Income tax refund! Collect $20',
        9: 'Bank error in your favor! Collect $200',
        10: 'Get out of jail free card!',
        11: 'Beauty contest winner! Collect $10',
        12: 'You inherit $100',
        13: 'Advance to GO! Collect $200',
        14: 'Pay hospial $100',
        15: 'Receive for services $25'}
    
    chance = {0: 'Take a ride to the Chennai Central Railway Station', 
        1: 'Bank pays you dividend of $50', 
        2: 'Get out of jail free card!', 
        3: 'Repairs! Each house pay $25, hotel $100', 
        4: 'Pay poor tax of $15', 
        5: 'Advance to the nearest railroad! Double rent or buy', 
        6: 'Pay each player $50', 
        7: 'Go back 3 spaces', 
        8: 'Go to jail directly', 
        9: 'Advance to Jaipur', 
        10: 'Advance to Go!', 
        11: 'Advance to the neaerest utility', 
        12: 'Building loan matures! Collect $150', 
        13: 'Advance to Ludhiana!', 
        14: 'Advance to Mumbai', 
        15: 'Advance to nearest railroad and pay twice the rent'}
    
    def __init__(self):
        super().__init__()
        self.board = []
        self.players = [] 
        self.player_positions = [] 
        self.jail_players = {}
        self.players_out = []
        self.currentPlayer = -1
    
    def get_community_or_chance(self):
        return random.randint(0, 16)
    
    def _parse_board(self, filename = './boards/parse_board_indian.txt'):
        count = 0
        with open(filename, 'r') as f:
            while (True):
                line = f.readline()
                if not line:
                    break
                line_break = line.split(' ')
                if (len(line_break) == 1):
                    self.board.append(line.strip())
                elif (len(line_break) == 2):
                    self.board.append(Station(line_break[0], count))
                elif (len(line_break) == 3):
                    self.board.append(Trade_Card(
                        line_break[0], 150, 75, count))
                elif (len(line_break) == 11):
                    self.board.append(Place(line_break[0], 
                        int(line_break[2]), int(line_break[9]), count,
                        line_break[1], int(line_break[3]), 
                        [int(line_break[4]), int(line_break[5]), 
                        int(line_break[6]), int(line_break[7])], 
                        int(line_break[8]), int(line_break[10])))
                count += 1
            f.close()
        return

    def _add_player(self, name, position = 0, balance = 1500, jail_cards = 0):
        id = len(self.players)
        self.players.append(Player(name, id, balance, jail_cards))
        self.player_positions.append(position)
        self.jail_players[id] = 0
        return id
    
    def _remove_player(self, id):
        pos, player = self._get_player_using_id(id)
        if (pos == -1):
            return 1
        self.players.pop(pos)
        for key, val in player.cards.items():
            val.sold = False
            val.mortgaged = False
            val.player = -1
            val.hotels = 0
            val.houses = 0
        self.players_out.insert(0, player)
        return 0
    
    def bid_war(self, card):
        curr_bid = 1
        dead_alive_count = len(self.players)
        dead_alive = [True] * dead_alive_count
        curr_player = 0
        while (dead_alive_count > 1):
            print('Current bid: ${}'.format(curr_bid))
            if (self.players[curr_player].balance <= curr_bid):
                print('{} has insufficinet funds to make bid!'.format(
                    self.players[curr_player].name
                ))
                dead_alive[curr_player] = False
                dead_alive_count -= 1
            if (dead_alive[curr_player]):
                try:
                    player_bid = int(input('{}\'s (balance: {}) bid: '.format(
                        self.players[curr_player].name, 
                        self.players[curr_player].balance)))
                    if (player_bid > self.players[curr_player].balance):
                        print('Bid exceeded balance! Cannot bid again.')
                        dead_alive[curr_player] = False
                        dead_alive_count -= 1
                    elif (player_bid <= curr_bid):
                        print('Bid cannot be below current bid!')
                        continue
                    else:
                        curr_bid = player_bid
                except:
                    print('Invalid/exit bid! Cannot bid again.')
                    dead_alive[curr_player] = False
                    dead_alive_count -= 1
            curr_player = (curr_player + 1) % len(self.players)
            print('')
        curr_player = dead_alive.index(True)
        if self.players[curr_player].buy_card(card, purchase_price=curr_bid):
            print('Nobody won the bid. Card remains unsold!')
            return
        print('Winning bid by {} for ${}. Updated balance: ${}'.format(
            self.players[curr_player].name, curr_bid, 
            self.players[curr_player].balance
        ))
    
    def print_board(self):
        s = ""
        pos_dict = defaultdict(lambda:'')
        for i in range(len(self.players)):
            pos_dict[self.player_positions[i]] += str(self.players[i].id)
        
        for i in range(len(self.board)):
            if (isinstance(self.board[i], str)):
                tmp = self.board[i].replace('_', ' ')
                check = f'{bcolors.WHITE}{tmp}{bcolors.ENDC}'
            else:
                check = str(self.board[i]).replace('_', ' ')
            if (i%2==0):
                s += '\t\t{:^6} {:02d}. {:50}'.format(pos_dict[i], i, check)
            else: 
                s += '\t{:^6} {:02d}. {:50} '.format(pos_dict[i], i, check) + '\n'
            if ((i-9) % 10 == 0):
                s += '\n'
        return s[:-1]
    
    @classmethod
    def roll_dice(cls):
        return random.randint(0, 6)
    
    def roll_dice_for_curr_player(self, pos, forward = 0):
        if (forward > 0):
            # if (forward < 2 or forward > 12):
            #     return 1
            pass
        else:
            forward = Board.roll_dice() + Board.roll_dice()
        curr_pos = self.player_positions[pos]
        self.player_positions[pos] = (curr_pos + forward) % len(self.board)
        return forward, self.player_positions[pos] < curr_pos

    def _get_player_using_id(self, id:int):
        count = 0
        for i in self.players:
            if i.id == id:
                return count, i
            count += 1
        return -1, None
    
    def get_balances(self):
        s = ''
        for i in self.players:
            s += str(i) + ', '
        return s[:-2]
    
    def print_chance_community(self, s):
        curtains = '=' * 100
        s = '{:^120}\n\n{:^120}\n\n{:^120}'.format(curtains, s, curtains)
        return s

    

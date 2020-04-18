from random import sample

class PlayBlackJack:
    """ Blackjack game console """
    
    
    def __init__(self):

        self.setup()
        self.game_starts()
        
        
    def setup(self):
        """ Setup the game and deals the first cards """
        
        print("-------------------- Setup Game --------------------")
        
        # Players number
        players_number = input("How many players ? (max 3) : ")
        while players_number not in ["1","2","3"]:
            players_number = input("How many players ? (please give a number between 1 and 3) : ")
        self.players_number = players_number
        
        # Players name + players dict created + dealer dict
        players_name = []
        players = dict()
        
        for i in range(int(players_number)):
            name = input("Player's {} name : ".format(i+1))
            name = name.replace(" ", "")
            name = name.replace("_", "")
            name = name[:9]
            if (name in players_name) | (name == "") | (name == "Dealer"):
                name = name + "_" + str(i+1)
                print("Your name is saved as : {}".format(name))
            players_name.append(name)
            players[name] = dict()
            players[name]["name"] = name
            players[name]["money"] = 0
        
        self.players_name = players_name
        self.players = players
        self.dealer = dict()
        self.dealer["name"] = "Dealer"
            
    
    @staticmethod
    def points_calculation(player):
        """ Calculate players and dealer points """
        
        hand = [card[0] for card in player["cards"]]
        
        # Convert heads to 10
        total_ace = 0
        for i in range(len(hand)):
            if hand[i] in ["K","Q","J","T"]:
                hand[i] = 10
            elif hand[i] != "A":
                hand[i] = int(hand[i])
            else:
                total_ace = total_ace + 1
        
        # Total if no aces
        if total_ace == 0:
            return sum(hand)
        
        # Hand value without aces
        hand_tot = 0
        for card in hand:
            if card != "A":
                hand_tot = hand_tot + card
        
        # Total if aces
        if hand_tot + total_ace > 21:
            return hand_tot + total_ace
        
        hand_tot = hand_tot + total_ace*11
        while hand_tot > 21:
            hand_tot = hand_tot - 10
        return hand_tot
                
    
    def print_hand(self, player):
        """ Print a player's hand and his points """
        
        print("{}'s hand : {}.".format(player["name"], ", ".join(player["cards"])))
        print("{}'s points : {}".format(player["name"], self.points_calculation(player)))

    
    def game_starts(self):
        """ The beginning of the game """
         
        print("-------------------- Game Starts --------------------")
        
        # cards initialization
        signs = [" of Club", " of Spade", " of Heart", " of Diamond"]
        numbers = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
        cards = [number + sign for number in numbers for sign in signs]
        self.cards = sample(cards, 52)
        
        # players and dealer initialization
        for player in self.players_name:
            print("{} money : {}".format(player, self.players[player]["money"]))
            self.players[player]["cards"] = self.cards[:2]
            self.cards = self.cards[2:]
            self.players[player]["points"] = 0
            self.players[player]["BJ"] = False
            self.players[player]["insurance"] = False
            self.players[player]["double"] = False
            self.players[player]["split"] = False
        
        self.dealer["cards"] = []
        self.dealer["cards"] = [self.cards.pop(0)]
        self.hidden_card = self.cards.pop(0)
        self.dealer["points"] = 0
        self.dealer["BJ"] = False
        
        self.main()
            
        
    def main(self):
        """ Game from the start of first player turn to the end of the dealer turn """
        
        # Players turns
        for player in self.players_name:
            
            self.players[player]["points"] = self.points_calculation(self.players[player])
            # Blackjack case
            if self.players[player]["points"] == 21:
                self.print_hand(self.players[player])
                self.players[player]["BJ"] = True
                print("Blackjack for {} !".format(player))
            
            # Other cases
            else:
                
                self.print_hand(self.dealer)
                self.print_hand(self.players[player])
                # double case
                if self.ask_for_double(player) is True:
                    continue
                
                while True:
                    self.print_hand(self.dealer)
                    self.print_hand(self.players[player])
                                        
                    # Ask for card
                    want_card = input("{} do you want a card ? (y/n) : ".format(player))
                    while want_card not in ["y","n"]:
                        want_card = input("Please {}, do you want a card ? (y/n) : ".format(player))
                    
                    if want_card == "n":
                        break
                    else:
                        self.players[player]["cards"].append(self.cards.pop(0))
                        self.players[player]["points"] = self.points_calculation(self.players[player])
                        if self.players[player]["points"] == 21:
                            self.print_hand(self.players[player])
                            break
                        elif self.players[player]["points"] > 21:
                            self.print_hand(self.players[player])
                            print("{} lost.".format(player))
                            break
                        
        # Dealer turn
        self.dealer["cards"].append(self.hidden_card)
        self.dealer["points"] = self.points_calculation(self.dealer)
        print("Dealer turn his card !")
        self.print_hand(self.dealer)
        
        if self.dealer["points"] == 21:
            self.dealer["BJ"] = True
            print("Blackjack from the dealer, end of the game !")
        else:
            while self.dealer["points"] < 17:
                print("Dealer draw a card !")
                self.dealer["cards"].append(self.cards.pop(0))
                self.dealer["points"] = self.points_calculation(self.dealer)
                self.print_hand(self.dealer)
            print("Dealer has {} points, end of the game !".format(self.dealer["points"]))
        
        print("-------------------- End of the Game --------------------")
        self.give_results()
        self.ask_for_new_game()
        
        
    def ask_for_double(self, player):
        """ The double case """
        
        question = input("{} do you want to double ? (y/n) : ".format(player))
        while question not in ["y","n"]:
            question = input("Please {}, do you want a card ? (y/n) : ".format(player))
        
        if question == "y":
            self.players[player]["double"] = True
            self.players[player]["cards"].append(self.cards.pop(0))
            self.players[player]["points"] = self.points_calculation(self.players[player])
            self.print_hand(self.players[player])
            return True
        return False
        
    
    def give_results(self):
        """ List the results """
        
        print("-------------------- Results --------------------")
        
        for player in self.players_name:
            
            # Game bet
            if self.players[player]["double"] == True:
                game_bet = 2
            else:
                game_bet = 1
            
            # BJ case
            if self.players[player]["BJ"] == True:
                if self.dealer["BJ"] == True:
                    print("Draw for {}.".format(player))
                else:
                    print("{} wins.".format(player))
                    self.players[player]["money"] = self.players[player]["money"] + game_bet
                    
            # Other cases
            else:
                # more than 21 points
                if self.players[player]["points"] > 21:
                    print("{} loses.".format(player))
                    self.players[player]["money"] = self.players[player]["money"] - game_bet
                # 21 points or less
                else:
                    # dealer BJ
                    if self.dealer["BJ"] == True:
                        print("{} loses.".format(player))
                        self.players[player]["money"] = self.players[player]["money"] - game_bet
                    # other cases
                    else:
                        if self.dealer["points"] > 21:
                            print("{} wins.".format(player))
                            self.players[player]["money"] = self.players[player]["money"] + game_bet
                        elif self.players[player]["points"] > self.dealer["points"]:
                            print("{} wins.".format(player))
                            self.players[player]["money"] = self.players[player]["money"] + game_bet
                        elif self.players[player]["points"] < self.dealer["points"]:
                            print("{} loses.".format(player))
                            self.players[player]["money"] = self.players[player]["money"] - game_bet
                        else:
                            print("Draw for {}.".format(player))
            

    def ask_for_new_game(self):
        """ Ask for a new game """
        
        question = input("New game ? (y/n) : ")
        while question not in ["y","n"]:
            question = input("New game ? (y/n) : ")       
        
        if question == "y":
            self.game_starts()
        
        else:
            for player in self.players_name:
                print("{} money : {}".format(player, self.players[player]["money"]))
                
        return
        

if __name__ == "__main__":
    game = PlayBlackJack()

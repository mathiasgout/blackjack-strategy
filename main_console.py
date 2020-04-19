from random import sample

class PlayBlackJack:
    """ Blackjack game console """
    
    
    def __init__(self):
        
        print("\n")
        self.setup()
        self.game_starts()
        
        
    def setup(self):
        """ Setup the game and deals the first cards """

        print("-------------------- Setup Game --------------------\n")
        
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
    def points_calculation(player, opt=0):
        """ 
        Calculate players points
        opt = 0 for player["cards"]
        opt = 1 for player["cards_1"]
        opt = 2 for player["cards_2"]
        """
        
        if opt == 2:
            hand = [card[0] for card in player["cards_2"]]
        elif opt == 1:
            hand = [card[0] for card in player["cards_1"]]
        else:
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
                
    
    def print_hand(self, player, opt=0):
        """ 
        Print a player's hand and his points
        opt = 0 for player["cards"]
        opt = 1 for player["cards_1"]
        opt = 2 for player["cards_2"]
        """
        
        if opt == 2:
            print("{}'s hand : {}.".format(player["name"] + "-second-split", ", ".join(player["cards_2"])))
            print("{}'s points : {}".format(player["name"] + "-second-split", self.points_calculation(player, opt=2)))
        elif opt == 1:
            print("{}'s hand : {}.".format(player["name"] + "-first-split", ", ".join(player["cards_1"])))
            print("{}'s points : {}".format(player["name"] + "-first-split", self.points_calculation(player, opt=1)))
        else:
            print("{}'s hand : {}.".format(player["name"], ", ".join(player["cards"])))
            print("{}'s points : {}".format(player["name"], self.points_calculation(player)))
    
    
    def game_starts(self):
        """ The beginning of the game """
        
        print("\n")
        print("-------------------- GAME STARTS --------------------\n")
        
        # cards initialization
        signs = [" of Club", " of Spade", " of Heart", " of Diamond"]
        values = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
        cards = [value + sign for value in values for sign in signs]
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
            self.players[player]["points_1"] = 0
            self.players[player]["points_2"] = 0
            self.players[player]["cards_1"] = []
            self.players[player]["cards_2"] = []
            self.players[player]["double_1"] = False
            self.players[player]["double_2"] = False
        
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
            print("\n")
            self.print_hand(self.dealer)
            print("\n")
            self.print_hand(self.players[player])
            
            # Insurance
            if self.dealer["cards"][0][0] == "A":
                want_insurance = input("Dealer's first card is an Ace, do you want an insurance {} ? (y/n) : ".format(player))
                while want_insurance not in ["y","n"]:
                    want_insurance = input("Please {}, do you want an insurance ? (y/n) : ".format(player))
                if want_insurance == "y":
                    self.players[player]["insurance"] = True
                    
            # Split case
            if self.ask_for_split(self.players[player]) is True:
                continue
                
            # Blackjack case
            if self.players[player]["points"] == 21:
                self.players[player]["BJ"] = True
                print("Blackjack for {} !".format(player))
            
            # Other cases
            else:
                # double case
                if self.ask_for_double(self.players[player]) is True:
                    continue
                
                while True:
                                        
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
                            print("\n")
                            self.print_hand(self.players[player])
                            break
                        elif self.players[player]["points"] > 21:
                            print("\n")
                            self.print_hand(self.players[player])
                            print("{} lost.".format(player))
                            break
                    print("\n")
                    self.print_hand(self.dealer)
                    print("\n")
                    self.print_hand(self.players[player])
                        
        # Dealer turn
        print("\n")
        print("-------------------- Dealer's Turn --------------------")
        self.dealer["cards"].append(self.hidden_card)
        self.dealer["points"] = self.points_calculation(self.dealer)
        print("\nDealer turn his card !")
        print("\n")
        self.print_hand(self.dealer)
        
        if self.dealer["points"] == 21:
            self.dealer["BJ"] = True
            print("Blackjack from the dealer, end of the game !")
        else:
            while self.dealer["points"] < 17:
                print("\n")
                print("Dealer draw a card !")
                self.dealer["cards"].append(self.cards.pop(0))
                self.dealer["points"] = self.points_calculation(self.dealer)
                print("\n")
                self.print_hand(self.dealer)
            print("\n")
            print("Dealer has {} points, end of the game !".format(self.dealer["points"]))
        
        self.give_results()
        self.ask_for_new_game()
        
        
    def ask_for_double(self, player, opt=0):
        """ 
        The double case
        opt = 0 for player["cards"]
        opt = 1 for player["cards_1"]
        opt = 2 for player["cards_2"]
        """
        
        if opt == 2:
            question = input("{} do you want to double ? (y/n) : ".format(player["name"] + "-second-split"))
            while question not in ["y","n"]:
                question = input("Please {}, do you want to double ? (y/n) : ".format(player["name"] + "-second-split"))
            
            if question == "y":
                player["double_2"] = True
                player["cards_2"].append(self.cards.pop(0))
                player["points_2"] = self.points_calculation(player, opt=2)
                print("\n")
                self.print_hand(player, opt=2)
                if player["points_1"] > 21:
                    print("{} lost.".format(player["name"] + "-second-split"))
                return True
            return False
        
        elif opt == 1:
            question = input("{} do you want to double ? (y/n) : ".format(player["name"] + "-first-split"))
            while question not in ["y","n"]:
                question = input("Please {}, do you want to double ? (y/n) : ".format(player["name"] + "-first-split"))
            
            if question == "y":
                player["double_1"] = True
                player["cards_1"].append(self.cards.pop(0))
                player["points_1"] = self.points_calculation(player, opt=1)
                print("\n")
                self.print_hand(player, opt=1)
                if player["points_1"] > 21:
                    print("{} lost.".format(player["name"] + "-first-split"))
                return True
            return False
        
        else:
            question = input("{} do you want to double ? (y/n) : ".format(player["name"]))
            while question not in ["y","n"]:
                question = input("Please {}, do you want to double ? (y/n) : ".format(player["name"]))
            
            if question == "y":
                player["double"] = True
                player["cards"].append(self.cards.pop(0))
                player["points"] = self.points_calculation(player)
                print("\n")
                self.print_hand(player)
                if player["points"] > 21:
                    print("{} lost.".format(player["name"]))
                return True
            return False    
    
    
    def ask_for_split(self, player):
        """ The split case """
        
        # check if you can split
        hand = [card[0] for card in player["cards"]]

        for i in range(2):
            if hand[i] in ["K","Q","J","T"]:
                hand[i] = 10
            elif hand[i] == "A":
                hand[i] = 11
            else:
                hand[i] = int(hand[i])
        
        # can not split
        if hand[0] != hand[1]:
            return False
        
        # can split
        else:
            question = input("{} do you want to split ? (y/n) : ".format(player["name"]))
            while question not in ["y","n"]:
                question = input("Please {}, do you want to split ? (y/n) : ".format(player["name"]))
            
            # do not want to split
            if question == "n":
                return False
            # want to split
            else:
                player["split"] = True
                player["cards_1"].append(player["cards"][0])
                player["cards_2"].append(player["cards"][1])
                player["points_1"] = self.points_calculation(player, opt=1)
                player["points_2"] = self.points_calculation(player, opt=2)
                
                for i,word in enumerate(["first","second"]):
                    print("\n")
                    self.print_hand(self.dealer)
                    print("\n")
                    self.print_hand(player, opt=i+1)
                    # double case
                    if self.ask_for_double(player, opt=i+1) is True:
                        continue
                    
                    while True:
                                            
                        # Ask for card
                        want_card = input("{}-{} do you want a card ? (y/n) : ".format(player["name"], word + "-split"))
                        while want_card not in ["y","n"]:
                            want_card = input("Please {}-{}, do you want a card ? (y/n) : ".format(player["name"], word + "-split"))
                        
                        if want_card == "n":
                            break
                        else:
                            player["cards_{}".format(i+1)].append(self.cards.pop(0))
                            player["points_{}".format(i+1)] = self.points_calculation(player, opt=i+1)
                            if player["points_{}".format(i+1)] == 21:
                                print("\n")
                                self.print_hand(player, opt=i+1)
                                break
                            elif player["points_{}".format(i+1)] > 21:
                                print("\n")
                                self.print_hand(player, opt=i+1)
                                print("{}-{} lost.".format(player["name"], word + "-split"))
                                break
                        print("\n")
                        self.print_hand(self.dealer)
                        print("\n")
                        self.print_hand(player, opt=i+1)
                            
                return True
        
    
    def give_results(self):
        """ List the results """
        
        print("\n")
        print("-------------------- Results --------------------\n")
        
        for player in self.players_name:
            
            # Insurance case
            if self.players[player]["insurance"] == True:
                if self.dealer["BJ"] == True:
                    self.players[player]["money"] = self.players[player]["money"] + 1.5
                else:
                    self.players[player]["money"] = self.players[player]["money"] - 0.5
            
            # Split case
            if self.players[player]["split"] == True:
                
                for i,word in enumerate(["first","second"]):
                    # Split bet
                    if self.players[player]["double_{}".format(i+1)] == True:
                        game_bet = 2
                    else:
                        game_bet = 1
                        
                    # more than 21 points
                    if self.players[player]["points_{}".format(i+1)] > 21:
                        print("{}-{} lost.".format(player, word + "-split"))
                        self.players[player]["money"] = self.players[player]["money"] - game_bet
                    # 21 points or less
                    else:
                        # dealer BJ
                        if self.dealer["BJ"] == True:
                            print("{}-{} lost.".format(player, word + "-split"))
                            self.players[player]["money"] = self.players[player]["money"] - game_bet
                        # other cases
                        else:
                            if self.dealer["points"] > 21:
                                print("{}-{} wins.".format(player, word + "-split"))
                                self.players[player]["money"] = self.players[player]["money"] + game_bet
                            elif self.players[player]["points_{}".format(i+1)] > self.dealer["points"]:
                                print("{}-{} wins.".format(player, word + "-split"))
                                self.players[player]["money"] = self.players[player]["money"] + game_bet
                            elif self.players[player]["points_{}".format(i+1)] < self.dealer["points"]:
                                print("{}-{} lost.".format(player, word + "-split"))
                                self.players[player]["money"] = self.players[player]["money"] - game_bet
                            else:
                                print("Draw for {}-{}.".format(player, word + "-split"))
                continue
                    
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
    
        print("\n-------------------- END OF THE GAME --------------------")
        print("\n")
        question = input("New game ? (y/n) : ")
        while question not in ["y","n"]:
            question = input("New game ? (y/n) : ")       
        
        if question == "y":
            self.game_starts()
        
        else:
            print("\n")
            print("-------------------- Final results --------------------\n")
            for player in self.players_name:
                print("{} final money : {}".format(player, self.players[player]["money"]))
                
        

if __name__ == "__main__":
    game = PlayBlackJack()
    # game.players["_1"]["cards"] = ["T","J"]
    # game.players["_1"]["cards_1"] = []
    # game.players["_1"]["cards_2"] = []
    # game.players["_1"]["points_1"] = 0
    # game.players["_1"]["points_2"] = 0    
    # game.players["_1"]["money"] = 0
    # game.players["_2"]["cards"] = ["8","9"]
    # game.players["_2"]["money"] = 0
    # game.dealer["cards"] = ["9"]
    # game.dealer["points"] = 9
    
    

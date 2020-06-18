from random import sample


class StrategyMC:
    """ Find the best strategy with a MC method """
    
    def __init__(self, dealer_card, player_cards, n_iter=10000, insurance=False, split=False,
                 double=False, max_point=18, num_cards=None):
        """
        Example :
        strategy = StrategyMC(dealer_card="8", player_cards=["T", "9"], n_iter=100000, num_cards=0)
        print(strategy.results)

        dealer_card = a card
        player_cards = a list of 2 cards
        n_iter = int
        insurance = bool
        split = bool
        double = bool
        max_point = int
        nums_card = int (the number of cards you want to hit) or None if you want to use max_point
        """
        self.player = dict()
        self.player["money"] = 0
        self.dealer = dict()
        self.n_iter = n_iter
        self.dealer_card = dealer_card
        self.player_cards = player_cards
        self.insurance = insurance
        self.split = split
        self.double = double
        self.max_point = max_point
        self.num_cards = num_cards
        self.results = dict()

        self.game_starts()
    
    # the count
    N = 0

    def game_starts(self):
        """ Game initialization + main + results"""
        
        while self.N < self.n_iter:
            
            # cards initialization
            self.player["cards"] = self.player_cards[:]
            self.dealer["cards"] = [self.dealer_card]
            self.cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"] * 4
            self.cards.remove(self.player["cards"][0])
            self.cards.remove(self.player["cards"][1])
            self.cards.remove(self.dealer["cards"][0])
            self.cards = sample(self.cards, len(self.cards)-3)
            
            # player and dealer initialization
            self.player["points"] = self.points_calculation(self.player)
            self.player["BJ"] = False
            self.player["points_1"] = 0
            self.player["points_2"] = 0
            self.player["cards_1"] = []
            self.player["cards_2"] = []
                       
            self.hidden_card = self.cards.pop(0)
            self.dealer["points"] = 0
            self.dealer["BJ"] = False

            " Game main "
            # player turn
            # split case
            if self.split is True:
                self.split_case()

            # BJ case
            elif self.player["points"] == 21:
                self.player["BJ"] = True
            
            # Other cases
            else:
                # double case
                if self.double is True:
                    self.double_case()
                # no double case
                else:
                    if self.num_cards is None:
                        while self.player["points"] < self.max_point:
                            self.player["cards"].append(self.cards.pop(0))
                            self.player["points"] = self.points_calculation(self.player)
                    else:
                        count = 0
                        while count < self.num_cards:
                            self.player["cards"].append(self.cards.pop(0))
                            self.player["points"] = self.points_calculation(self.player)
                            count = count + 1
                            
            # dealer turn
            self.dealer["cards"].append(self.hidden_card)
            self.dealer["points"] = self.points_calculation(self.dealer)
            
            if self.dealer["points"] == 21:
                self.dealer["BJ"] = True
            else:
                while self.dealer["points"] < 17:
                    self.dealer["cards"].append(self.cards.pop(0))
                    self.dealer["points"] = self.points_calculation(self.dealer)

            """ List the results """
            # Insurance case
            if self.insurance is True:
                if self.dealer["BJ"] is True:
                    self.player["money"] = self.player["money"] + 1
                else:
                    self.player["money"] = self.player["money"] - 0.5
                    
            # Split case
            if self.split is True:
                # Game bet
                if self.double is True:
                    game_bet = 2
                else:
                    game_bet = 1
                for i in range(1, 3):
                    if self.player["points_{}".format(i)] > 21:
                        self.player["money"] = self.player["money"] - game_bet
                    else:
                        if self.dealer["points"] > 21:
                            self.player["money"] = self.player["money"] + game_bet
                        elif self.player["points_{}".format(i)] > self.dealer["points"]:
                            self.player["money"] = self.player["money"] + game_bet
                        elif self.player["points_{}".format(i)] < self.dealer["points"]:
                            self.player["money"] = self.player["money"] - game_bet
            
            # Other cases
            else:
                # Game bet
                if self.double is True:
                    game_bet = 2
                else:
                    game_bet = 1
                
                # BJ case
                if self.player["BJ"]:
                    if self.dealer["BJ"] is False:
                        self.player["money"] = self.player["money"] + game_bet
                # Other cases
                else:
                    # more than 21 points
                    if self.player["points"] > 21:
                        self.player["money"] = self.player["money"] - game_bet
                    # 21 points or less
                    else:
                        if self.dealer["points"] > 21:
                            self.player["money"] = self.player["money"] + game_bet
                        elif self.player["points"] > self.dealer["points"]:
                            self.player["money"] = self.player["money"] + game_bet
                        elif self.player["points"] < self.dealer["points"]:
                            self.player["money"] = self.player["money"] - game_bet
        
            self.N = self.N + 1
            
        else:
            self.results["profit"] = self.player["money"]
            self.results["mean_profit"] = self.player["money"]/self.N
            self.results["win_rate"] = (self.results["mean_profit"] + 1)/2
            if self.double is True and self.split is True:
                self.results["win_rate"] = (self.results["mean_profit"] + 4)/8
            elif self.double is True or self.split is True:
                self.results["win_rate"] = (self.results["mean_profit"] + 2)/4
            return 

    def double_case(self, opt=0):
        """ 
        The double case
        opt = 0 for player["cards"]
        opt = 1 for player["cards_1"]
        opt = 2 for player["cards_2"]
        """
        
        if opt == 2: 
            self.player["cards_2"].append(self.cards.pop(0))
            self.player["points_2"] = self.points_calculation(self.player, opt=2)
        
        elif opt == 1:
            self.player["cards_1"].append(self.cards.pop(0))
            self.player["points_1"] = self.points_calculation(self.player, opt=1)
        
        else: 
            self.player["cards"].append(self.cards.pop(0))
            self.player["points"] = self.points_calculation(self.player)

    def split_case(self):
        """ The split case """
        
        self.player["cards_1"].append(self.player["cards"][0])
        self.player["cards_2"].append(self.player["cards"][1])
        self.player["points_1"] = self.points_calculation(self.player, opt=1)
        self.player["points_2"] = self.points_calculation(self.player, opt=2)
       
        if self.double is True:
            self.double_case(opt=1)
            self.double_case(opt=2)
            
        else:
            if self.num_cards is None:
                for i in range(1, 3):
                    while self.player["points_{}".format(i)] < self.max_point:
                        self.player["cards_{}".format(i)].append(self.cards.pop(0))
                        self.player["points_{}".format(i)] = self.points_calculation(self.player, opt=i)
            else:
                for i in range(1, 3):
                    count = 0
                    while count < self.num_cards:
                        self.player["cards_{}".format(i)].append(self.cards.pop(0))
                        self.player["points_{}".format(i)] = self.points_calculation(self.player, opt=i)
                        count = count + 1

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
            if hand[i] in ["K", "Q", "J", "T"]:
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

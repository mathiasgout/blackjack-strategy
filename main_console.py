from random import sample

class PlayBlackJack:
    """ Blackjack game console """
    
    
    def __init__(self):
        signs = [" of Club", " of Spade", " of Heart", " of Diamond"]
        numbers = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
        cards = [number + sign for number in numbers for sign in signs]
        self.cards = sample(cards, 52)
        
        print("-------------------- Setup Game --------------------")
        self.setup()
    
        print("-------------------- Game Starts --------------------")
        
        
    def setup(self):
        """ Setup the game """
        
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
            if (name in players_name) | (name == ""):
                name = name + "_" + str(i+1)
                print("Your name is saved as : {}".format(name))
            players_name.append(name)
            players[name] = dict()
        
        self.players_name = players_name
        self.players = players
        self.dealer = dict()
        
        
    


if __name__ == "__main__":
    game = PlayBlackJack()
    game

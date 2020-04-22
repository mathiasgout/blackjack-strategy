from strategy import StrategyMC
import pandas as pd

class BuildBestStrategy:
    """ Build the best strategy depending of the cases """
    
    CARDS_DEALER = ["A","T","9","8","7","6","5","4","3","2"]
    CARDS_PLAYER_SOFT = CARDS_DEALER
    CARDS_PLAYER = ["T","9","8","7","6","5","4","3","2"]    
    
    @staticmethod
    def count_points(cards):
        """ Count player starting hand points """
        
        count = 0
        for card in cards:
            if card == "T":
                count = count + 10
            elif card == "A":
                count = count + 11
            else:
                count = count + int(card)
        
        return count 
                
        
    def HardCases(self, n_iter=10000):
        """ Build the best strategy with hard cases """
                    
        DF = pd.DataFrame(columns=["dealer_cards","player_cards","points","mean_profit_stand", "mean_profit_hit", "mean_profit_double"])
                
        for i in range(len(self.CARDS_PLAYER)-1):
            for j in range(i+1, len(self.CARDS_PLAYER)):
                
                result_dict = dict()
                result_dict["dealer_cards"] = []
                result_dict["player_cards"] = []
                result_dict["points"] = []
                result_dict["mean_profit_stand"] = []
                result_dict["mean_profit_hit"] = []
                result_dict["mean_profit_double"] = []
                result_dict["n_iter"] = []
                
                for card in self.CARDS_DEALER:
                    
                    strat_stand = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]], max_point=0, n_iter=n_iter)
                    strat_double = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]], double=True, n_iter=n_iter)
                    strat_hit = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]], max_point=self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]])+1, n_iter=n_iter)

                    result_dict["mean_profit_stand"].append(strat_stand.results["mean_profit"])
                    result_dict["mean_profit_hit"].append(strat_hit.results["mean_profit"])
                    result_dict["mean_profit_double"].append(strat_double.results["mean_profit"])
                    result_dict["dealer_cards"].append(card)
                    result_dict["player_cards"].append([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]])
                    result_dict["points"].append(self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]]))
                    result_dict["n_iter"].append(n_iter)
                    
                DF = pd.concat([DF, pd.DataFrame(result_dict)], ignore_index=True)
                
        return DF
            
    
if __name__ == "__main__":
    strategy = BuildBestStrategy()
    df = strategy.HardCases()
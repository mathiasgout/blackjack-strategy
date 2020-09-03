import pandas as pd
from strategy import StrategyMC
import pandas as pd


class BuildBestStrategy:
    """ Build the best strategy depending of the cases """
    
    CARDS_DEALER = ["A", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    CARDS_PLAYER = CARDS_DEALER  
    
    @staticmethod
    def count_points(cards, opt=0):
        """ Count player-starting-hand points 
        opt = 0, A = 1
        opt = 1, A = 11
        """
        
        if cards == ["A", "A"]:
            return 12
                
        count = 0
        for card in cards:
            if card == "T":
                count = count + 10
            elif card == "A" and opt == 0:
                count = count + 1
            elif card == "A" and opt == 1:
                count = count + 11
            else:
                count = count + int(card)
        
        return count 

    def normal_cases(self, n_iter=10000):
        """ Build the best strategy with hard and soft cases """
                    
        df = pd.DataFrame(columns=["dealer_cards", "player_cards", "points", "mean_profit_stand",
                                   "mean_profit_hit", "mean_profit_double", "n_iter"])

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
                   
                    strat_stand = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                             max_point=0, n_iter=n_iter)
                    
                    # blackjack cases
                    if self.CARDS_PLAYER[i] == "A" and self.CARDS_PLAYER[j] == "T":
                        result_dict["mean_profit_hit"].append(pd.NA)
                        result_dict["mean_profit_double"].append(pd.NA)
                    else: 
                        # more than 11 points -> draw only 1 card
                        if self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]], opt=1) > 11:
                            strat_hit = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                                   num_cards=1, n_iter=n_iter)
                        # less than 12 points -> draw card until 12 points
                        else:
                            strat_hit = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                                   max_point=12, n_iter=n_iter)
                       
                        strat_double = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                                  double=True, n_iter=n_iter)
                        result_dict["mean_profit_hit"].append(strat_hit.results["mean_profit"])
                        result_dict["mean_profit_double"].append(strat_double.results["mean_profit"])

                    result_dict["mean_profit_stand"].append(strat_stand.results["mean_profit"])
                    result_dict["dealer_cards"].append(card)
                    result_dict["player_cards"].append([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]])
                    result_dict["points"].append(self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                                                   opt=1))
                    result_dict["n_iter"].append(n_iter)
                    
                df = pd.concat([df, pd.DataFrame(result_dict)], ignore_index=True)
                
        return df

    def split_cases(self, n_iter=10000):
        """ Build the best strategy with split cases """
                    
        df = pd.DataFrame(columns=["dealer_cards", "player_cards", "points", "mean_profit_stand",
                                   "mean_profit_hit", "mean_profit_double", "mean_profit_split",
                                   "mean_profit_split_double", "n_iter"])
                
        for i in range(len(self.CARDS_PLAYER)):

            result_dict = dict()
            result_dict["dealer_cards"] = []
            result_dict["player_cards"] = []
            result_dict["points"] = []
            result_dict["mean_profit_stand"] = []
            result_dict["mean_profit_hit"] = []
            result_dict["mean_profit_double"] = []
            result_dict["mean_profit_split"] = []
            result_dict["mean_profit_split_double"] = []
            result_dict["n_iter"] = []

            for card in self.CARDS_DEALER:

                strat_stand = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                         max_point=0, n_iter=n_iter)
                strat_double = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                          double=True, n_iter=n_iter)
                strat_split = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                         max_point=12, split=True, n_iter=n_iter)
                strat_split_double = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                                double=True, split=True, n_iter=n_iter)

                # more than 11 points -> draw only 1 card
                if self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]], opt=1) > 11:
                    strat_hit = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                           num_cards=1, n_iter=n_iter)
                # less than 12 points -> draw card until 12 points
                else:
                    strat_hit = StrategyMC(card, [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                           max_point=12, n_iter=n_iter)

                result_dict["mean_profit_stand"].append(strat_stand.results["mean_profit"])
                result_dict["mean_profit_hit"].append(strat_hit.results["mean_profit"])
                result_dict["mean_profit_double"].append(strat_double.results["mean_profit"])
                result_dict["mean_profit_split"].append(strat_split.results["mean_profit"])
                result_dict["mean_profit_split_double"].append(strat_split_double.results["mean_profit"])
                result_dict["dealer_cards"].append(card)
                result_dict["player_cards"].append([self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]])
                result_dict["points"].append(self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]], opt=1))
                result_dict["n_iter"].append(n_iter)

            df = pd.concat([df, pd.DataFrame(result_dict)], ignore_index=True)
                
        return df

    def insurance_cases(self, n_iter=10000):
        """ Build the best strategy with insurances cases """
                    
        df = pd.DataFrame(columns=["dealer_cards", "player_cards", "points", "mean_profit_stand",
                                   "mean_profit_hit", "mean_profit_double", "insurance", "n_iter"])
        
        for i in range(len(self.CARDS_PLAYER)-1):
            for j in range(i+1, len(self.CARDS_PLAYER)):
                
                result_dict = dict()
                result_dict["dealer_cards"] = []
                result_dict["player_cards"] = []
                result_dict["points"] = []
                result_dict["mean_profit_stand"] = []
                result_dict["mean_profit_hit"] = []
                result_dict["mean_profit_double"] = []
                result_dict["insurance"] = []
                result_dict["n_iter"] = []
                
                strat_stand = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                         max_point=0, n_iter=n_iter)
                
                # blackjack cases
                if self.CARDS_PLAYER[i] == "A" and self.CARDS_PLAYER[j] == "T":
                    result_dict["mean_profit_hit"].append(pd.NA)
                    result_dict["mean_profit_double"].append(pd.NA)
                else: 
                    # more than 11 points -> draw only 1 card
                    if self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]], opt=1) > 11:
                        strat_hit = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                               num_cards=1, n_iter=n_iter)
                    # less than 12 points -> draw card until 12 points
                    else:
                        strat_hit = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                               max_point=12, n_iter=n_iter)
                    
                    strat_double = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]],
                                              double=True, n_iter=n_iter)
                    result_dict["mean_profit_hit"].append(strat_hit.results["mean_profit"])
                    result_dict["mean_profit_double"].append(strat_double.results["mean_profit"])
                        
                result_dict["mean_profit_stand"].append(strat_stand.results["mean_profit"])
                result_dict["dealer_cards"].append("A")
                result_dict["player_cards"].append([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]])
                result_dict["points"].append(self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[j]], opt=1))
                result_dict["insurance"].append(True)
                result_dict["n_iter"].append(n_iter)
                    
                df = pd.concat([df, pd.DataFrame(result_dict)], ignore_index=True)
        
        df_split = pd.DataFrame(columns=["dealer_cards", "player_cards", "points", "mean_profit_stand",
                                         "mean_profit_hit", "mean_profit_double", "mean_profit_split",
                                         "mean_profit_split_double", "insurance", "n_iter"])
                
        for i in range(len(self.CARDS_PLAYER)):
                
            result_dict = dict()
            result_dict["dealer_cards"] = []
            result_dict["player_cards"] = []
            result_dict["points"] = []
            result_dict["mean_profit_stand"] = []
            result_dict["mean_profit_hit"] = []
            result_dict["mean_profit_double"] = []
            result_dict["mean_profit_split"] = []
            result_dict["mean_profit_split_double"] = []
            result_dict["insurance"] = []
            result_dict["n_iter"] = []
                             
            strat_stand = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                     max_point=0, n_iter=n_iter)
            strat_double = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                      double=True, n_iter=n_iter)
            strat_split = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                     max_point=12, split=True, n_iter=n_iter)
            strat_split_double = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                            double=True, split=True, n_iter=n_iter)
              
            # more than 11 points -> draw only 1 card
            if self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]], opt=1) > 11:
                strat_hit = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                       num_cards=1, n_iter=n_iter)
            # less than 12 points -> draw card until 12 points
            else:
                strat_hit = StrategyMC("A", [self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]],
                                       max_point=12, n_iter=n_iter)
                
            result_dict["mean_profit_stand"].append(strat_stand.results["mean_profit"])
            result_dict["mean_profit_hit"].append(strat_hit.results["mean_profit"])
            result_dict["mean_profit_double"].append(strat_double.results["mean_profit"])
            result_dict["mean_profit_split"].append(strat_split.results["mean_profit"])
            result_dict["mean_profit_split_double"].append(strat_split_double.results["mean_profit"])
            result_dict["dealer_cards"].append("A")
            result_dict["player_cards"].append([self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]])
            result_dict["points"].append(self.count_points([self.CARDS_PLAYER[i], self.CARDS_PLAYER[i]], opt=1))
            result_dict["insurance"].append(True)
            result_dict["n_iter"].append(n_iter)
                    
            df_split = pd.concat([df_split, pd.DataFrame(result_dict)], ignore_index=True)

        return df, df_split


if __name__ == "__main__":
    # df creation
    bbs = BuildBestStrategy()
    df_normal = bbs.normal_cases()
    df_split = bbs.split_cases()
    
    # df backup
    df_normal.to_csv("best_strategies/df_normal.csv")
    df_split.to_csv("best_strategies/df_split.csv")

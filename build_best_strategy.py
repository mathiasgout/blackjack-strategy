import pandas as pd
from strategy import StrategyMC

df_BJ_hard = pd.DataFrame(columns=["dealer_hand","starting_hand","points","stand","hit","double"])
stand_profit = []
dealer_hands = []
starting_hands = []
for card in ["2","3","4","5","6","7","8","9","T","A"]:
    results = StrategyMC(card, ["9","T"], n_iter=10000, max_point=19).results
    stand_profit.append(results["mean_profit"])
    dealer_hands.append(card)
    starting_hands.append("T9")

hit_profit = []
for card in ["2","3","4","5","6","7","8","9","T","A"]:
    results = StrategyMC(card, ["9","T"], n_iter=10000, max_point=20).results
    hit_profit.append(results["mean_profit"])

double_profit = []
for card in ["2","3","4","5","6","7","8","9","T","A"]:
    results = StrategyMC(card, ["9","T"], n_iter=10000, double=True).results
    double_profit.append(results["mean_profit"])




df_BJ_hard = pd.concat([df_BJ_hard, pd.DataFrame({"dealer_hand":["2"]*10,"starting_hand":["T9"]*10,"points":[19]*10,"stand":stand_profit, "hit":hit_profit,'double':double_profit})], ignore_index=True)
df_BJ_hard.dtypes

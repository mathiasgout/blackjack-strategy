import pandas as pd
import matplotlib.pyplot as plt
import ast
import seaborn as sns

df_normal = pd.read_csv("C:/Users/mathi/Documents/amusement/python/blackjack/best_strategies/df_normal.csv")
df_normal["best_strategy"] = df_normal.loc[:, ["mean_profit_stand", "mean_profit_hit", "mean_profit_double"]].idxmax(axis=1)
df_normal["best_strategy"] = df_normal.best_strategy.map({"mean_profit_stand":"stand", "mean_profit_hit":"hit", "mean_profit_double":"double"})


dealer_ace = df_normal.loc[df_normal.dealer_cards == "A", :].copy()
dealer_ace.reset_index(drop=True, inplace=True)

def get_card(cards, position):
    listed_cards = ast.literal_eval(cards)
    return listed_cards[position]

dealer_ace["card1"] = dealer_ace.player_cards.apply(get_card, position=1)
dealer_ace["card2"] = dealer_ace.player_cards.apply(get_card, position=0)
cards = ["A","T","9","8","7","6","5","4","3","2"]

df = pd.DataFrame(index=cards, columns=cards)
for i in range(dealer_ace.shape[0]):
    df.loc[dealer_ace.card1.iloc[i], dealer_ace.card2.iloc[i]] = dealer_ace.loc[i, "best_strategy"]


df.plot()

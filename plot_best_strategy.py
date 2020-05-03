import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
import seaborn as sns

df_normal = pd.read_csv("C:/Users/mathi/Documents/amusement/python/blackjack/best_strategies/df_normal.csv")
df_normal["best_strategy"] = df_normal.loc[:, ["mean_profit_stand", "mean_profit_hit", "mean_profit_double"]].idxmax(axis=1)
df_normal["best_strategy"] = df_normal.best_strategy.map({"mean_profit_stand":"stand", "mean_profit_hit":"hit", "mean_profit_double":"double"})


dealer_ace = df_normal.loc[df_normal.dealer_cards == "A", :].copy()
dealer_ace.reset_index(drop=True, inplace=True)

def get_card(cards, position):
    listed_cards = ast.literal_eval(cards)
    return listed_cards[position]

label_y = dealer_ace.player_cards.apply(get_card, position=1)
label_x = dealer_ace.player_cards.apply(get_card, position=0)

y = label_y.copy()
x = label_x.copy()

y = y.replace("T", 10)
x = x.replace("A", 11)
x = x.replace("T", 10)

y = y.to_numpy()
y = y.astype("int")
x = x.to_numpy()
x = x.astype("int")

strat_list = dealer_ace.best_strategy
strat_list = strat_list.replace("stand", 0)
strat_list = strat_list.replace("hit", 1)
strat_list = strat_list.replace("double", 2)
strat_list = strat_list.to_numpy()
strat_list = strat_list.astype("int")



max_profit = dealer_ace.loc[:, ["mean_profit_stand", "mean_profit_hit", "mean_profit_double"]].max(axis=1)
max_profit = max_profit.to_numpy()

df = pd.DataFrame(index=["T","9","8","7","6","5","4","3","2"], columns=["A","T","9","8","7","6","5","4","3"])
for i in range(len(max_profit)):
    df.loc[label_y.iloc[i],  label_x.iloc[i]] = max_profit[i]

df = np.tril(df)
df = df.astype("float")
df = df.round(2)
df = pd.DataFrame(df, index=["T","9","8","7","6","5","4","3","2"], columns=["A","T","9","8","7","6","5","4","3"])
mask = np.zeros_like(df)
mask[np.triu_indices_from(mask, 1)] = True


fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(11,5))

im = ax1.scatter(x, y, s=350, c=strat_list, cmap=plt.cm.get_cmap('Paired', 3), marker="s")
ax1.set_xlim(11.5, 2.5)
ax1.set_ylim(1.5, 10.5)
ax1.set(frame_on=False)

def fmt_func(x, loc):
    return ["Stand", "Hit", "Double"][x]

formatter = plt.FuncFormatter(fmt_func)

fig.colorbar(im, ticks = [0, 1, 2], format=formatter, ax=ax1)
im.set_clim(-0.5, 2.5)
ax1.set_xticks([11,10,9,8,7,6,5,4,3])
ax1.set_xticklabels(labels=["A", "T", 9, 8, 7, 6, 5, 4, 3])
ax1.set_yticks([2,3,4,5,6,7,8,9,10])
ax1.set_yticklabels(labels=[2, 3, 4, 5, 6, 7, 8, 9, "T"])
ax1.set_xlabel("First Player's Card")
ax1.set_ylabel("Second Player's Card")
ax1.set_title("Best Blackjack Strategy", pad=20)


im2 = sns.heatmap(df, linewidth=0.5, mask=mask, cmap="bwr", annot=True, vmax=2, vmin=-2, cbar_kws={'label': 'Mean Profit, Initial Bet = 1'}, ax=ax2)
im2.set_title('Mean Profit with Best Strategy', pad=20)
im2.set_xlabel("First Player's Card")
im2.set_ylabel("Second Player's Card")

fig.suptitle("Dealer's Card : Ace", fontsize=20, y=0.98, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.85])
plt.show()
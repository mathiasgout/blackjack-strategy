# Blackjack Strategy

Un programme Python permettant de jouer au Blackjack dans un terminal.
<br/> Recherche des meilleures stratégies grâce à des méthodes Monte Carlo.

Par exemple, voici les meilleures stratégies à adopter quand la carte du croupier est un 7 :

<p align="center">
  <img src="https://raw.githubusercontent.com/mathiasgout/blackjack_strategy/master/best_strategies/BS_dealer_7.png">
</p>

<br/>

## Instructions

- `main_console.py` permet aux utilisateurs de jouer au Blackjack dans un terminal. Il est possible de prendre une assurance, de doubler et de split.
- `strategy.py` permet de calculer le gain moyen d'un joueur, en fonction de la strategie qu'il adopte, de ses deux cartes de départ et de la carte du croupier, grâce à une méthode Monte Carlo.
- `build_best_strategy.py` permet de sauvegarder dans un data frame l'ensemble des gains moyens.
- `plot_best_strategy.py` permet d'afficher sur des graphiques les meilleures stratégies à adopter et les profits espérés.

Les résultats de `build_best_strategy.py` et `plot_best_strategy.py` sont déjà stockés dans le dossier `best_strategies/`.


## Requirements

Les packages suivants sont nécéssaires (pour utiliser `main_console.py`, seule une installation python 3.x sera requise.) : 

- python 3.x
- pandas
- matplotlib
- seaborn
- numpy

### Installation locale

Il est possible d'installer les packages en utilisant `pip` :
```
$ pip install -r requirements.txt
```

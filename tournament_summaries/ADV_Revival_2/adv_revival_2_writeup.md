# ADV Revival 2 Summary


## Table of Contents
1. [Background](#background)
2. [General Analysis](#general-analysis)
3. [Statistical Analysis](#statistical-analysis)
4. [Conclusions](#conclusions)


## Background
[ADV Revival 2](https://youtu.be/mPNWXh-YwJE?si=dD1SDCZ0zD9bS984) was a Pokemon tournament hosted by [Jimothy Cool](https://www.youtube.com/@jimothycool) and the [Revival Tournaments](https://www.youtube.com/@RevivalTournaments) YouTube Channel. This tournament uses the ADV OU metagame rulesets (with some minor modifications to limit high-luck playstyles). ADV OU consists of most of the pokemon available in the 3rd generation games (Ruby, Sapphire, Emerald era) with a few legendary pokemon excluded. With over 700 players this is the largest ever tournament for this ruleset. As such, it's a unique opportunity to delve deeper into a large series of games and pull out some statistical relationships. As part of the tournament players submitted their replays, these replays are helpfully stored in a .json format which can be machine read to extract important information.




## General Analysis


### Usage Rates


First off we have the top 10 pokemon in terms of overall usage rates. This list shouldn't be too unusual to anyone who has played ADV OU before.


|  Pokemon  | Usage Rate | Win Rate | Net Win Rate |
|-----------|:----------:|:--------:|:------------:|
| Tyranitar |   0.545216 | 0.498220 |     0.016912 |
| Metagross |   0.397694 | 0.473730 |    -0.007579 |
|  Swampert |   0.375999 | 0.496811 |     0.015503 |
|  Skarmory |   0.362069 | 0.498266 |     0.016957 |
|    Zapdos |   0.334095 | 0.485304 |     0.003996 |
|   Blissey |   0.304864 | 0.494382 |     0.013074 |
| Salamence |   0.294017 | 0.489320 |     0.008012 |
|    Celebi |   0.247088 | 0.490296 |     0.008988 |
|   Suicune |   0.243092 | 0.498826 |     0.017518 |
|    Gengar |   0.239667 | 0.464983 |    -0.016325 |


One thing you may have noticed is that the win rates are all below 0.5 Because I only had access to the public replays and not the full logs I only have information on what pokemon were seen (not which pokemon were on the player's team). You're more likely to win with unrevealed pokemon than lose (in a tournament setting like this, forfeits with unrevealed pokemon is much less likely). Therefore the total number of pokemon seen on a winning team is lower than the total number of pokemon seen on a losing team.


### Net Win Rates


If we sort instead by net win rate (their win rate over the average of 0.4813) the results show some pokemon with notably lower usage rates. I did limit this list to pokemon seen on at least 5% teams in the dataset to avoid cases where a pokemon was used a single time and has a 100% win rate.


|  Pokemon  | Usage Rate | Win Rate | Net Win Rate |
|-----------|:----------:|:--------:|:------------:|
| Registeel |   0.011532 | 0.534653 |     0.053345 |
|  Smeargle |   0.021009 | 0.516304 |     0.034996 |
|  Regirock |   0.018155 | 0.515723 |     0.034415 |
|      Jynx |   0.021009 | 0.510870 |     0.029561 |
|   Claydol |   0.178694 | 0.505431 |     0.024123 |
|   Milotic |   0.053094 | 0.505376 |     0.024068 |
|   Jirachi |   0.192510 | 0.505338 |     0.024030 |
|  Houndoom |   0.012332 | 0.500000 |     0.018692 |
|   Suicune |   0.243092 | 0.498826 |     0.017518 |
|  Skarmory |   0.362069 | 0.498266 |     0.016957 |


### Distribution of Revealed Pokemon


Below is a heatmap of the different numbers of revealed pokemon. As you can see, the majority of games are 6-6 with a large number of 5-6. As would be expected in a tournament setting but not necessarily a more casual setting there are very few forfeits where the loser has less than 6 revealed pokemon.


![Revealed Heatmap](./data/teammate_count_heatmap.png)


### Distribution of Turn Count


Below is a histogram of the number of turns each match took. If you're familiar with common distributions you may recognize this as being Weibull shaped (with a shape parameter > 1). This makes sense as what we are measuring is essentially the "time to game end" and the likelihood of the game ending gets higher every turn. This is analogous to the type of "time to failure" analysis for a part which experiences increased likelihood of failure as it ages which Weibulls are often used for.


![Turn Count Distribution](./data/turn_count_histogram.png)


### Average Number of Moves Used


Another flaw with the use of replays instead of full logs is that you only know the moves a pokemon used and not the moves they had but never moved. That said, I looked at how many moves a pokemon used on average. Again, this list is filtered to only pokemon who showed up on at least 5% of teams.


| Top 5      | Avg # of Used Moves | Bottom 5   | Avg # of Used Moves |
|------------|:-------------------:|------------|:-------------------:|
|   Venusaur |            2.472222 |    Dugtrio | 0.950224            |
|    Blissey |            2.453558 |    Marowak | 1.197368            |
|       Jynx |            2.369565 | Aerodactyl | 1.255756            |
| Misdreavus |            2.358209 |   Magneton | 1.322802            |
|   Smeargle |            2.326087 |     Raikou | 1.414286            |


![Revealed Moves Distribution](./data/revealed_moves.png)


## Statistical Analysis


With all this data I thought it was an excellent chance to see if we could learn anything about what pokemon and/or moves were most likely to change the outcomes of games.


### Pokemon Win Rates
Filtering all pokemon showing up in at least 5% of teams, I did a series of Fisher's Exact Tests to compare the win rates between teams that had that pokemon and teams that did not.


Ultimately I found that there are 4 pokemon which have a statistically significant effect on win rates. In the below table the odds ratio is how much more or less likely you are to win a game if you reveal one of the below pokemon. So in this case, having a (revealed) Heracross on your team makes you 0.66 times as likely to win as if you didn't have a revealed Heracross.


|  Pokemon   | Odds Ratio | p-value  |
|------------|:----------:|:--------:|
| Heracross  |   0.662219 | 2.937e-6 |
| Aerodactyl |   0.806867 | 1.110e-4 |
| Gengar     |   0.834993 | 3.419e-4 |
| Metagross  |   0.847307 | 1.567e-4 |


### Move Influence on Win Rates
I did a series of similar tests looking at all pokemon/move combinations that showed up on at least 5% of teams. I compared the win rate of the pokemon who used that move vs the win rate who did not and found 3 significant results.


|  Pokemon   | Move       |Odds Ratio| p-value  |
|------------|------------|:--------:|:--------:|
| Aerodactyl | Rock Slide | 0.620989 | 1.747e-5 |
| Celebi     | Giga Drain | 1.472952 | 9.836e-5 |
| Skarmory   | Spikes     | 1.792853 | 4.118e-5 |


All three of these options make somewhat intuitive sense to me. Giga drain on Celebi is a semi-uncommon move, if you decide to use it you likely have a good target in front of you can (and often will) hit. Skarmory Spikes is similar. If a Skarmory doesn't manage to get spikes down what was the point? It may have just died to Magneton and did nothing else. Aerodactyl Rock slide making things worse is interesting. My best guess is that a rock slide isn't usually the best choice to hit anything but flyers. But it's also so obvious that if they have any other option they'll likely switch to a rock resist and then you have to switch out the next turn. In many cases it's probably safer to predict the switch and switch yourself or use double edge/earthquake.


### Limiting to Upper Pool Play and Final Bracket
Many of the best ADV players participated in ADV Revival 2, but so did many people who are much less good. As a final test I looked at if there was a difference in the win rates when including only games after the first 5 rounds (~800 games) or only games in the final bracket (~50).


In both cases, a chi squared test showed that the higher level players bring different pokemon than the overall tournament.


|  Pokemon   | Filter        |Odds Ratio| p-value  |
|------------|---------------|:--------:|:--------:|
| Aerodactyl | After Round 5 | 0.762793 | 2.117e-4 |
| Hariyama   | After Round 5 | 0.530813 | 5.9297-5 |
| Jirachi    | After Round 5 | 1.395924 | 4.471e-7 |
| Milotic    | Final Bracket | 3.476509 | 6.771e-5 |


Furthermore, when looking at these smaller subsets no Pokemon showed a statistically significant relationship.


## Conclusions
The takeaways I have from this project are
1. Heracross, Aerodactyl, Gengar, and Metagross are often misused by lower level players
2. Clicking Rock Slide is often a mistake with Aerodactyl
3. Most pokemon use only 1 or 2 moves in a single game
4. The best players like Milotic a lot more than the general public
5. Collecting more data from high level players will give a larger sample side and show interesting results among the very best teams

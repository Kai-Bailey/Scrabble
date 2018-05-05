# Scrabble
A recreation of the popular game of Scrabble with challenging compter player. Created for CMPUT 275 final project by Kai Bailey and Cody Gramlich.

## Project Description
This project is a recreation of the popular game of scrabble. This game features a challenging computer player that users can test their skills against. When two computer players play against each other they consistently scores over 300 points per game. According to the Hasbro's website the top 300 players in the world "average between 330-450 points per game". Users can choose up to 4 players with any combination of computer players and human players. They can easily place, recall or exchange tiles. The user can see the score of each player, who's turn it is and the number of tiles left. If the user places an invalid word thier tiles will be automatically recalled.


<a href="https://imgflip.com/gif/29p9xq"><img src="https://i.imgflip.com/29p9xq.gif" title="made at imgflip.com"/></a>

Two Computer Players Playing Against Each Other

## Notes:
There are many 2 letter words that are valid in scrabble but not an actual English word. The computer is very good at
taking advantage of these words to build off words that are already played. If you are unsure whether the computer played a
valid word or not you can check by using control f in the dictionary.txt file.

To exchange tiles click the exchange tile button then select the tiles you would like to exchange. Once you are done select
the exchange tile button again. Exchanging tiles will cost you your turn.


## Included Files:
- scrabble.py - The main file of the program
- Board.py
- Trie.py
- Cell.py
- player.py
- dictionary.txt


## How to run:
1) Ensure that python 3.6 or greater is installed on your computer.
2) Install pygame using the command pip3 install pygame if you are on windows or
   sudo apt-get install python-pygame if you are on ubuntu.
3) In the folder containing the above files run the command python3 scrabble.py if you
   are on windows or python scrabble.py if you are on ubuntu.


## Authors
- Kai Bailey - Software engineering student at the University of Alberta
- Cody Gramlich - Software engineering student at the University of Alberta

References:

- The computer player implemented is based on The Worlds Fastest Scrabble Player, a research paper from Andrew W. Appel and
Guy J. Jacobson. The idea of reducing the game to 1 dimension by computing across/down checks and across/down sums was also
used when computing the score of words played, and whether those words were valid.
https://pdfs.semanticscholar.org/da31/cb24574f7c881a5dbf008e52aac7048c9d9c.pdf

- All of the rules for this game are based on the game of Scrabble from Hasbros.
https://scrabble.hasbro.com/en-us

- The method draw_random_tile in the board class was based on ideas discussed in the following forum. The code is able
to randomly select a key based on proportionality/weight of the value stored in the dictionary. This was used to randomly
select tiles from the "bag of tiles" where the letter of the tile was the key and the number of occurrences of the tile in
the bag of tiles is the value.
https://stackoverflow.com/questions/2570690/python-algorithm-to-randomly-select-a-key-based-on-proportionality-weight

- The file dictionary.txt was take from the following link.
https://raw.githubusercontent.com/jonbcard/scrabble-bot/master/src/dictionary.txt

- Number of points per game for pro scrabble players.
https://scrabble.hasbro.com/en-us/faq

- Pygame documentation.
https://www.pygame.org/docs/
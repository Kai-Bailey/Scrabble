import pygame
import random
from pygame.locals import *

letter_scores = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
                'H': 4, 'I': 1, 'J':8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
                'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U':1, 'V': 4, 'W': 4,
                 'X': 8, 'Y': 4, 'Z': 10}

class Board:
    def __init__(self):
        # Array of board each inner list is a row
        self.board = []
        # List of players playing the game
        self.players = []
        # Index in list players of whos turn it is
        self.turn = 0
        # "Bag of Tiles" left for the players to randomly choose from
        self.tiles = {'E':12, 'A':9, 'I':9, 'O':8, 'N':6, 'R':6, 'T':6, 'L':4, 'S':4, 'U':4, 'D':4, 'G':3, 'B':2, 'C':2, 'M':2, 'P':2, 'F':2, 'H':2, 'V':2, 'W':2, 'Y':2, 'K':1, 'J':1, 'X':1, 'Q':1, 'Z':1}
        self.number_tiles = 98

        self.initBoard()


    def initBoard(self):
        triple_word = set([(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14) ])
        double_word = set([(1,1), (2,2), (3,3), (4,4), (1,13), (2,12), (3,11), (4,10), (10,4), (11,3), (12,2), (13,1), (10,10), (11,11), (12,12), (13,13)])
        triple_letter = set([(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (5,1), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9) ])
        double_letter = set([(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (14,3), (14,11), (12,6), (12,8), (11,0), (11,7), (11,14)])
        for i in range(15):
            self.board.append([])
            for j in range(15):
                if (i,j) in triple_word:
                    self.board[i].append(Cell(None, 1, 3))
                elif (i,j) in double_word:
                    self.board[i].append(Cell(None, 1, 2))
                elif (i,j) in triple_letter:
                    self.board[i].append(Cell(None, 3, 1))
                elif (i,j) in double_letter:
                    self.board[i].append(Cell(None, 2, 1))
                else:
                    self.board[i].append(Cell(None, 1, 1))

    def draw_random_tile(self):
        """
        Draw a random tile from the "bag of tiles". Returns the leter that was drawn
        and removes it from the bag of tiles.
        """
        rand_ind = random.randint(1, self.number_tiles-1)
        
        sum_letters = 0
        for let, num_left in self.tiles.items():
            sum_letters += num_left
            if sum_letters > rand_ind:
                letter = let
                if self.tiles[let] == 1:
                    self.tiles.pop(let)
                else:
                    self.tiles[let] -= 1
                break

        self.number_tiles -= 1
        return letter


class Cell:
    def __init__(self, letter, letter_mul, word_mul):
        self.letter = letter
        self.word_mul = word_mul
        self.letter_mul = letter_mul

    def score(self):
        return letter_scores[self.letter]*self.letter_mul

    def setLetter(self, letter):
        self.letter = letter

    def getLetter(self):
        return self.letter

class Player:
    def __init__(self):
        self.rack = []
        self.score = 0

class Human:
    def __init__(self):
        super().__init__()

    def turn(self):
        pass

class Computer:
    def __init__(self):
        super().__init__()

    def turn(self):
        pass

class Tile:
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption('Scrabble')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((188, 255, 243))

    # font = pygame.font.Font(None, 36)
    # text = font.render('Scrabble', 1, (188, 51, 35))
    # textpos = text.get_rect(centerx=background.get_width()/2)
    # background.blit(text, textpos)

    screen.blit(background, (0,0))
    pygame.display.flip()

    for i in range(15):
        for j in range(15):
            tile = pygame.Rect((0+30*i, 0+30*j, 29, 29))
            pygame.draw.rect(background, (76, 255, 88), tile)
            if board.board[i][j].letter != None:
                font = pygame.font.Font(None, 24)
                letter = font.render(board.board[i][j].letter, 1, (10, 10, 10))
                background.blit(letter, (10+30*i, 10+30*j))
                pass
            if board.board[i][j].letter_mul != 1:
                font = pygame.font.Font(None, 20)
                # draw new tile color
                tile = pygame.Rect((0+30*i, 0+30*j, 29, 29))
                pygame.draw.rect(background, (66, 99, 247), tile)
                if board.board[i][j].letter_mul == 2:
                    doub_letter = font.render('DL', 1, (10, 10, 10))
                    background.blit(doub_letter, (5+30*i, 10+30*j))
                elif board.board[i][j].letter_mul == 3:
                    trip_letter = font.render('TL', 1, (10, 10, 10))
                    background.blit(trip_letter, (5+30*i, 10+30*j))


            if board.board[i][j].word_mul != 1:
                font = pygame.font.Font(None, 20)
                # draw new tile color255, 87, 61)
                tile = pygame.Rect((0+30*i, 0+30*j, 29, 29))
                pygame.draw.rect(background, (255, 87, 61), tile)
                if board.board[i][j].word_mul == 2:
                    doub_word = font.render('DW', 1, (10, 10, 10))
                    background.blit(doub_word, (5+30*i, 10+30*j))
                elif board.board[i][j].word_mul == 3:
                    trip_word = font.render('TW', 1, (10, 10, 10))
                    background.blit(trip_word, (5+30*i, 10+30*j))



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.blit(background, (0,0))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':

    board = Board()
    board.initBoard()

    main()



import pygame
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
                print(self.board[i][j].letter_mul, end=" ")
            print()


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
    pass

class Tile:
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
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


    # tile = pygame.Surface((30, 30))
    # tile.fill((239, 188, 79))
    # background.blit(tile, (0, 0))


    font = pygame.font.Font(None, 13)
    letter = font.render('A', 1, (10, 10, 10))
    letterpos = letter.get_rect(centerx=tile.get_width()/2)
    tile.blit(letter, (0,0))

    for i in range(15):
        for j in range(15):
            pygame.draw.rect(background, (70, 96, 91), (0+30*i, 0+30*j, 30, 30), 3)
            


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.blit(background, (0,0))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    # main()

    board = Board()
    board.initBoard()
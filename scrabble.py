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

# draws all objects onto the background
def draw_everything(background):
    pos = pygame.mouse.get_pos()
    tile_size = background.get_width()/15

    # draw board
    for i in range(15):
        for j in range(15):
            # draw letter tile
            tile = pygame.Rect((0+tile_size*i, 0+tile_size*j, tile_size-1, tile_size-1))

            # if cell has a letter
            if board.board[i][j].letter != None:
                pygame.draw.rect(background, (255, 200, 50), tile)
                # draw letter on tile
                font = pygame.font.Font(None, 24)
                letter = font.render(board.board[i][j].letter, 1, (10, 10, 10))
                background.blit(letter, (9+tile_size*i, 8+tile_size*j))
                # draw score in bottom right corner of tile
                font = pygame.font.Font(None, 12)
                letter_score = font.render(str(letter_scores[board.board[i][j].letter]), 1, (10, 10, 10))
                background.blit(letter_score, (20+tile_size*i, 20+tile_size*j))

            # if cell is a letter multiplier
            elif board.board[i][j].letter_mul != 1:
                font = pygame.font.Font(None, 20)
                # draw new tile color
                pygame.draw.rect(background, (66, 99, 247), tile)
                if board.board[i][j].letter_mul == 2:
                    doub_letter = font.render('DL', 1, (10, 10, 10))
                    background.blit(doub_letter, (5+tile_size*i, 10+tile_size*j))
                elif board.board[i][j].letter_mul == 3:
                    trip_letter = font.render('TL', 1, (10, 10, 10))
                    background.blit(trip_letter, (5+tile_size*i, 10+tile_size*j))

            # if cell is a word multiplier
            elif board.board[i][j].word_mul != 1:
                font = pygame.font.Font(None, 20)
                # draw new tile color
                pygame.draw.rect(background, (255, 87, 61), tile)
                if board.board[i][j].word_mul == 2:
                    doub_word = font.render('DW', 1, (10, 10, 10))
                    background.blit(doub_word, (5+tile_size*i, 10+tile_size*j))
                elif board.board[i][j].word_mul == 3:
                    trip_word = font.render('TW', 1, (10, 10, 10))
                    background.blit(trip_word, (5+tile_size*i, 10+tile_size*j))

            # draw empty cell
            else:
                pygame.draw.rect(background, (76, 255, 88), tile)

        # draw rack
        for i in range(4, 11):
            # draw tile in rack
            tile = pygame.Rect((0+tile_size*i, 0+tile_size*16, tile_size-1, tile_size-1))
            pygame.draw.rect(background, (255, 200, 50), tile)
            # draw letter on tile
            font = pygame.font.Font(None, 24)
            letter = font.render(rack[i-4], 1, (10, 10, 10))
            background.blit(letter, (9+tile_size*i, 8+tile_size*16))
            # draw score in bottom right corner of tile
            font = pygame.font.Font(None, 12)
            letter_score = font.render(str(letter_scores[rack[i-4]]), 1, (10, 10, 10))
            background.blit(letter_score, (20+tile_size*i, 20+tile_size*16))

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption('Scrabble')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((188, 255, 243))

    screen.blit(background, (0,0))
    pygame.display.flip()

    draw_everything(background)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.blit(background, (0,0))
        pygame.display.flip()

        draw_everything(background)

    pygame.quit()


if __name__ == '__main__':

    board = Board()
    board.initBoard()
    board.board[0][5].letter = 'A'
    board.board[0][7].letter = 'Q'
    rack = ['H', 'L', 'E', 'O', 'L', 'N', 'B']
    main()

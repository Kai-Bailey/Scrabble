import pygame
import random
import Trie
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
        """
        Initializes the playing board by making self.board a 15x15 matrix. The matrix is represented by a
        list of lists and each element is an object of class cell. Based on their position on the board cells
        cells can be initialized as double/triple word or double/triple letter. 
        """

        triple_word = set([(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14) ])
        double_word = set([(1,1), (2,2), (3,3), (4,4), (1,13), (2,12), (3,11), (4,10), (10,4), (11,3), (12,2), (13,1), (10,10), (11,11), (12,12), (13,13)])
        triple_letter = set([(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (5,1), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9) ])
        double_letter = set([(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (14,3), (14,11), (12,6), (12,8), (11,0), (11,7), (11,14)])
        for i in range(15):
            self.board.append([])
            for j in range(15):
                if (i,j) in triple_word:
                    self.board[i].append(Cell(None, 1, 3, i, j))
                elif (i,j) in double_word:
                    self.board[i].append(Cell(None, 1, 2, i, j))
                elif (i,j) in triple_letter:
                    self.board[i].append(Cell(None, 3, 1, i, j))
                elif (i,j) in double_letter:
                    self.board[i].append(Cell(None, 2, 1, i, j))
                else:
                    self.board[i].append(Cell(None, 1, 1, i, j))


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


    def compute_score(self, cells_played):
        """
        Given a list of cells will return the score of the word within those cells.
        """
        score = 0
        word_multiplier = 1
        for cell in cells_played:

            score += letter_scores[cell.letter] * cell.letter_mul
            word_multiplier *= cell.word_mul

        return score * word_multiplier
 
        
    def check_sum_single(self, check_cell, cell, orientation):

        # Tile already place their no need to compute cross checks and sums
        if check_cell.letter != None:
            return

        check_cell.anchor = True

        if orientation == 'L':
            curr_cell = self.board.tiles[row][col+1]
            postfix = []
            while curr_cell.letter != None:
                postfix.append(curr_cell.letter)
                curr_cell = self.board.tiles[row][col+1]


    def cross_checks_sums(self, cells_played):
        """
        Given a list of cells, will update the cross checks and cross sums for all of
        empty adjacent cells. Make sure the list cells_played includes cells already on
        the board if the were a part of the word played.
        """
        
        for cell in cells_played:
            row = cell.row
            col = cell.col
            # Check the cell above
            if cell.row > 0:
                check_sum_single(self.board.tiles[row-1][col], cell, 'U')
            # Check the cell to the below
            if cell.row < 14:
                check_sum_single(self.board.tiles[row+1][col], cell, 'D')
            # Check the cell to the left
            if cell.col > 0:
                check_sum_single(self.board.tiles[row][col-1], cell, 'L')
            # Check the cell to the right
            if cell.col < 14:
                check_sum_single(self.board.tiles[row][col+1], cell, 'R')


class Cell:
    def __init__(self, letter, letter_mul, word_mul, row, col):
        self.letter = letter
        self.word_mul = word_mul
        self.letter_mul = letter_mul
        self.row = row
        self.col = col
        # True of the cell is adjacent to a cell with a letter in it
        self.anchor = False
        # The valid letters that can be placed in this cell
        self.cross_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
    
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


def check_valid(self, trie, cells_played):
    """
    Given a list of the cells played will check if the word is valid. The word
    is only valid if each letter played is in the set cross_check for that given 
    cell and the word as a whole is in the dictionary (trie tree).
    """
    word = []
    for cell in cells_played:
        word.append(cell.letter)
        if cell.letter not in cell.cross_check:
            return False
    
    if trie.valid_word(word):
        return True
    else:
        return False  


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

import pygame
import random
import Trie
from pygame.locals import *

letter_scores = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
                'H': 4, 'I': 1, 'J':8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
                'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U':1, 'V': 4, 'W': 4,
                 'X': 8, 'Y': 4, 'Z': 10}

class Board:
    def __init__(self, dict_name):
        # Array of board each inner list is a row
        self.board = []
        # List of players playing the game
        self.players = []
        # Index in list players of whos turn it is
        self.turn = 0
        # "Bag of Tiles" left for the players to randomly choose from
        self.tiles = {'E':12, 'A':9, 'I':9, 'O':8, 'N':6, 'R':6, 'T':6, 'L':4, 'S':4, 'U':4, 'D':4, 'G':3, 'B':2, 'C':2, 'M':2, 'P':2, 'F':2, 'H':2, 'V':2, 'W':2, 'Y':2, 'K':1, 'J':1, 'X':1, 'Q':1, 'Z':1}
        self.number_tiles = 98

        self.dictionary = Trie.TrieTree()
        self.dictionary.trie_from_txt(dict_name)

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


    def check_valid(self, cells_played):
        """
        Given a list of the cells played will check if the word is valid. The word
        is only valid if each letter played is in the set cross_check for that given
        cell and the word as a whole is in the dictionary (trie tree).
        """

        if len(cells_played) == 1:
            cell = cells_played[0]
            if cell.letter in cell.across_check and cell.letter in cell.down_check:
                return True
            else:
                return False

        word = []

        if cells_played[0].row == cells_played[1].row:
            for cell in cells_played:
                word.append(cell.letter)
                if cell.letter not in cell.down_check:
                    return False
        else:
            for cell in cells_played:
                word.append(cell.letter)
                if cell.letter not in cell.across_check:
                    return False

        # Convert the list of letters to a string
        word = ''.join(word)
        word = word.lower()

        if self.dictionary.valid_word(word):
            return True
        else:
            return False


    def compute_score(self, cells_played):
        """
        Given a list of cells will return the score of the word within those cells.
        Including any addition words that it connects to which are accounted for by
        the check_sum of each cell.
        """
        score = 0
        word_multiplier = 1
        for cell in cells_played:

            score += letter_scores[cell.letter] * cell.letter_mul
            score += cell.check_sum
            word_multiplier *= cell.word_mul

        return score * word_multiplier


    def compute_score_already_placed(self, cells_played):
        """
        Given a list of cells will return the score of the word within those cells. Used
        internally to update the cross_sum in the function check_sum_single. Ignores the
        check_sum of the current cells.
        """
        score = 0
        word_multiplier = 1
        for cell in cells_played:

            score += letter_scores[cell.letter] * cell.letter_mul
            word_multiplier *= cell.word_mul

        return score * word_multiplier


    def row_check(self, row):
        for cell in self.board[row]:
            if cell.letter != None:
                return
            row = cell.row
            col = cell.col
            cell.anchor = True

            prefix = []
            prefix_cell = []
            while col > 0:
                col -= 1
                cur_cell = self.board[row][col]
                if cur_cell != None:
                    prefix.append(cur_cell.letter)
                    prefix_cell.append(cur_cell)
                else:
                    break
            prefix.reverse()

            row = cell.row
            col = cell.col
            suffix = []
            suffix_cell = []
            while col < 14:
                col += 1
                cur_cell = self.board[row][col]
                if cur_cell != None:
                    suffix.append(cur_cell.letter)
                    suffix_cell.append(cur_cell)
                else:
                    break

            cell.check_sum = self.compute_score_already_placed(prefix_cell) + self.compute_score_already_placed(suffix_cell)
            self.dictionary.update_across_check(prefix, suffix, cell)

    def down_check(self, col):
        for row in self.board:
            cell = self.board[row][col]
            if cell.letter != None:
                return
            row = cell.row
            col = cell.col
            cell.anchor = True

            prefix = []
            prefix_cell = []
            while row > 0:
                row -= 1
                cur_cell = self.board[row][col]
                if cur_cell != None:
                    prefix.append(cur_cell.letter)
                    prefix_cell.append(cur_cell)
                else:
                    break
            prefix.reverse()

            row = cell.row
            col = cell.col
            suffix = []
            suffix_cell = []
            while row < 14:
                row += 1
                cur_cell = self.board[row][col]
                if cur_cell != None:
                    suffix.append(cur_cell.letter)
                    suffix_cell.append(cur_cell)
                else:
                    break

            cell.check_sum = self.compute_score_already_placed(prefix_cell) + self.compute_score_already_placed(suffix_cell)
            self.dictionary.update_down_check(prefix, suffix, cell)


    def cross_checks_sums(self, cells_played):
        """
        Given a list of cells, will update the cross checks and cross sums for all of
        empty adjacent cells.
        """

        for cell in cells_played:
            row = cell.row
            col = cell.col
            # Check the cell above
            if cell.row > 0:
                self.check_sum_single(self.board[row-1][col], cell, 'DownMove')
            # Check the cell to the below
            if cell.row < 14:
                self.check_sum_single(self.board[row+1][col], cell, 'DownMove')
            # Check the cell to the left
            if cell.col > 0:
                self.check_sum_single(self.board[row][col-1], cell, 'AcrossMove')
            # Check the cell to the right
            if cell.col < 14:
                self.check_sum_single(self.board[row][col+1], cell, 'AcrossMove')



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
        self.across_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.down_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        # If a letter is played there in this cell the additional points
        # it will get from connecting to additional words
        self.cross_sum = 0

    def score(self):
        return letter_scores[self.letter]*self.letter_mul

    def setLetter(self, letter):
        self.letter = letter

    def getLetter(self):
        return self.letter

class Player:
    def __init__(self, board):
        self.rack = []
        self.score = 0
        self.board = board

    # place a tile on the board
    def place_tile(self, rack_tile, cell):
        self.board.board[cell[0]][cell[1]].letter = self.rack[rack_tile]
        self.rack[rack_tile] = 'Z' # tile is null for now
        pass


    def play(self):

        pass

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

class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.surface = background
        self.board = Board('20k.txt')
        self.player1 = Player(self.board)
        self.player2 = Player(self.board)
        self.running = True
        self.tile_size = self.surface.get_width()/15
        self.text_color = (10, 10, 10)

    def play_game(self):
        self.board.board[0][5].letter = 'A'
        self.board.board[0][7].letter = 'Q'
        self.player1.rack = ['H', 'L', 'E', 'O', 'L', 'N', 'B']
        self.player1.place_tile(1, (0, 0))
        self.draw_board()
        self.draw_rack()
        self.draw()

        self.board.board[10][8].letter = 'H'
        self.board.board[10][9].letter = 'E'
        self.board.board[10][10].letter = 'L'
        self.board.board[10][11].letter = 'L'
        self.board.board[10][12].letter = 'O'

        cells_played = [self.board.board[10][8], self.board.board[10][9], self.board.board[10][10], \
        self.board.board[10][11], self.board.board[10][12]]
        print(self.board.check_valid(cells_played))

        while self.running:
            self.handle_event()
            self.update()
            self.draw()

    def draw_tile(self, i, j):
        # draw letter tile
        tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*j, self.tile_size-1, self.tile_size-1))
        # if cell has a letter
        if self.board.board[j][i].letter != None:
            pygame.draw.rect(self.surface, (255, 200, 50), tile)

            # draw letter on tile
            font = pygame.font.Font(None, 24)
            letter = font.render(self.board.board[j][i].letter, 1, self.text_color)
            self.surface.blit(letter, (9+self.tile_size*i, 8+self.tile_size*j))
            # draw score in bottom right corner of tile
            font = pygame.font.Font(None, 12)
            letter_score = font.render(str(letter_scores[self.board.board[j][i].letter]), 1, self.text_color)
            self.surface.blit(letter_score, (20+self.tile_size*i, 20+self.tile_size*j))

        # if cell is a letter multiplier
        elif self.board.board[j][i].letter_mul != 1:
            font = pygame.font.Font(None, 20)
            # draw new tile color
            pygame.draw.rect(self.surface, (66, 99, 247), tile)
            if self.board.board[j][i].letter_mul == 2:
                doub_letter = font.render('DL', 1, self.text_color)
                self.surface.blit(doub_letter, (5+self.tile_size*i, 10+self.tile_size*j))
            elif self.board.board[j][i].letter_mul == 3:
                trip_letter = font.render('TL', 1, self.text_color)
                self.surface.blit(trip_letter, (5+self.tile_size*i, 10+self.tile_size*j))

        # if cell is a word multiplier
        elif self.board.board[j][i].word_mul != 1:
            font = pygame.font.Font(None, 20)
            # draw new tile color
            pygame.draw.rect(self.surface, (255, 87, 61), tile)
            if self.board.board[j][i].word_mul == 2:
                doub_word = font.render('DW', 1, self.text_color)
                self.surface.blit(doub_word, (5+self.tile_size*i, 10+self.tile_size*j))
            elif self.board.board[j][i].word_mul == 3:
                trip_word = font.render('TW', 1, self.text_color)
                self.surface.blit(trip_word, (5+self.tile_size*i, 10+self.tile_size*j))

        # draw empty cell
        else:
            pygame.draw.rect(self.surface, (76, 255, 88), tile)


    def draw_board(self):
        for i in range(15):
            for j in range(15):
                self.draw_tile(i,j)


    def draw_rack(self):
        for i in range(4, 11):
            # draw tile in rack
            tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
            pygame.draw.rect(self.surface, (255, 200, 50), tile)
            # draw letter on tile
            font = pygame.font.Font(None, 24)
            letter = font.render(self.player1.rack[i-4], 1, self.text_color)
            self.surface.blit(letter, (9+self.tile_size*i, 8+self.tile_size*16))
            # draw score in bottom right corner of tile
            font = pygame.font.Font(None, 12)
            letter_score = font.render(str(letter_scores[self.player1.rack[i-4]]), 1, self.text_color)
            self.surface.blit(letter_score, (20+self.tile_size*i, 20+self.tile_size*16))

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in range(15):
                for j in range(15):
                    tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*j, self.tile_size-1, self.tile_size-1))
                    if tile.collidepoint(pos):
                        self.board.board[j][i].letter = 'Z'
                        self.draw_tile(i,j)

    def draw(self):
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()

    def update(self):
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption('Scrabble')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((188, 255, 243))

    screen.blit(background, (0,0))
    pygame.display.flip()

    game = Game(screen, background)
    game.play_game()
    pygame.quit()


if __name__ == '__main__':
    main()

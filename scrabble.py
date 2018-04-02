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
        # Array of board each inner list is a row and each item in the list is 
        # an instance of class cell
        self.board = []
        # List of players playing the game
        self.players = []
        # Index in list players of whos turn it is
        self.turn = 0
        # "Bag of Tiles" left for the players to randomly choose from
        self.tiles = {'E':12, 'A':9, 'I':9, 'O':8, 'N':6, 'R':6, 'T':6, 'L':4, 'S':4, 'U':4, 'D':4, 'G':3, 'B':2, 'C':2, 'M':2, 'P':2, 'F':2, 'H':2, 'V':2, 'W':2, 'Y':2, 'K':1, 'J':1, 'X':1, 'Q':1, 'Z':1}
        self.number_tiles = 98

        # A trie tree of all the valid words to be used in the game
        self.dictionary = Trie.TrieTree()
        self.dictionary.trie_from_txt(dict_name)

        # Fill and initialize cells in self.board
        self.initBoard()

    def initBoard(self):
        """
        Initializes the playing board by making self.board a 15x15 matrix. The matrix is represented by a
        list of lists and each element is an object of class cell. Based on their position on the board cells
        cells can be initialized as double/triple word or double/triple letter.
        """
        # Encodes the information of which cells are double/triple word/letter and centre
        centre = set([(7,7)])
        triple_word = set([(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)])
        double_word = set([(1,1), (2,2), (3,3), (4,4), (1,13), (2,12), (3,11), (4,10), (10,4), (11,3), (12,2), (13,1), (10,10), (11,11), (12,12), (13,13)])
        triple_letter = set([(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (5,1), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9) ])
        double_letter = set([(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (14,3), (14,11), (12,6), (12,8), (11,0), (11,7), (11,14)])
        
        # Iterate through all cells on the board check if the are double/triple word/letter or centre
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
                elif (i,j) in centre:
                    centre_cell = Cell(None, 1, 1, i, j)
                    centre_cell.centre = True
                    centre_cell.anchor = True
                    print(centre_cell.centre)
                    self.board[i].append(centre_cell)
                else:
                    self.board[i].append(Cell(None, 1, 1, i, j))


    def draw_random_tile(self):
        """
        Draw a random tile from the "bag of tiles". Returns the leter that was drawn
        and removes it from the bag of tiles.
        """
        # Random number between 1 and the number of tiles
        rand_ind = random.randint(1, self.number_tiles-1)

        # Loop though the tiles in the bag until greater than rand int.
        # Remove that tile and return it.
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
        
        # Convert cells will return an empty list of cells if the cells played 
        # are not all in the same row or collumn. In this case the word is false.
        if len(cells_played) == 0:
            return False

        # Ensure that atleast one letter is connected to the others on the board
        connected = False
        for cell in cells_played:
            if cell.anchor:
                connected = True 

        if not connected:
            return False 

        # If it is single letter just have to check the down checks and across checks
        if len(cells_played) == 1:
            cell = cells_played[0]
            if cell.letter in cell.down_check and cell.letter in cell.across_check:
                return True
            else:
                return False              

        # If it is an across move make sure all cells satisfy their down checks
        word = []
        if cells_played[0].row == cells_played[1].row:
            for cell in cells_played:
                word.append(cell.letter)
                if cell.letter not in cell.down_check:
                    return False
        # If it is a down move ensure all cells satisy their across checks
        else:
            for cell in cells_played:
                word.append(cell.letter)
                if cell.letter not in cell.across_check:
                    return False

        # Convert the list of letters to a string
        word = ''.join(word)
        word = word.upper()

        # Check that the overall word is a valid
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

        if len(cells_played) == 1:
            for cell in cells_played:
                score += letter_scores[cell.letter] * cell.letter_mul
                score += cell.down_sum
                score += cell.across_sum
                word_multiplier *= cell.word_mul
        elif cells_played[0].row == cells_played[1].row:
                for cell in cells_played:
                    score += letter_scores[cell.letter] * cell.letter_mul
                    score += cell.down_sum
                    word_multiplier *= cell.word_mul
        else:
            for cell in cells_played:
                score += letter_scores[cell.letter] * cell.letter_mul
                score += cell.across_sum
                word_multiplier *= cell.word_mul


        return score * word_multiplier


    def compute_score_already_placed(self, cells_played):
        """
        Given a list of cells will return the score of the word within those cells. Used
        internally to update the cross_sum in the function check_sum_single. Ignores the
        check_sum of the current cells and letter/word multipliers.
        """
        score = 0

        for cell in cells_played:
            score += letter_scores[cell.letter]

        return score


    def across_check(self, row):
        """
        Updates the across_check for every cell in a row on the board. The across_check
        is all valid letters that can be played so when making a down word through this 
        cell it also forms valid across words.
        """

        for cell in self.board[row]:
            # If the letter is already placed then skip
            if cell.letter != None:
                continue
            row = cell.row
            col = cell.col

            # Build the prefix of all the words before this letter
            prefix = []
            prefix_cell = []
            while col > 0:
                col -= 1
                cur_cell = self.board[row][col]
                if cur_cell.letter != None:
                    prefix.append(cur_cell.letter)
                    prefix_cell.append(cur_cell)
                else:
                    break
            prefix.reverse()

            # Build the suffix of all letters after this one
            row = cell.row
            col = cell.col
            suffix = []
            suffix_cell = []
            while col < 14:
                col += 1
                cur_cell = self.board[row][col]
                if cur_cell.letter != None:
                    suffix.append(cur_cell.letter)
                    suffix_cell.append(cur_cell)
                else:
                    break

            prefix = ''.join(prefix)
            prefix = prefix.upper()
            suffix = ''.join(suffix)
            suffix = suffix.upper()

            # If their are no letters to the left or right then no letters need to be removed from
            # the across_check
            if prefix == '' and suffix == '':
                continue

            # Cell is empty but adjacent to a placed tile so it canbe the start of a new word
            cell.anchor = True

            # Update the across sum by adding the points for the suffix and prefix 
            cell.across_sum = self.compute_score_already_placed(prefix_cell) + self.compute_score_already_placed(suffix_cell)
            # Update the across check for the cell
            self.dictionary.update_across_check(prefix, suffix, cell)

    def down_check(self, col):
        """
        Updates the down_check for every cell in a collumn on the board. The down_check
        is all valid letters that can be played so when making an across word through this 
        cell it also forms valid down words.
        """
        for row in self.board:
            cell = row[col]
            # If the letter is already placed then skip it
            if cell.letter != None:
                continue
            row = cell.row
            col = cell.col

            # Build the prefix of the letter above the current cell
            prefix = []
            prefix_cell = []
            while row > 0:
                row -= 1
                cur_cell = self.board[row][col]
                if cur_cell.letter != None:
                    prefix.append(cur_cell.letter)
                    prefix_cell.append(cur_cell)
                else:
                    break
            prefix.reverse()

            # Build the suffix of the letter below the current cell
            row = cell.row
            col = cell.col
            suffix = []
            suffix_cell = []
            while row < 14:
                row += 1
                cur_cell = self.board[row][col]
                if cur_cell.letter != None:
                    suffix.append(cur_cell.letter)
                    suffix_cell.append(cur_cell)
                else:
                    break

            prefix = ''.join(prefix)
            prefix = prefix.upper()
            suffix = ''.join(suffix)
            suffix = suffix.upper()

            # If the cell has nothing above or below it then no need to remove letter
            # from the down_check
            if prefix == '' and suffix == '':
                continue

            # Cell is empty but adjacent to a placed tile so it canbe the start of a new word
            cell.anchor = True

            # Update the down sum using the prefix and suffix
            cell.down_sum = self.compute_score_already_placed(prefix_cell) + self.compute_score_already_placed(suffix_cell)
            # Update the down check
            self.dictionary.update_down_check(prefix, suffix, cell)


    def cross_checks_sums(self, cells_played):
        """
        Given a list of cells, will update the cross checks and cross sums for all of
        empty adjacent cells.
        """

        if len(cells_played) == 1:
            self.down_check(cells_played[0].col)
            self.across_check(cells_played[0].row)
        elif cells_played[0].row == cells_played[1].row:
            self.across_check(cells_played[0].row)
            for cell in cells_played:
                self.down_check(cell.col)
        else:
            self.down_check(cells_played[0].col)
            for cell in cells_played:
                self.across_check(cell.row)

    def placed_cell_cleanup(self, cells_played):
        """
        Sets the across_sum and down_sum of the cells to 0 to ensure that they are not added to future scores.
        Sets anchor to false these cells are placed so they cannot be the start of a new word.
        """
        for cell in cells_played:
            cell.across_sum = 0
            cell.down_sum = 0
            cell.anchor = False
            cell.letter_mul = 1
            cell.word_mul = 1

    def convert_cells_played(self, cells_played):
        """
        The cells played list can be in an order with just the cells that were played
        and not the ones already on the board. This function will order them and fill
        in any of the letters on the board to complete the word.
        """
        if len(cells_played) == 1:
            return cells_played
        
        elif cells_played[0].row == cells_played[1].row:
            # If all the cells are not on the same row then send an empty list to valid_word
            # wich will return false
            for cell in cells_played:
                if cells_played[0].row != cell.row:
                    return []

            cells_played.sort(key=lambda cell: cell.col)
            start_cell = cells_played[0]
            end_cell = cells_played[-1]

            # Add all adjacent cells with letters to the left of the first placed letter
            row = start_cell.row
            col = start_cell.col
            while col > 0:
                col -= 1
                curr_cell = self.board[row][col]
                if curr_cell.letter != None:
                    cells_played.append(curr_cell)
                else:
                    break

            # Add all adjacent cells with letters to the right of the last letter
            row = end_cell.row
            col = end_cell.col
            while col < 14:
                col += 1
                curr_cell = self.board[row][col]
                if curr_cell.letter != None:
                    cells_played.append(curr_cell)
                else:
                    break

            # Add all cells between the first and last placed letters
            row = start_cell.row
            col = start_cell.col
            curr_cell = start_cell
            while curr_cell is not end_cell:
                if curr_cell not in cells_played:
                    cells_played.append(curr_cell)
                col += 1
                curr_cell = self.board[row][col]

            cells_played.sort(key=lambda cell: cell.col)
            return cells_played

        # A down word was played
        else:
            # If all the cells are not on the same collumn then send an empty list to valid_word
            # wich will return false
            for cell in cells_played:
                if cells_played[0].col != cell.col:
                    return []

            cells_played.sort(key=lambda cell: cell.row)
            start_cell = cells_played[0]
            end_cell = cells_played[-1]

            # Add all adjacent cells with letters above the first placed letter
            row = start_cell.row
            col = start_cell.col
            while row > 0:
                row -= 1
                curr_cell = self.board[row][col]
                if curr_cell.letter != None:
                    cells_played.append(curr_cell)
                else:
                    break

            # Add all adjacent cells with letters below the last letter
            row = end_cell.row
            col = end_cell.col
            while row < 14:
                row += 1
                curr_cell = self.board[row][col]
                if curr_cell.letter != None:
                    cells_played.append(curr_cell)
                else:
                    break

            # Add all cells between the first and last placed letters
            row = start_cell.row
            col = start_cell.col
            curr_cell = start_cell
            while curr_cell is not end_cell:
                if curr_cell not in cells_played:
                    cells_played.append(curr_cell)
                row += 1
                curr_cell = self.board[row][col]

            cells_played.sort(key=lambda cell: cell.row)
            return cells_played


class Cell:
    def __init__(self, letter, letter_mul, word_mul, row, col):
        self.letter = letter
        self.word_mul = word_mul
        self.letter_mul = letter_mul
        self.centre = False
        self.row = row
        self.col = col
        # True of the cell is adjacent to a cell with a letter in it
        self.anchor = False
        # The valid letters that can be placed in this cell
        self.across_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.down_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        # If a letter is played there in this cell the additional points
        # it will get from connecting to additional words
        self.across_sum = 0
        self.down_sum = 0

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
        # dictionary for placed tiles: key is rack index, value is (letter, (row, col))
        self.placed_tiles = {}
        self.selected_tile = ''
        self.is_tile_selected = False

        self.init_rack()

    # place a tile on the board
    def place_tile(self, rack_tile, row, col):
        self.board.board[col][row].letter = self.rack[rack_tile]
        self.placed_tiles[self.selected_tile] = (self.rack[self.selected_tile], (col, row))
        self.rack[self.selected_tile] = ''
        pass

    # looks in the placed_tiles dictionary, checks if it's a word
    # if it is, then it plays the word and returns true
    def play_word(self):
        tiles_played = []
        new_tiles = {}

        for t in self.placed_tiles:
            row = self.placed_tiles[t][1][0]
            col = self.placed_tiles[t][1][1]
            cell = self.board.board[row][col]
            tiles_played.append(cell)

        tiles_played = self.board.convert_cells_played(tiles_played)

        for t in tiles_played:
            print(t.letter)

        if self.board.check_valid(tiles_played):
            print(True)

            self.board.cross_checks_sums(tiles_played)
            score = self.board.compute_score(tiles_played)
            self.score += self.board.compute_score(tiles_played)
            self.board.placed_cell_cleanup(tiles_played)
            print("Score: ", score)

            # get new tiles and put on rack
            for t in self.placed_tiles:
                new_tiles[t] = self.board.draw_random_tile()
                self.rack[t] = new_tiles[t]
            return True
        else:
            print(False)
            return False

    # recalls the tiles back to the rack
    # currently does not empty the placed tiles dictionary
    # that is done in the game class right now
    def recall(self):
        for t in self.placed_tiles:
            row = self.placed_tiles[t][1][0]
            col = self.placed_tiles[t][1][1]
            # remove tiles from board
            self.board.board[row][col].letter = None
            # put tiles back on rack
            self.rack[t] = self.placed_tiles[t][0]

    # initiliazes the rack by drawing 7 tiles from the bag
    def init_rack(self):
        for i in range(7):
            self.rack.append(self.board.draw_random_tile())

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

class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.surface = background
        self.board = Board('dictionary.txt')
        self.player1 = Player(self.board)
        self.player2 = Player(self.board)
        self.running = True
        self.tile_size = self.surface.get_width()/15
        self.text_color = (10, 10, 10)


    def play_game(self):

        # self.board.board[10][8].letter = 'H'
        # self.board.board[10][9].letter = 'E'
        # self.board.board[10][10].letter = 'L'
        # self.board.board[10][11].letter = 'L'
        # self.board.board[10][12].letter = 'O'

        # cells_played = [self.board.board[10][10], self.board.board[10][8], self.board.board[10][9], \
        # self.board.board[10][11]]

        # # The cells played list can be in an order with just the cells that were played
        # # and not the ones already on the board. This function will order them and fill
        # # in any of the letters on the board to complete the word.
        # cells_played = self.board.convert_cells_played(cells_played)

        # # Returns a True if the cells played were true and false if they were not
        # valid = self.board.check_valid(cells_played)
        # print(valid)
        # # Updates the acrsoss/down checks and sum. Must be called after check_valid and only
        # # if the word is actully valid
        # self.board.cross_checks_sums(cells_played)
        # # Returns the score of the tiles played
        # score = self.board.compute_score(cells_played)
        # print(score)
        # # Run after previous commands
        # self.board.placed_cell_cleanup(cells_played)

        # self.board.board[9][9].letter = 'T'
        # self.board.board[11][9].letter = 'A'
        # self.board.board[12][9].letter = 'M'

        # cells_played = [self.board.board[11][9], self.board.board[12][9], self.board.board[9][9]]

        # cells_played = self.board.convert_cells_played(cells_played)
        # # Returns a True if the cells played were true and false if they were not
        # valid = self.board.check_valid(cells_played)
        # print(valid)
        # # Updates the acrsoss/down checks and sum. Must be called after check_valid
        # self.board.cross_checks_sums(cells_played)
        # # Returns the score of the tiles played
        # score = self.board.compute_score(cells_played)
        # print(score)
        # # Run after previous commands
        # self.board.placed_cell_cleanup(cells_played)

        self.draw_init()
        while self.running:
            self.handle_event()
            self.update()
            self.draw_update()

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
            if self.board.board[j][i].letter_mul == 2:
                pygame.draw.rect(self.surface, (66, 99, 247), tile)
                doub_letter = font.render('DL', 1, self.text_color)
                self.surface.blit(doub_letter, (7+self.tile_size*i, 10+self.tile_size*j))
            elif self.board.board[j][i].letter_mul == 3:
                pygame.draw.rect(self.surface, (34, 255, 45), tile)
                trip_letter = font.render('TL', 1, self.text_color)
                self.surface.blit(trip_letter, (7+self.tile_size*i, 10+self.tile_size*j))

        # if cell is a word multiplier
        elif self.board.board[j][i].word_mul != 1:
            font = pygame.font.Font(None, 20)
            if self.board.board[j][i].word_mul == 2:
                pygame.draw.rect(self.surface, (255, 87, 61), tile)
                doub_word = font.render('DW', 1, self.text_color)
                self.surface.blit(doub_word, (5+self.tile_size*i, 10+self.tile_size*j))
            elif self.board.board[j][i].word_mul == 3:
                pygame.draw.rect(self.surface, (255, 130, 35), tile)
                trip_word = font.render('TW', 1, self.text_color)
                self.surface.blit(trip_word, (5+self.tile_size*i, 10+self.tile_size*j))

        # if cell is the centre cell
        elif self.board.board[j][i].centre:
            font = pygame.font.Font(None, 20)
            pygame.draw.rect(self.surface, (241, 244, 66), tile)


        # draw empty cell
        else:
            pygame.draw.rect(self.surface, (33, 255, 192), tile)

    def draw_rack_tile(self, rack_tile):
        i = rack_tile
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


    def draw_board(self):
        for i in range(15):
            for j in range(15):
                self.draw_tile(i,j)


    def draw_rack(self):
        for i in range(4, 11):
            self.draw_rack_tile(i)

    def draw_selected_rack_tile(self, rack_tile):
        tile = pygame.Rect((0+self.tile_size*rack_tile, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile, 1)

    def draw_unselected_rack_tile(self, rack_tile):
        tile = pygame.Rect((0+self.tile_size*rack_tile, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (188, 255, 243), tile, 1)

    def draw_remove_rack_tile(self, rack_tile):
        tile = pygame.Rect((0+self.tile_size*rack_tile, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile)

    def draw_recall(self):
        # draw tile in rack
        tile = pygame.Rect((0+self.tile_size*1, 0+self.tile_size*16, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile)
        # draw letter on tile
        font = pygame.font.Font(None, 18)
        letter = font.render('Recall', 1, self.text_color)
        self.surface.blit(letter, (15+self.tile_size*1, 8+self.tile_size*16))

    def draw_play(self):
        # draw tile in rack
        tile = pygame.Rect((0+self.tile_size*12, 0+self.tile_size*16, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile)
        # draw letter on tile
        font = pygame.font.Font(None, 18)
        letter = font.render('Play', 1, self.text_color)
        self.surface.blit(letter, (20+self.tile_size*12, 8+self.tile_size*16))

    def handle_select_rack_tile(self, pos):
        for i in range(4, 11):
            tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
            if tile.collidepoint(pos):
                # check that the rack tile is not empty
                if self.player1.rack[i-4] != '':
                    self.player1.selected_tile = i - 4
                    self.player1.is_tile_selected = True
                    self.draw_selected_rack_tile(i)

    def handle_place_tile(self, pos):
        for i in range(15):
            for j in range(15):
                tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*j, self.tile_size-1, self.tile_size-1))
                if tile.collidepoint(pos):
                    if self.board.board[j][i].letter == None:
                        # set letter on the board from rack
                        self.player1.place_tile(self.player1.selected_tile, i, j)
                        print(self.player1.placed_tiles)
                        self.player1.is_tile_selected = False
                        # draw remove tile from rack and tile on board
                        self.draw_remove_rack_tile(self.player1.selected_tile+4)
                        self.draw_tile(i,j)
                        # set rack tile to empty
                        self.player1.rack[self.player1.selected_tile] = ''


    def handle_recall(self):
        self.player1.recall()
        for t in self.player1.placed_tiles:
            row = self.player1.placed_tiles[t][1][0]
            col = self.player1.placed_tiles[t][1][1]
            # draw removal of tiles from board
            self.draw_tile(col, row)

        # remove tile from placed tiles dictionary
        self.player1.placed_tiles = {}
        self.draw_rack()

    def handle_play(self):
        # if some tiles have been placed
        if self.player1.placed_tiles != {}:
            if self.player1.play_word():
                for t in self.player1.placed_tiles:
                    self.draw_rack_tile(t+4)
            else:
                self.handle_recall()


        self.player1.placed_tiles = {}

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            recall = pygame.Rect((0+self.tile_size*1, 0+self.tile_size*16, (self.tile_size-1)*2, self.tile_size-1))
            play = pygame.Rect((0+self.tile_size*12, 0+self.tile_size*16, (self.tile_size-1)*2, self.tile_size-1))
            rack = pygame.Rect((0+self.tile_size*4, 0+self.tile_size*16, (self.tile_size-1)*7, self.tile_size-1))
            if not self.player1.is_tile_selected:
                if rack.collidepoint(pos):
                    self.handle_select_rack_tile(pos)
                elif recall.collidepoint(pos):
                    self.handle_recall()
                elif play.collidepoint(pos):
                    self.handle_play()
            else:
                self.handle_place_tile(pos)

    def draw_update(self):
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()


    def draw_init(self):
        self.draw_board()
        self.draw_rack()
        self.draw_recall()
        self.draw_play()
        self.draw_update()



    def update(self):
        pass


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

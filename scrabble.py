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

        triple_word = set([(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)])
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
        word = word.upper()

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
        for cell in self.board[row]:
            if cell.letter != None:
                continue
            row = cell.row
            col = cell.col
            cell.anchor = True

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

            if prefix == '' and suffix == '':
                continue

            cell.across_sum = self.compute_score_already_placed(prefix_cell) + self.compute_score_already_placed(suffix_cell)
            self.dictionary.update_across_check(prefix, suffix, cell)

    def down_check(self, col):
        for row in self.board:
            cell = row[col]
            if cell.letter != None:
                continue
            row = cell.row
            col = cell.col
            cell.anchor = True

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

            if prefix == '' and suffix == '':
                continue

            cell.down_sum = self.compute_score_already_placed(prefix_cell) + self.compute_score_already_placed(suffix_cell)
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
        for cell in cells_played:
            cell.across_sum = 0
            cell.down_sum = 0
            cell.anchor = False

    def convert_cells_played(self, cells_played):
        """
        The cells played list can be in an order with just the cells that were played
        and not the ones already on the board. This function will order them and fill
        in any of the letters on the board to complete the word.
        """
        if len(cells_played) == 1:
            return cells_played
        elif cells_played[0].row == cells_played[1].row:
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

        else:
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
        self.board = Board('dictionary.txt')
        self.player1 = Player(self.board)
        self.player2 = Player(self.board)
        self.running = True
        self.tile_size = self.surface.get_width()/15
        self.text_color = (10, 10, 10)

    def play_game(self):

        self.board.board[10][8].letter = 'H'
        self.board.board[10][9].letter = 'E'
        self.board.board[10][10].letter = 'L'
        self.board.board[10][11].letter = 'L'
        self.board.board[10][12].letter = 'O'

        cells_played = [self.board.board[10][10], self.board.board[10][8], self.board.board[10][9], \
        self.board.board[10][11]]

        # The cells played list can be in an order with just the cells that were played
        # and not the ones already on the board. This function will order them and fill
        # in any of the letters on the board to complete the word. 
        cells_played = self.board.convert_cells_played(cells_played)

        # Returns a True if the cells played were true and false if they were not
        valid = self.board.check_valid(cells_played)
        print(valid)
        # Updates the acrsoss/down checks and sum. Must be called after check_valid and only
        # if the word is actully valid
        self.board.cross_checks_sums(cells_played)
        # Returns the score of the tiles played
        score = self.board.compute_score(cells_played)
        print(score)
        # Run after previous commands
        self.board.placed_cell_cleanup(cells_played)

        self.board.board[9][9].letter = 'T'
        self.board.board[11][9].letter = 'A'
        self.board.board[12][9].letter = 'M'

        cells_played = [self.board.board[11][9], self.board.board[12][9], self.board.board[9][9]]
        
        cells_played = self.board.convert_cells_played(cells_played)
        # Returns a True if the cells played were true and false if they were not
        valid = self.board.check_valid(cells_played)
        print(valid)
        # Updates the acrsoss/down checks and sum. Must be called after check_valid
        self.board.cross_checks_sums(cells_played)
        # Returns the score of the tiles played
        score = self.board.compute_score(cells_played)
        print(score)
        # Run after previous commands
        self.board.placed_cell_cleanup(cells_played)

        self.player1.rack = ['H', 'L', 'E', 'O', 'L', 'N', 'B']
        self.player1.place_tile(1, (0, 0))
        self.draw_board()
        self.draw_rack()
        self.draw()


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

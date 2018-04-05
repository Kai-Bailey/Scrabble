import pygame
from Board import *
from pygame.locals import *


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

        # self.board.board[7][7].letter = 'F'
        # self.board.board[7][8].letter = 'E'
        # self.board.board[7][9].letter = 'A'
        # self.board.board[7][10].letter = 'R'
        # cells_played = [self.board.board[7][7], self.board.board[7][8], self.board.board[7][9], self.board.board[7][10]]
        # cells_played = self.board.convert_cells_played(cells_played)
        # valid = self.board.check_valid(cells_played)
        # print(valid)
        # self.board.cross_checks_sums(cells_played)
        # score = self.board.compute_score(cells_played)
        # print("score: ", score)
        # self.board.placed_cell_cleanup(cells_played)

        # self.board.board[6][9].letter = 'T'
        # self.board.board[8][9].letter = 'R'
        # self.board.board[9][9].letter = 'N'
        # cells_played = [self.board.board[6][9], self.board.board[8][9], self.board.board[9][9]]
        # cells_played = self.board.convert_cells_played(cells_played)
        # valid = self.board.check_valid(cells_played)
        # print(valid)
        # self.board.cross_checks_sums(cells_played)
        # score = self.board.compute_score(cells_played)
        # print("score: ", score)
        # self.board.placed_cell_cleanup(cells_played)

        # self.board.board[7][11].letter = 'E'
        # self.board.board[7][12].letter = 'D'
        # cells_played = [self.board.board[7][11], self.board.board[7][12]]
        # cells_played = self.board.convert_cells_played(cells_played)
        # valid = self.board.check_valid(cells_played)
        # print(valid)
        # self.board.cross_checks_sums(cells_played)
        # score = self.board.compute_score(cells_played)
        # print("score: ", score)
        # self.board.placed_cell_cleanup(cells_played)

        # self.board.board[6][11].letter = 'T'
        # self.board.board[8][11].letter = 'A'
        # cells_played = [self.board.board[6][11], self.board.board[8][11]]
        # cells_played = self.board.convert_cells_played(cells_played)
        # valid = self.board.check_valid(cells_played)
        # print(valid)
        # self.board.cross_checks_sums(cells_played)
        # score = self.board.compute_score(cells_played)
        # print("score: ", score)
        # self.board.placed_cell_cleanup(cells_played)

        # self.board.board[7][6].letter = 'H'
        # self.board.board[7][7].letter = 'E'
        # self.board.board[7][8].letter = 'L'
        # self.board.board[7][9].letter = 'L'
        # self.board.board[7][10].letter = 'O'

        # cells_played = [self.board.board[7][6], self.board.board[7][7], self.board.board[7][8], \
        # self.board.board[7][9], self.board.board[7][10]]

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

        # test_rack = ['B', 'H', 'A', 'Z', 'E', 'O', 'L']

        # self.board.generate_moves(test_rack)

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

import pygame
from Board import *
from pygame.locals import *


class Player:
    def __init__(self, board, name):
        self.rack = []
        self.score = 0
        self.board = board
        self.name = name
        # dictionary for placed tiles: key is rack index, value is (letter, (row, col))
        self.placed_tiles = {}
        self.selected_tile = ''
        self.tile_selected = False
        # dictionary for tiles to exchange: key is rack index, value is letter
        self.tiles_to_exchange = {}

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
        self.players = [Player(self.board, 'Cody'), Player(self.board, 'Kai'), Player(self.board, 'Computer1'), Player(self.board, 'Computer2')]
        self.current_player_number = 0
        self.current_player = self.players[self.current_player_number]
        self.running = True
        self.exchanging = False
        self.tile_size = (self.surface.get_width()-200)/15
        self.text_color = (10, 10, 10)


    def play_game(self):

        # self.board.board[10][8].letter = 'H'
        # self.board.board[10][9].letter = 'E'
        # self.board.board[10][10].letter = 'L'
        # self.board.board[10][11].letter = 'L'
        # self.board.board[10][12].letter = 'O'
        #
        # cells_played = [self.board.board[10][10], self.board.board[10][8], self.board.board[10][9], \
        # self.board.board[10][11]]
        #
        # # The cells played list can be in an order with just the cells that were played
        # # and not the ones already on the board. This function will order them and fill
        # # in any of the letters on the board to complete the word.
        # cells_played = self.board.convert_cells_played(cells_played)
        #
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
        #
        # self.board.board[9][9].letter = 'T'
        # self.board.board[11][9].letter = 'A'
        # self.board.board[12][9].letter = 'M'
        #
        # cells_played = [self.board.board[11][9], self.board.board[12][9], self.board.board[9][9]]
        #
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
            pygame.draw.rect(self.surface, (247, 216, 153), tile)

    def draw_rack_tile(self, rack_tile):
        i = rack_tile
        # draw tile in rack
        tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (255, 200, 50), tile)
        # draw letter on tile
        font = pygame.font.Font(None, 24)
        letter = font.render(self.current_player.rack[i-4], 1, self.text_color)
        self.surface.blit(letter, (9+self.tile_size*i, 8+self.tile_size*16))
        # draw score in bottom right corner of tile
        font = pygame.font.Font(None, 12)
        letter_score = font.render(str(letter_scores[self.current_player.rack[i-4]]), 1, self.text_color)
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

    def draw_remove_rack_tile(self, rack_tile):
        tile = pygame.Rect((0+self.tile_size*rack_tile, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile)

    def draw_recall(self):
        tile = pygame.Rect((0+self.tile_size*1, 0+self.tile_size*15.25, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, (247, 234, 0), tile)
        font = pygame.font.Font(None, 18)
        letter = font.render('Recall', 1, self.text_color)
        self.surface.blit(letter, (15+self.tile_size*1, 8+self.tile_size*15.25))

    def draw_exchange(self, exchanging):
        tile = pygame.Rect((0+self.tile_size*1, 0+self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))
        if exchanging:
            pygame.draw.rect(self.surface, (255, 30, 56), tile)
        else:
            pygame.draw.rect(self.surface, (247, 234, 0), tile)

        font = pygame.font.Font(None, 18)
        letter = font.render('Exchange', 1, self.text_color)
        self.surface.blit(letter, (5+self.tile_size*1, 8+self.tile_size*16.75))

    def draw_play(self):
        tile = pygame.Rect((0+self.tile_size*12, 0+self.tile_size*15.25, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, (247, 234, 0), tile)
        font = pygame.font.Font(None, 18)
        letter = font.render('Play', 1, self.text_color)
        self.surface.blit(letter, (20+self.tile_size*12, 8+self.tile_size*15.25))


    def draw_skip(self):
        tile = pygame.Rect((0+self.tile_size*12, 0+self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, (247, 234, 0), tile)
        font = pygame.font.Font(None, 18)
        letter = font.render('Skip', 1, self.text_color)
        self.surface.blit(letter, (20+self.tile_size*12, 8+self.tile_size*16.75))

    def draw_player_names(self):
        font = pygame.font.Font(None, 22)
        for i in range(len(self.players)):
            letter = font.render(self.players[i].name, 1, self.text_color)
            self.surface.blit(letter, (10+self.tile_size*16, 40+self.tile_size*i))

    def draw_player_scores(self):
        font = pygame.font.Font(None, 22)
        for i in range(len(self.players)):
            letter = font.render(str(self.players[i].score), 1, self.text_color)
            self.surface.blit(letter, (10+self.tile_size*20, 40+self.tile_size*i))

    def draw_current_player(self):
        font = pygame.font.Font(None, 22)
        letter = font.render('>', 1, self.text_color)
        self.surface.blit(letter, (10+self.tile_size*15, 40+self.tile_size*(self.current_player_number)))

    def draw_tiles_left(self):
        font = pygame.font.Font(None, 22)
        letter = font.render('Tiles Left: ', 1, self.text_color)
        self.surface.blit(letter, (10+self.tile_size*16, 40+self.tile_size*5))

        letter = font.render(str(self.board.number_tiles), 1, self.text_color)
        self.surface.blit(letter, (10+self.tile_size*19, 40+self.tile_size*5))

    def draw_scoreboard(self):
        # clear all for redrawing
        tile = pygame.Rect((self.tile_size*15, 0, (self.tile_size-1)*6, (self.tile_size-1)*10))
        pygame.draw.rect(self.surface, (188, 255, 243), tile)
        font = pygame.font.Font(None, 28)
        letter = font.render('Scoreboard', 1, self.text_color)
        self.surface.blit(letter, (10+self.tile_size*16, 10))
        self.draw_player_names()
        self.draw_player_scores()
        self.draw_current_player()
        self.draw_tiles_left()

    def handle_select_rack_tile(self, pos):
        for i in range(4, 11):
            tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
            if tile.collidepoint(pos):
                # draw deselect of previous selected
                if self.current_player.tile_selected:
                    self.draw_rack_tile(self.current_player.selected_tile+4)
                # check that the rack tile is not empty
                if self.current_player.rack[i-4] != '':
                    self.current_player.selected_tile = i - 4
                    self.current_player.tile_selected = True
                    self.draw_selected_rack_tile(i)

    def handle_place_tile(self, pos):
        for i in range(15):
            for j in range(15):
                tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*j, self.tile_size-1, self.tile_size-1))
                if tile.collidepoint(pos):
                    if self.board.board[j][i].letter == None:
                        # set letter on the board from rack
                        self.current_player.place_tile(self.current_player.selected_tile, i, j)
                        print(self.current_player.placed_tiles)
                        self.current_player.tile_selected = False
                        # draw remove tile from rack and tile on board
                        self.draw_remove_rack_tile(self.current_player.selected_tile+4)
                        self.draw_tile(i,j)
                        # set rack tile to empty
                        self.current_player.rack[self.current_player.selected_tile] = ''


    def handle_recall(self):
        self.current_player.recall()
        for t in self.current_player.placed_tiles:
            row = self.current_player.placed_tiles[t][1][0]
            col = self.current_player.placed_tiles[t][1][1]
            # draw removal of tiles from board
            self.draw_tile(col, row)

        # remove tile from placed tiles dictionary
        self.current_player.placed_tiles = {}
        self.draw_rack()

    def handle_play(self):
        # if some tiles have been placed
        if self.current_player.placed_tiles != {}:
            if self.current_player.play_word():
                for t in self.current_player.placed_tiles:
                    self.draw_rack_tile(t+4)
                # change to next player
                self.current_player.placed_tiles = {}
                self.handle_endturn()
            else:
                self.handle_recall()
        print(self.current_player.rack)

    # changes to next player, redraws the rack and the scoreboard
    def handle_endturn(self):
        self.current_player_number += 1
        self.current_player_number = self.current_player_number % len(self.players)
        self.current_player = self.players[self.current_player_number]
        # turn exchanging off if the turn is ended
        self.exchanging = False
        self.draw_exchange(False)
        self.draw_rack()
        self.draw_scoreboard()


    # when in the exchanging state, handles select and deselect of tiles
    def handle_exchange_select_tile(self, pos):
        for i in range(4, 11):
            tile = pygame.Rect((0+self.tile_size*i, 0+self.tile_size*16, self.tile_size-1, self.tile_size-1))
            if tile.collidepoint(pos):
                # if the tiles is already selected, deselect it by redrawing the rack tile
                if (i-4) in self.current_player.tiles_to_exchange:
                    self.current_player.tiles_to_exchange.pop(i-4)
                    self.draw_rack_tile(i)
                # check that the rack tile is not empty, then select it
                elif self.current_player.rack[i-4] != '':
                    self.current_player.tiles_to_exchange[i-4] = self.current_player.rack[i-4]
                    self.draw_selected_rack_tile(i)

    def handle_exchange(self):
        if len(self.current_player.tiles_to_exchange) != 0:
            for tile in self.current_player.tiles_to_exchange:
                print(self.current_player.rack)
                self.current_player.rack.remove(self.current_player.tiles_to_exchange[tile])
                self.current_player.rack.insert(tile, self.board.draw_random_tile())

            self.current_player.tiles_to_exchange = {}
            self.handle_endturn()
        self.draw_rack()



    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            recall = pygame.Rect((0+self.tile_size*1, 0+self.tile_size*15.5, (self.tile_size-1)*2, self.tile_size-1))
            play = pygame.Rect((0+self.tile_size*12, 0+self.tile_size*15.5, (self.tile_size-1)*2, self.tile_size-1))
            skip = pygame.Rect((0+self.tile_size*12, 0+self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))
            rack = pygame.Rect((0+self.tile_size*4, 0+self.tile_size*16, (self.tile_size-1)*7, self.tile_size-1))
            exchange = pygame.Rect((0+self.tile_size*1, 0+self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))

            if rack.collidepoint(pos):
                if self.exchanging:
                    self.handle_exchange_select_tile(pos)
                else:
                    self.handle_select_rack_tile(pos)
            elif recall.collidepoint(pos):
                self.handle_recall()
            elif play.collidepoint(pos):
                self.handle_play()
            elif skip.collidepoint(pos):
                self.handle_recall()
                self.handle_endturn()
            elif exchange.collidepoint(pos):
                # recall any placed tiles
                self.handle_recall()
                if self.exchanging:
                    self.draw_exchange(False)
                    self.exchanging = False
                    self.handle_exchange()
                else:
                    self.draw_exchange(True)
                    self.draw_rack()
                    self.exchanging = True
            elif self.current_player.tile_selected:
                self.handle_place_tile(pos)

    def draw_update(self):
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()


    def draw_init(self):
        self.draw_board()
        self.draw_rack()
        self.draw_recall()
        self.draw_exchange(False)
        self.draw_play()
        self.draw_skip()
        self.draw_update()
        self.draw_scoreboard()


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
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

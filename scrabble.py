import pygame
from pygame.locals import *
from Board import *
from player import *
import time

class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.surface = background
        self.board = Board('dictionary.txt', 2)
        # dictionary for player types: key is player number, value is type in string
        self.player_types = {1:'Human', 2:'CPU', 3:'None', 4:'None'}
        # list of the players of the Player class
        self.players = []
        self.current_player_number = 0
        self.current_player = None
        self.winner = None
        self.running = True
        self.menu_screen = True
        self.end_game = False
        self.exchanging = False
        self.tile_size = (self.surface.get_width()-200)/15
        self.text_color = (10, 10, 10)
        self.tile_color = (255, 200, 50)
        self.button_color = (247, 234, 0)


    def play_game(self):
        # draw the menu screen
        self.draw_menu_screen()
        while self.menu_screen:
            self.handle_menu_event()
            self.draw_update()

        if self.running:
            # clear the screen
            self.surface.fill((188, 255, 243))
            self.draw_gameplay()

        # while the game is running
        while self.running:
            # handle any events
            self.handle_gameplay_event()
            # if the current player is a computer player
            if self.current_player.is_computer and not self.end_game:
                # if the current player
                if self.current_player.play_word_computer():
                    self.handle_endturn()
                    self.draw_board()
                    time.sleep(0.5)
                else:
                    self.end_game = True
                    self.draw_scoreboard()
                    self.handle_winner()
            self.draw_update()

    def draw_tile(self, row, col):
        """
        Draws a tile on the board given a row and col number.
        """
        i = row
        j = col
        # draw letter tile
        tile = pygame.Rect((self.tile_size*row, self.tile_size*j, self.tile_size-1, self.tile_size-1))
        # if cell has a letter
        if self.board.board[j][i].letter != None:
            pygame.draw.rect(self.surface, self.tile_color, tile)

            # draw letter on tile
            font = pygame.font.Font(None, 24)
            letter = font.render(self.board.board[j][i].letter, 1, self.text_color)
            self.surface.blit(letter, (9+self.tile_size*i, 8+self.tile_size*j))
            # draw letter score in bottom right corner of tile
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

    def draw_rack_tile(self, rack_ind):
        """
        Given an index for of the rack, draws the corresponding tile of the current
        player's rack tiles.
        """
        # variable for displacement of drawing
        i = rack_ind + 4
        # draw tile in rack
        tile = pygame.Rect((self.tile_size*i, self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, self.tile_color, tile)
        # draw letter on tile
        font = pygame.font.Font(None, 24)
        letter = font.render(self.current_player.rack[rack_ind], 1, self.text_color)
        self.surface.blit(letter, (9+self.tile_size*i, 8+self.tile_size*16))
        # draw score in bottom right corner of tile
        font = pygame.font.Font(None, 12)
        letter_score = font.render(str(letter_scores[self.current_player.rack[rack_ind]]), 1, self.text_color)
        self.surface.blit(letter_score, (20+self.tile_size*i, 20+self.tile_size*16))

    def draw_selected_rack_tile(self, rack_ind):
        """
        Draws an outline of the tile given a rack index to indicate which tile is selected.
        """
        tile = pygame.Rect((self.tile_size*(rack_ind+4), self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile, 1)

    def draw_remove_rack_tile(self, rack_ind):
        """
        Draws an empty tile given rack index. It is used for when the user places a tile on the board.
        """
        tile = pygame.Rect((self.tile_size*(rack_ind+4), self.tile_size*16, self.tile_size-1, self.tile_size-1))
        pygame.draw.rect(self.surface, (163, 81, 0), tile)

    def draw_board(self):
        """
        Draws the 15 by 15 cell board.
        """
        for i in range(15):
            for j in range(15):
                self.draw_tile(i,j)

    def draw_rack(self):
        """
        Draws the 7 tiles on the rack.
        """
        for i in range(7):
            self.draw_rack_tile(i)


    def draw_recall(self):
        """
        Draws the 'Recall' button in the bottom left of the screen.
        """
        rect_recall = pygame.Rect((self.tile_size*1, self.tile_size*15.25, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, self.button_color, rect_recall)
        font = pygame.font.Font(None, 18)
        text_recall = font.render('Recall', 1, self.text_color)
        self.surface.blit(text_recall, (15+self.tile_size*1, 8+self.tile_size*15.25))

    def draw_exchange(self, exchanging):
        """
        Draws the 'Exchange' button in the bottom left of the screen.
        If exchanging is True, then it will be drawn red to indicate that it is
        in the exchanging state.
        """
        rect_exchange = pygame.Rect((self.tile_size*1, self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))
        if exchanging:
            # draw red
            pygame.draw.rect(self.surface, (255, 30, 56), rect_exchange)
        else:
            # draw yellow
            pygame.draw.rect(self.surface, self.button_color, rect_exchange)

        font = pygame.font.Font(None, 18)
        text_exchange = font.render('Exchange', 1, self.text_color)
        self.surface.blit(text_exchange, (5+self.tile_size*1, 8+self.tile_size*16.75))

    def draw_play(self):
        """
        Draws the 'Play' button in the bottom right of the screen.
        """
        rect_play = pygame.Rect((self.tile_size*12, self.tile_size*15.25, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, self.button_color, rect_play)
        font = pygame.font.Font(None, 18)
        text_play = font.render('Play', 1, self.text_color)
        self.surface.blit(text_play, (20+self.tile_size*12, 8+self.tile_size*15.25))


    def draw_skip(self):
        """
        Draws the 'Skip' button in the bottom right of the screen.
        """
        rect = pygame.Rect((self.tile_size*12, self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))
        pygame.draw.rect(self.surface, self.button_color, rect)
        font = pygame.font.Font(None, 18)
        text_skip = font.render('Skip', 1, self.text_color)
        self.surface.blit(text_skip, (20+self.tile_size*12, 8+self.tile_size*16.75))


    def draw_player_names(self):
        """
        Draws the names of the players in the top right of the screen
        It gets the names from the self.players attribute.
        """
        font = pygame.font.Font(None, 22)
        for i in range(len(self.players)):
            text_name = font.render(self.players[i].name, 1, self.text_color)
            self.surface.blit(text_name, (10+self.tile_size*16, 40+self.tile_size*i))

    def draw_player_scores(self):
        """
        Draws the scores of the players in the top right of the screen.
        """
        font = pygame.font.Font(None, 22)
        for i in range(len(self.players)):
            text_score = font.render(str(self.players[i].score), 1, self.text_color)
            self.surface.blit(text_score, (10+self.tile_size*19, 40+self.tile_size*i))

    def draw_current_player(self):
        """
        Draws '>' beside the current player on the scoreboard to indicate whose
        turn it is.
        """
        font = pygame.font.Font(None, 22)
        text_curr = font.render('>', 1, self.text_color)
        self.surface.blit(text_curr, (10+self.tile_size*15, 40+self.tile_size*(self.current_player_number)))

    def draw_tiles_left(self):
        """
        Draws the 'Tiles Left' text along with the number of tiles remaining.
        """
        font = pygame.font.Font(None, 22)
        text_tiles_left = font.render('Tiles Left: ', 1, self.text_color)
        self.surface.blit(text_tiles_left, (10+self.tile_size*16, 40+self.tile_size*5))
        num_tiles = font.render(str(self.board.number_tiles), 1, self.text_color)
        self.surface.blit(num_tiles, (10+self.tile_size*19, 40+self.tile_size*5))

    def draw_scoreboard(self):
        """
        Clears the scoreboard by drawing a rect of the same color as the background
        over the scoreboard area. Then draws the scoreboard text and calls the functions
        that draw the names, scores, and tiles left.
        """
        # clear all for redrawing
        rect_scoreboard = pygame.Rect((self.tile_size*15, 0, (self.tile_size-1)*6, (self.tile_size-1)*10))
        pygame.draw.rect(self.surface, (188, 255, 243), rect_scoreboard)
        # draw the scoreboard text
        font = pygame.font.Font(None, 28)
        text_scoreboard = font.render('Scoreboard', 1, self.text_color)
        self.surface.blit(text_scoreboard, (10+self.tile_size*16, 10))
        # draw the scoreboard information
        self.draw_player_names()
        self.draw_player_scores()
        self.draw_current_player()
        self.draw_tiles_left()

    def draw_winner(self):
        font = pygame.font.Font(None, 22)
        text_winner = font.render('Winner: ' + self.winner + '!', 1, self.text_color)
        self.surface.blit(text_winner, (10+self.tile_size*16, 40+self.tile_size*8))

    def handle_player_type_select(self, pos):
        for i in range(1,5):
            rect = pygame.Rect(self.surface.get_width()/2 + 38, 80 + 40*i, 40, 30)
            if rect.collidepoint(pos):
                if i < 3:
                    if self.player_types[i] == 'Human':
                        self.draw_player_type(i, 'CPU')
                        self.player_types[i] = 'CPU'
                    elif self.player_types[i] == 'CPU':
                        self.draw_player_type(i, 'Human')
                        self.player_types[i] = 'Human'
                else:
                    if self.player_types[i] == 'Human':
                        self.draw_player_type(i, 'CPU')
                        self.player_types[i] = 'CPU'
                    elif self.player_types[i] == 'CPU':
                        self.draw_player_type(i, 'None')
                        self.player_types[i] = 'None'
                    elif self.player_types[i] == 'None':
                        self.draw_player_type(i, 'Human')
                        self.player_types[i] = 'Human'


    def handle_menu_play(self):
        for num, type in self.player_types.items():
            if type == 'CPU':
                self.players.append(Player(self.board, 'Player ' + str(num), True))
            elif type == 'Human':
                self.players.append(Player(self.board, 'Player ' + str(num), False))

        self.current_player = self.players[self.current_player_number]
        self.menu_screen = False



    def draw_player_type(self, player, type):
        rect = pygame.Rect(self.surface.get_width()/2 + 38, 80 + 40*player, 40, 30)
        if type == 'Human':
            pygame.draw.rect(self.surface, (250, 255, 0), rect)
            font = pygame.font.Font(None, 14)
            text_player = font.render('Human', 1, self.text_color)
            self.surface.blit(text_player, (self.surface.get_width()/2 + 43, 89 + 40*player))


        elif type == 'CPU':
            pygame.draw.rect(self.surface, (255, 72, 0), rect)
            font = pygame.font.Font(None, 14)
            text_player = font.render('CPU', 1, self.text_color)
            self.surface.blit(text_player, (self.surface.get_width()/2 + 50, 89 + 40*player))


        else:
            pygame.draw.rect(self.surface, (184, 184, 184), rect)
            font = pygame.font.Font(None, 14)
            text_player = font.render('None', 1, self.text_color)
            self.surface.blit(text_player, (self.surface.get_width()/2 + 47, 89 + 40*player))

            self.player_types[player] = 'None'


    def draw_menu_screen(self):
        font = pygame.font.Font(None, 60)
        text_scrabble = font.render('Scrabble', 1, self.text_color)
        self.surface.blit(text_scrabble, (self.surface.get_width()/2 - 85, 40))

        for player in range(1,5):
            # draw player names
            font = pygame.font.Font(None, 28)
            text_player = font.render('Player '+str(player), 1, self.text_color)
            self.surface.blit(text_player, (self.surface.get_width()/2 - 72, 85 + 40*player))
            if player == 1:
                self.draw_player_type(player, 'Human')
            elif player == 2:
                self.draw_player_type(player, 'CPU')
            else:
                self.draw_player_type(player, 'None')

        # draw play game button
        rect = pygame.Rect(self.surface.get_width()/2 - 85, 40*8, self.surface.get_width()/4, 50)
        pygame.draw.rect(self.surface, (66, 244, 69), rect)
        font = pygame.font.Font(None, 32)
        text_play = font.render('Play Game', 1, self.text_color)
        self.surface.blit(text_play, (self.surface.get_width()/2 - 55, 40*8.3))

    def draw_update(self):
        """
        Updates the display.
        """
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()


    def draw_gameplay(self):
        """
        Draws all gameplay drawings when the game starts.
        """
        self.draw_board()
        self.draw_rack()
        self.draw_recall()
        self.draw_exchange(False)
        self.draw_play()
        self.draw_skip()
        self.draw_update()
        self.draw_scoreboard()

    def handle_winner(self):
        max_player_score = 0
        for player in self.players:
            if player.score > max_player_score:
                max_player_score = player.score
                self.winner = player.name
        self.draw_winner()



    def handle_select_rack_tile(self, pos):
        """
        Handles the selection of a rack tile given a mouse position.
        """
        for i in range(7):
            tile = pygame.Rect((self.tile_size*(i+4), self.tile_size*16, self.tile_size-1, self.tile_size-1))
            if tile.collidepoint(pos):
                # draw deselect of previous selected
                if self.current_player.tile_selected:
                    self.draw_rack_tile(self.current_player.selected_tile)
                # check that the rack tile is not empty
                if self.current_player.rack[i] != '':
                    self.current_player.selected_tile = i
                    self.current_player.tile_selected = True
                    self.draw_selected_rack_tile(i)

    def handle_place_tile(self, pos):
        """
        Handles the placement of a tile on the board given a mouse position.
        """
        for i in range(15):
            for j in range(15):
                tile = pygame.Rect((self.tile_size*i, self.tile_size*j, self.tile_size-1, self.tile_size-1))
                if tile.collidepoint(pos):
                    if self.board.board[j][i].letter == None:
                        # set letter on the board from rack
                        self.current_player.place_tile(self.current_player.selected_tile, i, j)
                        print(self.current_player.placed_tiles)
                        self.current_player.tile_selected = False
                        # draw remove tile from rack and tile on board
                        self.draw_remove_rack_tile(self.current_player.selected_tile)
                        self.draw_tile(i,j)
                        # set rack tile to empty
                        self.current_player.rack[self.current_player.selected_tile] = ''

    def handle_recall(self):
        """
        Handles recall.
        Returns the tiles in the current player's placed tiles attribute.
        """
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
        """
        Handles the playing of a word when a user clicks 'play'.
        """
        # if some tiles have been placed
        if self.current_player.placed_tiles != {}:
            if self.current_player.play_word():
                for t in self.current_player.placed_tiles:
                    self.draw_rack_tile(t)
                # change to next player
                self.current_player.placed_tiles = {}
                self.handle_endturn()
            else:
                self.handle_recall()

    def handle_endturn(self):
        """
        Ends the players turn and changes to the next player.
        Redraws the exchange button, rack, and scoreboard.
        """
        # change to next player
        self.current_player_number += 1
        self.current_player_number = self.current_player_number % len(self.players)
        self.current_player = self.players[self.current_player_number]
        # turn exchanging off if the turn is ended
        self.exchanging = False
        self.draw_exchange(False)
        self.draw_rack()
        self.draw_scoreboard()

    def handle_exchange_select_tile(self, pos):
        """
        Handles select and deselect of tiles when in the exchanging state.
        """
        for i in range(7):
            tile = pygame.Rect((self.tile_size*(i+4), self.tile_size*16, self.tile_size-1, self.tile_size-1))
            if tile.collidepoint(pos):
                # if the tiles is already selected, deselect it by redrawing the rack tile
                if i in self.current_player.tiles_to_exchange:
                    self.current_player.tiles_to_exchange.pop(i)
                    self.draw_rack_tile(i)
                # check that the rack tile is not empty, then select it
                elif self.current_player.rack[i] != '':
                    self.current_player.tiles_to_exchange[i] = self.current_player.rack[i]
                    self.draw_selected_rack_tile(i)

    def handle_exchange(self):
        """
        Calls the exchange tiles method in the player class, if more than one
        tile is exchanged, it ends the turn and redraws the rack.
        """
        if self.current_player.exchange_tiles():
            self.handle_endturn()
        self.draw_rack()

    def handle_menu_event(self):
        """
        Handles events in the menu.
        """
        # grab event
        event = pygame.event.poll()
        # if the user clicks exit, then set self.running to false
        if event.type == QUIT:
            self.menu_screen = False
            self.running = False
        # if the user clicks the mouse button down
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            play_game = pygame.Rect(self.surface.get_width()/2 - 85, 40*8, self.surface.get_width()/4, 50)
            if play_game.collidepoint(pos):
                self.handle_menu_play()
            else:
                self.handle_player_type_select(pos)



    def handle_gameplay_event(self):
        """
        Handles events in the game. When the user clicks in the screen, it check
        if it has clicked on an area corresponding to a button or a tile.
        """
        # grab event
        event = pygame.event.poll()
        # if the user clicks exit, then set self.running to false
        if event.type == QUIT:
            self.running = False
        # if the user clicks the mouse button down
        elif event.type == MOUSEBUTTONDOWN and not self.end_game:
            pos = pygame.mouse.get_pos()
            # Rects to check if the mouse location when clicked corresponds to some game function
            recall = pygame.Rect((self.tile_size*1, self.tile_size*15.5, (self.tile_size-1)*2, self.tile_size-1))
            play = pygame.Rect((self.tile_size*12, self.tile_size*15.5, (self.tile_size-1)*2, self.tile_size-1))
            skip = pygame.Rect((self.tile_size*12, self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))
            rack = pygame.Rect((self.tile_size*4, self.tile_size*16, (self.tile_size-1)*7, self.tile_size-1))
            exchange = pygame.Rect((self.tile_size*1, self.tile_size*16.75, (self.tile_size-1)*2, self.tile_size-1))

            # if the rack is clicked
            if rack.collidepoint(pos):
                # check if it is in the exchanging state
                if self.exchanging:
                    # call the tile selection for exchanging tiles
                    self.handle_exchange_select_tile(pos)
                else:
                    # call the tile selection for placing tiles on the board
                    self.handle_select_rack_tile(pos)
            # if the recall button is clicked
            elif recall.collidepoint(pos):
                # call handle_recall
                self.handle_recall()
            # if the play button is clicked
            elif play.collidepoint(pos):
                # call handle_play
                self.handle_play()
            # if the skip button is clicked
            elif skip.collidepoint(pos):
                # call recall in case any tiles are on the board and then end turn
                self.handle_recall()
                self.handle_endturn()
            # if the exchange button is clicked
            elif exchange.collidepoint(pos):
                # recall any placed tiles
                self.handle_recall()
                # if in the exchanging state
                if self.exchanging:
                    # draw the exchange button as yellow
                    self.draw_exchange(False)
                    self.exchanging = False
                    self.handle_exchange()
                else:
                    # draw the exchange button as red
                    self.draw_exchange(True)
                    self.draw_rack()
                    self.exchanging = True
            # if tile is selected from the rack then handle placing it on the board
            elif self.current_player.tile_selected:
                self.handle_place_tile(pos)

def main():
    # initialize pygame
    pygame.init()
    # set the screen size to 700 by 600
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption('Scrabble')

    # create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((188, 255, 243))

    # update the display
    screen.blit(background, (0,0))
    pygame.display.flip()

    # run the game
    game = Game(screen, background)
    game.play_game()
    pygame.quit()


if __name__ == '__main__':
    main()

class Player:
    def __init__(self, board, name, is_computer):
        self.board = board
        # name of the player as a string
        self.name = name
        # list of letters in the player's rack
        self.rack = []
        # score of the player
        self.score = 0
        # dictionary for placed tiles: key is rack index, value is (letter, (row, col))
        self.placed_tiles = {}
        self.selected_tile = ''
        self.tile_selected = False
        # dictionary for tiles to exchange: key is rack index, value is letter
        self.tiles_to_exchange = {}
        # True if the player is a computer player, false if the player is a human player
        self.is_computer = is_computer
        # initialize the rack
        self.init_rack()

    def place_tile(self, rack_ind, row, col):
        """
        Place a tile on the board given a rack index, and a cell row and column.
        Adds the placed tile to the placed_tiles dictionary.
        """
        self.board.board[col][row].letter = self.rack[rack_ind]
        self.placed_tiles[self.selected_tile] = (self.rack[self.selected_tile], (col, row))
        # set the rack tile to an empty string
        self.rack[self.selected_tile] = ''

    def play_word(self):
        """
        Plays a word on the board. Looks in the placed_tiles dictionary and checks
        if it's a word. If it is, then it plays the word and returns true.
        """
        tiles_played = []
        new_tiles = {}

        for t in self.placed_tiles:
            row = self.placed_tiles[t][1][0]
            col = self.placed_tiles[t][1][1]
            cell = self.board.board[row][col]
            tiles_played.append(cell)

        # convert the tiles played to the whole word that the tiles made on the board
        word_played = self.board.convert_cells_played(tiles_played)

        # checks if the word is valid
        if self.board.check_valid(word_played):
            self.board.cross_checks_sums(word_played)
            self.score += self.board.compute_score(word_played)
            self.board.placed_cell_cleanup(word_played)

            # get new tiles and put on rack
            for t in self.placed_tiles:
                new_tiles[t] = self.board.draw_random_tile()
                self.rack[t] = new_tiles[t]
            return True
        else:
            return False

    def play_word_computer(self):
        """
        Plays a word on the board for the computer player. Returns False if it was
        unable to retrieve enough new tiles.
        """
        new_tiles = {}
        placed_tiles_computer = []

        # from the rack, get the word to be played, and add the score
        computer_rack = self.rack
        self.board.generate_moves(computer_rack)
        # tiles that make up the word in the board
        word_tiles = self.board.best_move_cell()
        self.board.cross_checks_sums(word_tiles)
        self.score += self.board.compute_score(word_tiles)
        self.board.placed_cell_cleanup(word_tiles)

        # from the tiles of the word formed on the board, retrieves the indices
        # of which tiles were the ones that were played from the rack
        for tile in word_tiles:
            for i in range(len(computer_rack)):
                if tile.letter == computer_rack[i]:
                    if i in placed_tiles_computer:
                        continue
                    placed_tiles_computer.append(i)
                    break

        # gets new tiles from the bag for every tile that was played
        for t in placed_tiles_computer:
            new_tile = self.board.draw_random_tile()
            if new_tile != None:
                new_tiles[t] = new_tile
                self.rack[t] = new_tiles[t]
            else:
                return False
        return True

    def recall(self):
        """
        Recalls the tiles back to the player's rack.
        Does not empty the placed_tiles dictionary.
        """
        for t in self.placed_tiles:
            row = self.placed_tiles[t][1][0]
            col = self.placed_tiles[t][1][1]
            # remove tiles from board
            self.board.board[row][col].letter = None
            # put tiles back on rack
            self.rack[t] = self.placed_tiles[t][0]

    def init_rack(self):
        """
        Initializes the rack by drawing 7 tiles from the bag.
        """
        for i in range(7):
            self.rack.append(self.board.draw_random_tile())


    # exchanges the tiles that are in the "tiles_to_exchange" attribute
    # returns true if one or more tiles were exchanged
    def exchange_tiles(self):
        """
        Exchanges the tiles that are in the "tiles_to_exchange" attribute.
        Returns true if one or more tiles were exchanged.
        """
        if len(self.tiles_to_exchange) != 0:
            for tile_ind, tile_let in self.tiles_to_exchange.items():
                # remove tile from rack
                self.rack.remove(tile_let)
                # put tile back in the bag and draw a new one
                new_tile = self.board.exchange_tile(tile_let)
                if new_tile != None:
                    # put the tile in the rack where the previous one was
                    self.rack.insert(tile_ind, new_tile)

            # clear the tiles to exchange dictionary
            self.tiles_to_exchange = {}
            return True
        else:
            return False

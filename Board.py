import Trie
from Cell import *
import random

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

        # A dictionary contain
        self.moves = []

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
            cell.across_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
            cell.down_check = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

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

    def generate_moves(self, rack):
        """
        Given a rack this function will return a list of cells representing the optimum
        move for the current state of the board.
        """
        for row in self.board:
            for cell in row:
                
                if not cell.anchor:
                    continue
                else:

                    # Consider the across move                
                    row = cell.row
                    col = cell.col
                    curr_cell = self.board[row][col-1]

                    partial_word = []

                    # Adjacent cell to the left is filled so just build the suffix
                    if curr_cell.letter != None:
                        while curr_cell.letter != None and col > 0:
                            partial_word.append((curr_cell.letter, curr_cell.row, curr_cell.col))
                            col -= 1
                            curr_cell = self.board[row][col]
                         
                        partial_word.reverse()
                        
                        # Traverse the trie tree to get to the correct node
                        node = self.dictionary.root
                        for item in partial_word:
                            node = node.children[item[0]]
                        

                        self.generate_suffix(partial_word[:], rack, cell, "A", node)

                    # Find the limit to build the left part
                    else:
                        limit = 0

                        while not curr_cell.anchor and col> 0 and limit < 7:
                            limit += 1
                            col -= 1
                            curr_cell = self.board[row][col]
    
                        self.generate_prefix([], limit, rack, cell, "A")                  
                    
                    # Consider the down move                
                    row = cell.row
                    col = cell.col
                    curr_cell = self.board[row-1][col]

                    # Reset the partial word
                    partial_word = []


                    # Adjacent cell above is filled so just build the suffix
                    if curr_cell.letter != None:
                        while curr_cell.letter != None and row > 0:
                            partial_word.append((curr_cell.letter, curr_cell.row, curr_cell.col))
                            row -= 1
                            curr_cell = self.board[row][col]
                        
                        partial_word.reverse()
                        
                        # Traverse the trie tree to get to the correct node
                        node = self.dictionary.root
                        for cell in partial_word:
                            node = node.children[cell.letter]
                        

                        self.generate_suffix(partial_word[:], rack, cell, "D", node)

                    # Find the limit to build the left part
                    else:
                        limit = 0

                        while not curr_cell.anchor and row > 0 and limit < 7:
                            limit += 1
                            row -= 1
                            curr_cell = self.board[row][col]
    
                        self.generate_prefix([], limit, rack, cell, "D")       

    def generate_prefix(self, partial_word, limit, rack, anchor, orientation, node=None):
        """
        Generates all possible prefixes given the limit and calls generate suffix to see if
        a valid word can be formed from them.
        """
        if node == None:
            node = self.dictionary.root

        self.generate_suffix(partial_word[:], rack, anchor, orientation, node)



        if limit > 0:
            for letter in node.children:
                if letter in rack:
                    child = node.children[letter]
                    rack.remove(child.letter)

                    row = anchor.row
                    col = anchor.col
                    if orientation == "A":
                        curr_cell = self.board[row][col-limit]
                    else:
                        curr_cell = self.board[row-limit][col]

                    partial_word.append((letter, curr_cell.row, curr_cell.col)) 
                    self.generate_prefix(partial_word, limit-1, rack, anchor, child)
                    rack.append(child.letter)


    def generate_suffix(self, partial_word, rack, cell, orientation, node):
        """
        Will generate all valid suffixes for the partial word and pass them to evaluate move to 
        be ranked.

        cell - Current cell on the board we are filling
        node - The node of the trie tree we are in based on the partial_word
        partial_word - The word we have built up so far
        rack - current letter we can build
        orientation - "A" for across or "D" for down 
        """
        if cell.letter == None:
            if node.terminate:
                self.evaluate_move(partial_word)


            for letter in node.children:
                if letter in rack:
                    if orientation == "A":
                        if letter not in cell.down_check:
                            continue
                    elif letter not in cell.across_check:
                        continue

                    rack.remove(letter)

                    # cell.letter = letter
                    partial_word.append((letter, cell.row, cell.col))

                    row = cell.row
                    col = cell.col

                    # Ensure that the word is not built off of the board
                    if row > 13 or col >13:
                        node = node.children[letter]
                        if node.terminate:
                            self.evaluate_move(partial_word)
                    else:
                        if orientation == "A":
                            curr_cell = self.board[row][col+1]
                        else:
                            curr_cell = self.board[row+1][col]

                        self.generate_suffix(partial_word[:], rack, curr_cell, orientation, node.children[letter])
                        partial_word = partial_word[:-1]
                        rack.append(letter)

        else:
            if cell.letter in node.children:
                
                partial_word.append((cell.letter, cell.row, cell.col))
                row = cell.row
                col = cell.col

                # Ensure that the word is not built off of the board
                if row > 13 or col > 13:
                    node = node.children[cell.letter]
                    if node.terminate:
                        self.evaluate_move(partial_word)
                else:
                    if orientation == "A":
                        curr_cell = self.board[row][col+1]
                    else:
                        curr_cell = self.board[row+1][col]
                    self.generate_suffix(partial_word[:], rack, curr_cell, orientation, node.children[cell.letter])
                    
    def evaluate_move(self, move):
        """
        When give a list of cells which represents a valid move this fucnction
        will calculate the score of the move and stores it in the board attribute
        """

        #score  = self.compute_score(move)
        move = move[:]
        print()
        print("Move Found!", move)
        print()
        self.moves.append(move)


# Trie tree

alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

class Node():
    """
    Nodes used in the trie tree. Holds the letter, children of the node and terminate.
    """
    
    def __init__(self, letter, terminate):
        # Letter node represents
        self.letter = letter
        # True if this is the ast letter in a valid word
        self.terminate = terminate
        # Children nodes
        self.children = {}
        

class TrieTree():
    """
    A Trie tree data structure used to hold all valid words. Words with the same prefix
    are stored along the same branch. The ends of words are reprented by having terminate true on
    the last letter.
    """

    def __init__(self):
        """
        The root node of the tree
        """
        self.root = Node("root", False)


    def add_word(self, word):
        """
        Adds a word to the trie tree by traversing throught the tree creating new nodes if
        neccesary. Ends the final node with terminate as true.
        """
        currNode = self.root

        # Traverse the tree adding node new nodes if neccesary 
        for letter in word[:-1]:
            # not_found is true if the current node does not have a child node with
            # the specified letter
            not_found = True

            # Search through children checking for the correct letter
            if letter in currNode.children:
                currNode = currNode.children[letter]
                not_found = False

        
            # If not found create a new child node
            if not_found:
                newNode = Node(letter, False)
                currNode.children[letter] = newNode
                currNode = newNode


        # Add the final node to the trie setting terminate to true
        not_found = True
        letter = word[-1]
        if letter in currNode.children:
            currNode.children[letter].terminate = True
            not_found = False

        
        if not_found:
            newNode = Node(letter, True)
            currNode.children[letter] = (newNode)
        

    def trie_from_txt(self, file_name):
        """
        Builds a trie tree from a text file where each word in the dictionary is a
        on a new line in the text file.
        """
        with open(file_name, mode='r') as file:
            for line in file:
                line = line.rstrip("\n")
                self.add_word(line)


    def update_down_check(self, prefix, suffix, cell):
        curr_node = self.root
        for letter in prefix:
            if letter in curr_node.children:
                curr_node = curr_node.children[letter]
                break

        for letter in alphabet:
            if letter not in curr_node.children:
                if letter in cell.down_check:
                    cell.down_check.remove(letter)
                continue
            if not self.valid_word(suffix, curr_node.children[letter]):
                if letter in cell.down_check:
                    cell.down_check.remove(letter)

    
    def update_across_check(self, prefix, suffix, cell):
        curr_node = self.root
        for letter in prefix:
            if letter in curr_node.children:
                curr_node = curr_node.children[letter]
                break

        for letter in alphabet:
            if letter not in curr_node.children:
                if letter in cell.across_check:
                    cell.across_check.remove(letter)
                continue
            if not self.valid_word(suffix, curr_node.children[letter]):
                if letter in cell.across_check:
                    cell.across_check.remove(letter)


    def left_part(self, partial_word, node, limit):
        pass

    def valid_word(self, word, root=None):
        """
        Checks if the a word is valid by traversing the trie tree. Word is a string and root
        defaults to the root of the Trie unless another starting point is specified.
        """
        if root == None:
            curr_node = self.root
        else:
            curr_node = root

        # Travers the trie tree to the last letter if there is a path
        for letter in word[:-1]:
            # not_found is true if the current node does not have a child node with
            # the specified letter
            not_found = True

            if letter in curr_node.children:
                curr_node = curr_node.children[letter]
                not_found = False
   
            
            if not_found:
                return False
        
        # If no word is being valid just ensure the starting node is terminated
        if len(word) == 0:
            if curr_node.terminate:
                return True
            else:
                return False

        # Check that the last node has terminate
        letter = word[-1]
        # for child in curr_node.children:
        if letter in curr_node.children and  curr_node.children[letter].terminate:
            return True

        return False



if __name__ == "__main__":
    trie_tree = TrieTree()
    trie_tree.trie_from_txt("dictionary.txt")
    print(trie_tree.valid_word("HELLO"))
    print(trie_tree.valid_word("TEST"))
    print(trie_tree.valid_word("TESTING"))
    print(trie_tree.valid_word("FALSE"))
    print(trie_tree.valid_word("THISIS"))
    print(trie_tree.valid_word("HIPPOPATMUSESES"))
    print(trie_tree.valid_word("DEFNNOT"))
    
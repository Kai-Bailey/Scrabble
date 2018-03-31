# Trie tree

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
        self.children = []
        

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
            for child in currNode.children:
                if child.letter == letter:
                    currNode = child
                    not_found = False
                    break
        
            # If not found create a new child node
            if not_found:
                newNode = Node(letter, False)
                currNode.children.append(newNode)
                currNode = newNode


        # Add the final node to the trie setting terminate to true
        not_found = True
        letter = word[-1]
        for child in currNode.children:
            if child.letter == letter:
                child.terminate = True
                not_found = False
                break
        
        if not_found:
            newNode = Node(letter, True)
            currNode.children.append(newNode)
        

    def trie_from_txt(self, file_name):
        """
        Builds a trie tree from a text file where each word in the dictionary is a
        on a new line in the text file.
        """
        with open(file_name, mode='r') as file:
            for line in file:
                line = line.rstrip("\n")
                trie_tree.add_word(line)



    def valid_word(self, word):
        """
        Checks if the a word is valid by traversing the trie tree. Word is a string.
        """
        curr_node = self.root
        
        # Travers the trie tree to the last letter if there is a path
        for letter in word[:-1]:
            # not_found is true if the current node does not have a child node with
            # the specified letter
            not_found = True
            for child in curr_node.children:
                if child.letter == letter:
                    curr_node = child
                    not_found = False
                    break
            
            if not_found:
                return False
        
        # Check that the last node has terminate
        letter = word[-1]
        for child in curr_node.children:
            if child.letter == letter and child.terminate:
                return True

        return False



if __name__ == "__main__":
    trie_tree = TrieTree()
    trie_tree.trie_from_txt("20k.txt")
    print(trie_tree.valid_word("hello"))
    print(trie_tree.valid_word("test"))
    print(trie_tree.valid_word("testing"))
    print(trie_tree.valid_word("false"))
    print(trie_tree.valid_word("tests"))
    print(trie_tree.valid_word("hippoptamusess"))
    print(trie_tree.valid_word("isvalid"))
    
    
    
    # tree = TrieTree()
    # tree.add_word("Hello")
    # tree.add_word("Helping")
    # tree.add_word("Test")
    # print(tree.valid_word("Hello"))
    # print(tree.valid_word("Cat"))
    # print(tree.valid_word("Test"))
    # print(tree.valid_word("Helping"))
    # print(tree.valid_word("Help"))
    # print(tree.valid_word("HelpingMe"))
    # tree.add_word("Kittens")
    # tree.add_word("Kit")
    # print(tree.valid_word("Kit"))
    # print(tree.valid_word("Kitten"))
    # print(tree.valid_word("Kittens"))
    # print(tree.valid_word("Kitt"))
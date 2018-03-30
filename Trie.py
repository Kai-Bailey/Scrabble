# Trie tree

class Node():
    
    def __init__(self, letter, terminate):
        self.letter = letter
        self.terminate = terminate
        self.children = []
        

class TrieTree():

    def __init__(self):
        self.root = Node("root", False)


    def add_word(self, word):
        currNode = self.root
         
        for letter in word[:-1]:
            not_found = True
            for child in currNode.children:
                if child.letter == letter:
                    currNode = child
                    not_found = False
                    break
        
            if not_found:
                newNode = Node(letter, False)
                currNode.children.append(newNode)
                currNode = newNode


        # Add the final node to the trie
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
        with open(file_name, mode='r') as file:
            for line in file:
                line = line.rstrip("\n")
                trie_tree.add_word(line)



    def valid_word(self, word):
        curr_node = self.root

        
        for letter in word[:-1]:
            not_found = True
            for child in curr_node.children:
                if child.letter == letter:
                    curr_node = child
                    not_found = False
                    break
            
            if not_found:
                return False
        
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
import pygame
from pygame.locals import *

letter_scores = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
                'H': 4, 'I': 1, 'J':8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
                'P': 3, 'Q': 10, 'R': 1, 'S': 1 'T': 1, 'U':1, 'V': 4, 'W': 4,
                 'X': 8, 'Y': 4, 'Z': 10}

class Board:
    pass

class Cell:
    pass

class Player:
    pass

class Tile:
    pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption('Scrabble')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((188, 255, 243))

    # font = pygame.font.Font(None, 36)
    # text = font.render('Scrabble', 1, (188, 51, 35))
    # textpos = text.get_rect(centerx=background.get_width()/2)
    # background.blit(text, textpos)

    screen.blit(background, (0,0))
    pygame.display.flip()


    # tile = pygame.Surface((30, 30))
    # tile.fill((239, 188, 79))
    # background.blit(tile, (0, 0))


    font = pygame.font.Font(None, 13)
    letter = font.render('A', 1, (10, 10, 10))
    letterpos = letter.get_rect(centerx=tile.get_width()/2)
    tile.blit(letter, (0,0))

    for i in range(15):
        for j in range(15):
            pygame.draw.rect(background, (70, 96, 91), (0+30*i, 0+30*j, 30, 30), 3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.blit(background, (0,0))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()

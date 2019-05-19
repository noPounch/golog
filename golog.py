import sys
import pygame
from pygame.locals import *
from cat import *


def main():
    #window initialization
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display)

    #simpSet initialization
    golog = simpSet()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    golog.addSimplex(0,data=event.pos)
                    print([o.label for o in golog.simplecies])

        pygame.display.flip()

main()

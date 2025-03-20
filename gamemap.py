import pygame
# importerar det som behövs, variabler och klasser, från andra filer
from settings import *
from tiles import Tile1, Tile2, Tile3


class GameMap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
    # tar in två sprite.Groups 
    def draw_map(self, groups):
        # går igenom alla listor och tar ut indexen för varje lista genom enumrate funktionen
        for r_index, row in enumerate(GAME_MAP):
                # tar raden och går igenom varje item samt skriver ut dess index 
                for c_index, col in enumerate(row):
                    # räknar ut x positionen, horisontalt, genom att ta platsen i raden
                    # och multiplicera med storleken som är en kostant för varje tile
                    x = c_index * RECT_SIZE
                    # räknra ut y position, vertikalt, genom att ta indexen för listan
                    # uppifrån ner och multiplierar med konstanten
                    y = r_index * RECT_SIZE
                    # om itemet i listan är 1, 2, 3 så skapas en instans av tilen
                    # som har positionen x och y utifrån ovan beräknade
                    # samt tillhör två grupper, en för rendering och en för kollision
                    if col == 1:
                        Tile1((x, y), groups= groups)
                    if col == 2:
                         Tile2((x, y), groups= groups)
                    if col == 3:
                         Tile3((x, y), groups= groups)
                    

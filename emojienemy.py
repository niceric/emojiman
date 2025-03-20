import pygame
from settings import *


class EmojiEnemy(pygame.sprite.Sprite):
    # tar argument när den instansieras för att populera dom på olika platser
    # med olika antal steg och hastighet
    def __init__(self, start_x, start_y, steps, speed):
        super(EmojiEnemy, self).__init__()
        # laddar in bilden
        self.surface = pygame.image.load(ENEMY_SURFACE).convert()  
        # tar ovan argument och lägger till 20
        self.rect = self.surface.get_rect(center = (start_x + 20, start_y + 20))
        self.steps = steps 
        self.speed = speed
        self.direction_left = -self.speed
        self.direction_right = self.speed
        # skapar två stegräknare, vänster och höger
        self.steps_left = 0
        self.steps_right = 0
        
    def update(self):
        # kollar om antal steg åt vänster INTE har tagits
        # om INTE så fortsätter vi i if-satsen för varje spelloop
        if self.steps_left != self.steps:
            # förflyttar fienden åt vänster
            self.rect.move_ip(self.direction_left, 0)
            # lägger till ett steg till stegräknaren åt vänster
            self.steps_left = self.steps_left + 1

        # kollar om stegen åt vänster har tagits
        # och om steget åt höger INTE har tagits
        # går in i den if-satsen om så är fallet
        if self.steps_left == self.steps and self.steps_right != self.steps:
            # förluyttar fienden åt höger
            self.rect.move_ip(self.direction_right, 0)
            # lägger till steg till stegräkmnaren åt höger
            self.steps_right = self.steps_right + 1
            # om stegem åt höger har tagits 
            # så sätter vi tillbaka bägge stegräknarna till 0
            # så den första if-satsen gås in i igen
            if self.steps_right == self.steps:
                self.steps_left = 0
                self.steps_right = 0

        



    

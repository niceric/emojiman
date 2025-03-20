import pygame
# importerar från filer/moduler för anvädning nedan
import random
from settings import *


class EmojiMan(pygame.sprite.Sprite):
    def __init__(self):
        super(EmojiMan, self).__init__()
        # laddar in emoji bilden
        self.surface = pygame.image.load(EMOJI_SURFACE).convert()
        self.rect = self.surface.get_rect(topleft = PLAYER_START)
        self.bottom = self.rect.bottom

        # skapar instans av .Vector2 klassen för beräkningar i 2D
        self.direction = pygame.math.Vector2()
        # sätter variabler för använding i rörelseberäkning
        self.steps = 4
        self.jump_speed = 8
        self.gravity = 0.3
        self.jumped = False

    def apply_gravity(self):
        # tar och adderar direction.y med sig själv + gravitations variablen så den ständigt ökar
        self.direction.y += self.gravity
        # tar rect.y, dess position, med sig själv + riktningen
        self.rect.y += self.direction.y
        
        

    def update(self, key):
        if key[LEFT]:
            # tar och sätter objektets direction till negativt tal 
            self.direction.x = -self.steps
            # tar och adderar objektets x position med ovan riktning,
            # detta för att det inte finns någon gravitation som för y-axeln
            self.rect.x += self.direction.x
        if key[RIGHT]:
            self.direction.x = self.steps
            self.rect.x += self.direction.x 
            # kollar om space samt .jumped är False
        if key[SPACE] and self.jumped == False:
            # ändrar riktningen för y-axeln
            self.direction.y = -self.jump_speed
            # säkerställer så man inte kan hoppa flera gånger
            self.jumped = True
 
    # här kollra vi kollision, först x-axeln sedan sätter gravitation sist y-axeln
    def collision(self, player, collision_sprites): 
        # går igenom sprites i gruppen med collision_sprites som innehåller tiles
        for sprite in collision_sprites:
            # kollar om det är kollision med spelares .rect mot någon av tilesen
            if sprite.rect.colliderect(player.rect):
                # om spelarens riktning är negativ, är på väg åt vänster
                if self.direction.x < 0:
                    # då ska spelarens vänstersida sättas på tilens högersida som det är kollision mot
                    self.rect.left = sprite.rect.right
                # kollar om spelarens riktning är positiv, är på väg åt höger
                if self.direction.x > 0:
                    # spelarens högersida sätts på tilens vänstersidan som det är kollision mot
                    self.rect.right = sprite.rect.left
        
        # applicerar gravitation så spelaren hela tiden dras mot ett ökat y-värde, 
        # är alltså på väg nedåt/faller
        self.apply_gravity()

        # går åter igenom tiles spriten
        for sprite in collision_sprites:
            # kollar om det är kollision mellan en tiles.rect och spelarens .rect
            if sprite.rect.colliderect(player.rect):
                # om spelarens riktning är negativ, så är den på väg uppåt/hoppat                
                if self.direction.y < 0:
                    # sätter spelarens top mot tilens botten
                    self.rect.top = sprite.rect.bottom
                    # nollställer riktnigen så den inte fastnar/limmar sig
                    self.direction.y = 0
                # om spelarens riktning är positiv så är den på väg nedåt/faller
                if self.direction.y > 0:
                    # sätter spelarens botten på tilens top
                    self.rect.bottom = sprite.rect.top
                    # nollställer så gravitationen nollställs och fallet "börjar om"
                    self.direction.y = 0
                    # nu vet vi att spelarens står på en rect och kan då få hoppa igen
                    self.jumped = False

class FlyingEmoji(pygame.sprite.Sprite):
    def __init__(self):
        super(FlyingEmoji, self).__init__()
        # laddar in bilder samt skapar en .rect med start positino som kwarg
        # använder random.randint för att få dom att starta på olika platser utanför skärmen
        self.surface = pygame.image.load("assets/emoji_man_rect3.png").convert()
        self.rect = self.surface.get_rect(
            center = 
            (
            random.randint(0, 2900), 
            random.randint(-20, 0)
            )
        )
    # ser till att emojin flyger snettneråt 
    def fly(self, started):
        self.rect.move_ip(-4, 4)
        # tar bort objektet om det flyger utanför skärmen, prestanda skäl
        if self.rect.right == 0:
            self.kill()
        # om spelet har startat med ENTER så tar den bort alla flygande så 
        # man inte behlver vänta tills dom lämnat skärmen
        if started == True:
            self.kill()
        

class FlyingClouds(pygame.sprite.Sprite):
    def __init__(self):
        super(FlyingClouds, self).__init__()
        # laddar in bilder och sätter startposition med random.randint för att få
        # olika start platser utanför skärmen
        self.surface = pygame.image.load("assets/emoji_cloud1.png").convert_alpha()
        self.rect = self.surface.get_rect(center = 
            (
            random.randint(W, W + 100), 
            random.randint(0, H)
            ))
        # ger hastigheten en random int för att få olika hastigheter på molnen
        self.flying_speed = random.randint(-5, -1)

    # göratt molnen förflyttar sig
    def fly(self, started):
        self.rect.move_ip(self.flying_speed, 0)
        # tar bort dom om dom är utanför skärmen
        if self.rect.right < -50:
            self.kill()
        

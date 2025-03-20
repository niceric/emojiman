import pygame
# importerar från andra filer nödvändiga variabler samt klasser
from settings import *
from emojiman import FlyingEmoji

class Watermelon(pygame.sprite.Sprite):
    def __init__(self):
        super(Watermelon, self).__init__()
        # laddar in bilden för vattenmelonen
        self.surface = pygame.image.load("assets/emoji_man_watermelon1.png").convert_alpha()
        # skapar en rect och ger dess startposition
        self.rect = self.surface.get_rect(center = (1520, 560))

class Apples(pygame.sprite.Sprite):
    def __init__(self):
        super(Apples, self).__init__()
        self.surface = pygame.image.load("assets/emoji_man_apple1.png").convert_alpha()
        self.rect = self.surface.get_rect(center = (1440, 1000))
        
        
class Scores():
    def __init__(self, fruit_group):
        # tar en sprite.Group med frukter
        self.fruit_group = fruit_group
        # sätter startpoängen till 0
        self.current_score = 0

    def get_scores(self, player):
        # går igenom frukterna i spritegruppen
        for fruit in self.fruit_group:
            if pygame.Rect.colliderect(player.rect, fruit.rect):
                # om kollision med spelaren och en av frukterna
                # lägg till ett poäng och ta bort frukten
                self.current_score += 1
                fruit.kill()
                



class DrawScore():
    def __init__(self):
        # skapar två font variabler
        self.score_font = pygame.font.Font('assets/RETRO_SPACE.ttf', 50)
        self.instruct_font = pygame.font.Font('assets/RETRO_SPACE.ttf', 40)
        # laddar in startskärmens titel
        self.surface = pygame.image.load("assets/start_screen.png").convert_alpha()
        self.rect = self.surface.get_rect(x = 0, y = 0)
    
    def display_score(self, current_score):
        # tar in nuvarande poäng
        self.current_score = current_score
        # använder fonten ovan för att skapa en surface med text och nuvarande poäng
        self.score_surf = self.score_font.render(f'SCORE {self.current_score}', False, (10,10,10))
        # skickar rendering av ovan
        SCREEN.blit(self.score_surf, (100, 70))

    # nollställer poängen
    def score_reset(self): 
        return 0

    
    def game_over(self, current_score):
        # skickar in bakgrunden som backgrund för texten nedan
        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(self.surface, self.rect)
        # om poängen är 1 eller 0 när man dör
        self.instruct_surf = self.instruct_font.render('You lost. Press ENTER to start again.', False, (10, 10, 10))
        self.instruct_rect = self.instruct_surf.get_rect(center = (960, 540))
        # om man får 2 poäng
        self.score_message = self.score_font.render(f'YOU WON!', False, (64, 64, 64))
        self.score_message_rect = self.score_message.get_rect(center = (960, 540))
        
        # kollar poängen som skickas in som argument 
        # renderar någon av ovan skapade variabler med text
        if current_score == 0 or current_score == 1:
            SCREEN.blit(self.instruct_surf, self.instruct_rect)

        else:
            SCREEN.blit(self.score_message, self.score_message_rect)

    def draw_text(self):
        # renderar bakgrund med variabler med text som innehåller instruktioner
        SCREEN.blit(BACKGROUND, (0, 0))
        self.instruct_surf = self.instruct_font.render('Press ENTER to start the game.', False, (10, 10, 10))
        self.instruct_rect = self.instruct_surf.get_rect(center = (660, 540))
        self.instruct2_surf = self.instruct_font.render('Jump - SPACE', False, (10, 10, 10))
        self.instruct2_rect = self.instruct_surf.get_rect(center = (660, 590))
        self.instruct3_surf = self.instruct_font.render('Direction - LEFT and RIGHT arrows', False, (10, 10, 10))
        self.instruct3_rect = self.instruct_surf.get_rect(center = (660, 640))
        self.instruct4_surf = self.instruct_font.render('ESC to exit.', False, (10, 10, 10))
        self.instruct4_rect = self.instruct_surf.get_rect(center = (660, 690))
        self.instruct5_surf = self.instruct_font.render('Collect the fruits to win while avoiding the enemies.', False, (10, 10, 10))
        self.instruct5_rect = self.instruct_surf.get_rect(center = (660, 740))

        # skickar ovan variabler för rendering
        SCREEN.blit(self.instruct_surf, self.instruct_rect)
        SCREEN.blit(self.instruct2_surf, self.instruct2_rect)
        SCREEN.blit(self.instruct3_surf, self.instruct3_rect)
        SCREEN.blit(self.instruct4_surf, self.instruct4_rect)
        SCREEN.blit(self.instruct5_surf, self.instruct5_rect)
        SCREEN.blit(self.surface, self.rect)

class Life:
    def __init__(self):
        # skapar en startlista med 3 items, ett för varje hjärta
        self.starting_hearts = [1, 1, 1]
        # sätter nuvarande antal hjärtan, i början 3 hjärtan
        self.current_hearts = self.starting_hearts
        # laddar in bilden på hjärtat
        self.surface = pygame.image.load("assets/heart.png").convert_alpha()
        self.rect = self.surface.get_rect()
        # skapar font för "LIFE"
        self.score_font = pygame.font.Font('assets/RETRO_SPACE.ttf', 50)

    def draw_hearts(self):
        # skapar LIFE texten och skickar den till blit/rendering
        self.life_counter = self.score_font.render(f"LIFE ", False, (10, 25, 25))
        SCREEN.blit(self.life_counter, (1440, 70))
        # kollar längden på listan/antal nuvrande hjärtan och 
        # renderar bilderna beornde på längden
        if len(self.current_hearts) == 3:
            SCREEN.blit(self.surface, (1600, 60))

        if len(self.current_hearts) >= 2:
            SCREEN.blit(self.surface, (1680, 60))

        if len(self.current_hearts) >= 1:
            SCREEN.blit(self.surface, (1760, 60))
    # nollställer listan med hjärtan
    def reset_hearts(self):
        self.current_hearts = [1, 1, 1]